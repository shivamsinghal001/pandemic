# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.

from collections import OrderedDict, defaultdict
from itertools import combinations
from itertools import product as cartesianproduct
from typing import DefaultDict, Dict, List, Optional, Sequence, Type, cast

import numpy as np
from ordered_set import OrderedSet

from .contact_tracing import MaxSlotContactTracer
from .infection_model import SEIRModel, SpreadProbabilityParams
from .interfaces import (DEFAULT, ContactRate, ContactTracer,
                         GlobalTestingState, InfectionModel, InfectionSummary,
                         Location, LocationID, PandemicRegulation,
                         PandemicSimState, PandemicTesting, PandemicTestResult,
                         Person, PersonID, PersonRoutineAssignment, Registry,
                         SimTime, SimTimeInterval, get_infection_summary,
                         globals, sorted_infection_summary)
from .location import (Bar, GroceryStore, HairSalon, Home, Hospital, Office,
                       Restaurant, RetailStore, School)
from .make_population import make_population
from .pandemic_testing_strategies import RandomPandemicTesting
from .simulator_config import PandemicSimConfig
from .simulator_opts import PandemicSimOpts

__all__ = ["PandemicSim", "make_locations"]


def make_locations(sim_config: PandemicSimConfig) -> List[Location]:
    return [
        config.location_type(
            loc_id=f"{config.location_type.__name__}_{i}",
            init_state=config.location_type.state_type(**config.state_opts),
            **config.extra_opts,
        )  # type: ignore
        for config in sim_config.location_configs
        for i in range(config.num)
    ]


class PandemicSim:
    """Class that implements the pandemic simulator."""

    _id_to_person: Dict[PersonID, Person]
    _id_to_location: Dict[LocationID, Location]
    _infection_model: InfectionModel
    _pandemic_testing: PandemicTesting
    _registry: Registry
    _contact_tracer: Optional[ContactTracer]
    _new_time_slot_interval: SimTimeInterval
    _infection_update_interval: SimTimeInterval
    _infection_threshold: int
    _numpy_rng: np.random.RandomState

    _type_to_locations: DefaultDict
    _hospital_ids: List[LocationID]
    _persons: Sequence[Person]
    _state: PandemicSimState

    def __init__(
        self,
        locations: Sequence[Location],
        persons: Sequence[Person],
        infection_model: Optional[InfectionModel] = None,
        infection_model_delta: Optional[InfectionModel] = None,
        pandemic_testing: Optional[PandemicTesting] = None,
        contact_tracer: Optional[ContactTracer] = None,
        new_time_slot_interval: SimTimeInterval = SimTimeInterval(day=1),
        infection_update_interval: SimTimeInterval = SimTimeInterval(day=1),
        person_routine_assignment: Optional[PersonRoutineAssignment] = None,
        infection_threshold: int = 0,
        hospital_capacity: int = 0,
        delta_start_lo: int = 366,
        delta_start_hi: int = 367,
    ):
        """
        :param locations: A sequence of Location instances.
        :param persons: A sequence of Person instances.
        :param infection_model: Infection model instance, if None SEIR default infection model is used.
        :param pandemic_testing: PandemicTesting instance, if None RandomPandemicTesting default instance is used.
        :param contact_tracer: Optional ContactTracer instance.
        :param new_time_slot_interval: interval for updating contact tracer if that is not None. Default is set daily.
        :param infection_update_interval: interval for updating infection states. Default is set once daily.
        :param person_routine_assignment: An optional PersonRoutineAssignment instance that assign PersonRoutines to
            each person
        :param infection_threshold: If the infection summary is greater than the specified threshold, a
            boolean in PandemicSimState is set to True.
        """
        assert (
            globals.registry
        ), "No registry found. Create the repo wide registry first by calling init_globals()"
        self._registry = globals.registry
        self._numpy_rng = np.random.RandomState(
            np.random.randint(low=0, high=2**31)
        )  # globals.numpy_rng

        self._id_to_location = OrderedDict({loc.id: loc for loc in locations})
        assert self._registry.location_ids.issuperset(self._id_to_location)
        self._id_to_person = OrderedDict({p.id: p for p in persons})
        assert self._registry.person_ids.issuperset(self._id_to_person)

        self._infection_model = infection_model or SEIRModel()
        self._infection_model_delta = infection_model_delta or SEIRModel()
        self._pandemic_testing = pandemic_testing or RandomPandemicTesting()
        self._contact_tracer = contact_tracer
        self._new_time_slot_interval = new_time_slot_interval
        self._infection_update_interval = infection_update_interval
        self._infection_threshold = infection_threshold
        self._delta_start_lo = delta_start_lo
        self._delta_start_hi = delta_start_hi
        self._delta_start = self._numpy_rng.randint(
            self._delta_start_lo, self._delta_start_hi
        )

        self._type_to_locations = defaultdict(list)
        for loc in locations:
            self._type_to_locations[type(loc)].append(loc)
        self._hospital_ids = [loc.id for loc in locations if isinstance(loc, Hospital)]

        self._max_hospital_capacity = hospital_capacity

        self._persons = persons
        self._minors = []
        self._workers = []
        self._retirees = []
        for p in persons:
            if p._id.age <= 18:
                self._minors.append(p)
            elif p._id.age <= 65:
                self._workers.append(p)
            else:
                self._retirees.append(p)

        # assign routines
        if person_routine_assignment is not None:
            for _loc in person_routine_assignment.required_location_types:
                assert (
                    _loc.__name__ in globals.registry.location_types
                ), f"Required location type {_loc.__name__} not found. Modify sim_config to include it."
            person_routine_assignment.assign_routines(persons)

        self._state = PandemicSimState(
            id_to_person_state={person.id: person.state for person in persons},
            id_to_location_state={
                location.id: location.state for location in locations
            },
            location_type_infection_summary={
                type(location): 0 for location in locations
            },
            global_infection_summary={s: 0 for s in sorted_infection_summary},
            global_infection_summary_alpha={s: 0 for s in sorted_infection_summary},
            global_infection_summary_delta={s: 0 for s in sorted_infection_summary},
            global_testing_state=GlobalTestingState(
                summary={
                    s: len(persons) if s == InfectionSummary.NONE else 0
                    for s in sorted_infection_summary
                },
                num_tests=0,
            ),
            global_testing_state_alpha=GlobalTestingState(
                summary={
                    s: len(persons) if s == InfectionSummary.NONE else 0
                    for s in sorted_infection_summary
                },
                num_tests=0,
            ),
            global_testing_state_delta=GlobalTestingState(
                summary={
                    s: len(persons) if s == InfectionSummary.NONE else 0
                    for s in sorted_infection_summary
                },
                num_tests=0,
            ),
            global_location_summary=self._registry.global_location_summary,
            sim_time=SimTime(),
            regulation_stage=0,
            regulation_stage_sum=0,
            infection_above_threshold=False,
        )

        self.location_names = [
            "Home",
            "GroceryStore",
            "Office",
            "School",
            "Hospital",
            "RetailStore",
            "HairSalon",
            "Restaurant",
            "Bar",
        ]
        self.person_types = ["Minor", "Worker", "Retired"]
        self.prev_loc_data = np.zeros(2 * len(self.location_names))

    @classmethod
    def from_config(
        cls: Type["PandemicSim"],
        sim_config: PandemicSimConfig,
        sim_opts: PandemicSimOpts = PandemicSimOpts(),
    ) -> "PandemicSim":
        """
        Creates an instance using config

        :param sim_config: Simulator config
        :param sim_opts: Simulator opts
        :return: PandemicSim instance
        """
        assert (
            globals.registry
        ), "No registry found. Create the repo wide registry first by calling init_globals()"

        # make locations
        locations = make_locations(sim_config)

        # make population
        persons = make_population(sim_config)

        # make infection model
        infection_model = SEIRModel(
            spread_probability_params=SpreadProbabilityParams(
                sim_opts.infection_spread_rate_mean,
                sim_opts.infection_spread_rate_sigma,
            )
        )

        infection_model_delta = SEIRModel(
            spread_probability_params=SpreadProbabilityParams(
                sim_opts.infection_delta_spread_rate_mean,
                sim_opts.infection_delta_spread_rate_sigma,
            )
        )

        # setup pandemic testing
        pandemic_testing = RandomPandemicTesting(
            spontaneous_testing_rate=sim_opts.spontaneous_testing_rate,
            symp_testing_rate=sim_opts.symp_testing_rate,
            critical_testing_rate=sim_opts.critical_testing_rate,
            testing_false_positive_rate=sim_opts.testing_false_positive_rate,
            testing_false_negative_rate=sim_opts.testing_false_negative_rate,
            retest_rate=sim_opts.retest_rate,
        )

        # create contact tracing app (optional)
        contact_tracer = (
            MaxSlotContactTracer(storage_slots=sim_opts.contact_tracer_history_size)
            if sim_opts.use_contact_tracer
            else None
        )

        # setup sim
        return PandemicSim(
            persons=persons,
            locations=locations,
            infection_model=infection_model,
            infection_model_delta=infection_model_delta,
            pandemic_testing=pandemic_testing,
            contact_tracer=contact_tracer,
            infection_threshold=sim_opts.infection_threshold,
            person_routine_assignment=sim_config.person_routine_assignment,
            hospital_capacity=sim_config.max_hospital_capacity,
            delta_start_lo=sim_config.delta_start_lo,
            delta_start_hi=sim_config.delta_start_hi,
        )

    @property
    def registry(self) -> Registry:
        """Return registry"""
        return self._registry

    def _compute_contacts(self, location: Location) -> OrderedSet:
        assignees = location.state.assignees_in_location
        visitors = location.state.visitors_in_location
        cr = location.state.contact_rate

        groups = [(assignees, assignees), (assignees, visitors), (visitors, visitors)]
        constraints = [
            (cr.min_assignees, cr.fraction_assignees),
            (cr.min_assignees_visitors, cr.fraction_assignees_visitors),
            (cr.min_visitors, cr.fraction_visitors),
        ]

        contacts: OrderedSet = OrderedSet()

        for grp, cst in zip(groups, constraints):
            grp1, grp2 = grp
            minimum, fraction = cst

            possible_contacts = list(
                combinations(grp1, 2) if grp1 == grp2 else cartesianproduct(grp1, grp2)
            )
            num_possible_contacts = len(possible_contacts)

            if len(possible_contacts) == 0:
                continue

            fraction_sample = min(1.0, max(0.0, self._numpy_rng.normal(fraction, 1e-2)))
            real_fraction = max(minimum, int(fraction_sample * num_possible_contacts))

            # we are using an orderedset, it's repeatable
            contact_idx = self._numpy_rng.randint(
                0, num_possible_contacts, real_fraction
            )
            contacts.update([possible_contacts[idx] for idx in contact_idx])

        return contacts

    def _compute_infection_probabilities(self, contacts: OrderedSet) -> None:
        infectious_states = {InfectionSummary.INFECTED, InfectionSummary.CRITICAL}

        for c in contacts:
            id_person1 = c[0]
            id_person2 = c[1]
            person1_state = self._id_to_person[id_person1].state
            person2_state = self._id_to_person[id_person2].state
            person1_inf_state = person1_state.infection_state
            person2_inf_state = person2_state.infection_state
            person1_inf_state_delta = person1_state.infection_state_delta
            person2_inf_state_delta = person2_state.infection_state_delta

            if (
                # both are not infectious
                (person1_inf_state is None and person2_inf_state is None)
                or
                # both are already infected
                (
                    person1_inf_state is not None
                    and person2_inf_state is not None
                    and person1_inf_state.summary in infectious_states
                    and person2_inf_state.summary in infectious_states
                )
            ):
                continue
            elif (
                person1_inf_state is not None
                and person1_inf_state.summary in infectious_states
            ):
                spread_probability = (
                    person1_inf_state.spread_probability
                    * person1_state.infection_spread_multiplier
                )
                person2_state.not_infection_probability *= 1 - spread_probability
                person2_state.not_infection_probability_history.append(
                    (
                        person2_state.current_location,
                        person2_state.not_infection_probability,
                    )
                )
            elif (
                person2_inf_state is not None
                and person2_inf_state.summary in infectious_states
            ):
                spread_probability = (
                    person2_inf_state.spread_probability
                    * person2_state.infection_spread_multiplier
                )
                person1_state.not_infection_probability *= 1 - spread_probability
                person1_state.not_infection_probability_history.append(
                    (
                        person1_state.current_location,
                        person1_state.not_infection_probability,
                    )
                )

            if (
                # both are not infectious
                (person1_inf_state_delta is None and person2_inf_state_delta is None)
                or
                # both are already infected
                (
                    person1_inf_state_delta is not None
                    and person2_inf_state_delta is not None
                    and person1_inf_state_delta.summary in infectious_states
                    and person2_inf_state_delta.summary in infectious_states
                )
            ):
                continue
            elif (
                person1_inf_state_delta is not None
                and person1_inf_state_delta.summary in infectious_states
            ):
                spread_probability = (
                    person1_inf_state_delta.spread_probability
                    * person1_state.infection_spread_multiplier_delta
                )
                person2_state.not_infection_probability_delta *= 1 - spread_probability
                person2_state.not_infection_probability_delta_history.append(
                    (
                        person2_state.current_location,
                        person2_state.not_infection_probability_delta,
                    )
                )
            elif (
                person2_inf_state_delta is not None
                and person2_inf_state_delta.summary in infectious_states
            ):
                spread_probability = (
                    person2_inf_state_delta.spread_probability
                    * person2_state.infection_spread_multiplier_delta
                )
                person1_state.not_infection_probability_delta *= 1 - spread_probability
                person1_state.not_infection_probability_delta_history.append(
                    (
                        person1_state.current_location,
                        person1_state.not_infection_probability_delta,
                    )
                )

    def _test_result_to_infection_summary(
        self,
        new_result: PandemicTestResult,
        prev_result: Optional[PandemicTestResult] = None,
    ) -> InfectionSummary:
        if new_result == PandemicTestResult.UNTESTED:
            return InfectionSummary.NONE
        elif new_result == PandemicTestResult.NEGATIVE:
            if prev_result in [
                PandemicTestResult.POSITIVE,
                PandemicTestResult.CRITICAL,
            ]:
                return InfectionSummary.RECOVERED
            else:
                return InfectionSummary.NONE
        elif new_result == PandemicTestResult.POSITIVE:
            return InfectionSummary.INFECTED
        elif new_result == PandemicTestResult.CRITICAL:
            return InfectionSummary.CRITICAL
        elif new_result == PandemicTestResult.DEAD:
            return InfectionSummary.DEAD

    def _update_global_testing_state(
        self,
        state: GlobalTestingState,
        new_result: PandemicTestResult,
        prev_result: PandemicTestResult,
    ) -> None:
        if new_result == prev_result:
            # nothing to update
            return

        new_summary = self._test_result_to_infection_summary(new_result, prev_result)
        prev_summary = self._test_result_to_infection_summary(prev_result)

        if prev_summary == InfectionSummary.NONE and state.summary[prev_summary] == 0:
            prev_summary = InfectionSummary.RECOVERED
        assert state.summary[prev_summary] > 0

        state.summary[new_summary] += 1
        state.summary[prev_summary] -= 1
        state.num_tests += 1  # update number of tests

        if new_result != PandemicTestResult.DEAD:
            state.num_tests += 1

    # def poll(self) -> np.ndarray:
    #     """Returns an observation of the current state of the simulator. Used to update regulation specifics."""
    #     time = [float(self._state.sim_time.day / 365)]
    #     stage = [int(self._state.regulation_stage)]
    #     stage_sum = [0] if self._state.regulation_stage_sum == 0 else [float(self._state.regulation_stage_sum / self._state.sim_time.day)]
    #     threshold_reached = [int(self._state.infection_above_threshold)]
    #     #hospitalizations = [max(self._max_hospital_capacity, self._state.global_infection_summary.get(InfectionSummary.CRITICAL))]
    #     test_results = [self._state.global_testing_state.summary.get(s) / len(self._persons) for s in sorted_infection_summary]
    #     summary = np.array(time + stage + stage_sum + threshold_reached + test_results)
    #     return summary

    #     # loc_data = []
    #     # for l in self.location_names:
    #     #     entries = 0
    #     #     visits = 0
    #     #     for p in self.person_types:
    #     #         entries += self._state.global_location_summary[(l, p)].entry_count
    #     #         visits += self._state.global_location_summary[(l, p)].visitor_count
    #     #     loc_data.append(entries)
    #     #     loc_data.append(visits)
    #     # # Subtract because we only want a moving average of the previous restrictions
    #     # loc_data = (np.array(loc_data) - self.prev_loc_data) / len(self._persons)
    #     # self.prev_loc_data = loc_data

    #     #return np.concatenate([summary, loc_data])

    def step(self) -> None:
        """Method that advances one step through the simulator"""
        # sync all locations
        for location in self._id_to_location.values():
            location.sync(self._state.sim_time)
        self._registry.update_location_specific_information()

        # call person steps (randomize order)
        for i in self._numpy_rng.randint(0, len(self._persons), len(self._persons)):
            self._persons[i].step(self._state.sim_time, self._contact_tracer)

        # update person contacts
        for location in self._id_to_location.values():
            contacts = self._compute_contacts(location)

            if self._contact_tracer:
                self._contact_tracer.add_contacts(contacts)

            self._compute_infection_probabilities(contacts)

        # call infection model steps
        if self._infection_update_interval.trigger_at_interval(self._state.sim_time):
            global_infection_summary = {s: 0 for s in sorted_infection_summary}
            global_infection_summary_alpha = {s: 0 for s in sorted_infection_summary}
            global_infection_summary_delta = {s: 0 for s in sorted_infection_summary}
            for person in self._id_to_person.values():
                # infection model step
                person.state.infection_state = self._infection_model.step(
                    person.state.infection_state,
                    person.id.age,
                    person.state.risk,
                    1 - person.state.not_infection_probability,
                )

                if person.state.infection_state.exposed_rnb != -1.0:
                    for vals in person.state.not_infection_probability_history:
                        if person.state.infection_state.exposed_rnb < 1 - vals[1]:
                            infection_location = vals[0]
                            break

                    person_location_type = self._registry.location_id_to_type(
                        infection_location
                    )
                    self._state.location_type_infection_summary[
                        person_location_type
                    ] += 1

                # delta infection model step --- only run if delta variant emerged
                if self._state.sim_time.day > self._delta_start:
                    person.state.infection_state_delta = (
                        self._infection_model_delta.step(
                            person.state.infection_state_delta,
                            person.id.age,
                            person.state.risk,
                            1 - person.state.not_infection_probability_delta,
                        )
                    )

                    if person.state.infection_state_delta.exposed_rnb != -1.0:
                        for (
                            vals
                        ) in person.state.not_infection_probability_delta_history:
                            if (
                                person.state.infection_state_delta.exposed_rnb
                                < 1 - vals[1]
                            ):
                                infection_location = vals[0]
                                break

                        person_location_type = self._registry.location_id_to_type(
                            infection_location
                        )
                        self._state.location_type_infection_summary[
                            person_location_type
                        ] += 1

                global_infection_summary[get_infection_summary(person.state)] += 1
                if person.state.infection_state is None:
                    global_infection_summary_alpha[InfectionSummary.NONE] += 1
                else:
                    global_infection_summary_alpha[
                        person.state.infection_state.summary
                    ] += 1
                if person.state.infection_state_delta is None:
                    global_infection_summary_delta[InfectionSummary.NONE] += 1
                else:
                    global_infection_summary_delta[
                        person.state.infection_state_delta.summary
                    ] += 1

                person.state.not_infection_probability = 1.0
                person.state.not_infection_probability_delta = 1.0
                person.state.not_infection_probability_history = []
                person.state.not_infection_probability_delta_history = []

                # test the person for infection
                if self._pandemic_testing.admit_person(person.state):
                    (
                        new_test_result,
                        new_test_result_alpha,
                        new_test_result_delta,
                    ) = self._pandemic_testing.test_person(person.state)
                    self._update_global_testing_state(
                        self._state.global_testing_state,
                        new_test_result,
                        person.state.test_result,
                    )
                    self._update_global_testing_state(
                        self._state.global_testing_state_alpha,
                        new_test_result_alpha,
                        person.state.test_result_alpha,
                    )
                    self._update_global_testing_state(
                        self._state.global_testing_state_delta,
                        new_test_result_delta,
                        person.state.test_result_delta,
                    )
                    person.state.test_result = new_test_result
                    person.state.test_result_alpha = new_test_result_alpha
                    person.state.test_result_delta = new_test_result_delta

            self._state.global_infection_summary = global_infection_summary
            self._state.global_infection_summary_alpha = global_infection_summary_alpha
            self._state.global_infection_summary_delta = global_infection_summary_delta

        self._state.infection_above_threshold = (
            self._state.global_testing_state.summary[InfectionSummary.INFECTED]
            >= self._infection_threshold
        )

        self._state.global_location_summary = self._registry.global_location_summary

        if self._contact_tracer and self._new_time_slot_interval.trigger_at_interval(
            self._state.sim_time
        ):
            self._contact_tracer.new_time_slot()

        # call sim time step
        self._state.sim_time.step()

        self._check_testing_state()

    def _check_testing_state(self):
        testing_state: GlobalTestingState
        for test_result_attr, testing_state in [
            ("test_result", self._state.global_testing_state),
            ("test_result_alpha", self._state.global_testing_state_alpha),
            ("test_result_delta", self._state.global_testing_state_delta),
        ]:
            expected_summary = {k: 0 for k in InfectionSummary}
            for person in self._id_to_person.values():
                test_result: PandemicTestResult = getattr(
                    person.state, test_result_attr
                )
                if (
                    test_result == PandemicTestResult.UNTESTED
                    or test_result == PandemicTestResult.NEGATIVE
                ):
                    expected_summary[InfectionSummary.NONE] += 1
                elif test_result == PandemicTestResult.POSITIVE:
                    expected_summary[InfectionSummary.INFECTED] += 1
                elif test_result == PandemicTestResult.CRITICAL:
                    expected_summary[InfectionSummary.CRITICAL] += 1
                elif test_result == PandemicTestResult.DEAD:
                    expected_summary[InfectionSummary.DEAD] += 1
            assert (
                expected_summary[InfectionSummary.NONE]
                == (
                    testing_state.summary[InfectionSummary.NONE]
                    + testing_state.summary[InfectionSummary.RECOVERED]
                )
                and expected_summary[InfectionSummary.INFECTED]
                == testing_state.summary[InfectionSummary.INFECTED]
                and expected_summary[InfectionSummary.CRITICAL]
                == testing_state.summary[InfectionSummary.CRITICAL]
                and expected_summary[InfectionSummary.DEAD]
                == testing_state.summary[InfectionSummary.DEAD]
            )

    def step_day(self, hours_in_a_day: int = 24) -> None:
        for _ in range(hours_in_a_day):
            self.step()

    @staticmethod
    def _get_cr_from_social_distancing(
        location: Location, social_distancing: float
    ) -> ContactRate:
        new_fraction = 1 - social_distancing
        cr = location.state.contact_rate
        init_cr = location.init_state.contact_rate
        new_cr = ContactRate(
            cr.min_assignees,
            cr.min_assignees_visitors,
            cr.min_visitors,
            new_fraction * init_cr.fraction_assignees,
            new_fraction * init_cr.fraction_assignees_visitors,
            new_fraction * init_cr.fraction_visitors,
        )

        return new_cr

    def impose_regulation(self, regulation: PandemicRegulation) -> None:
        """
        Receive a regulation that updates the simulator dynamics

        :param regulation: a PandemicRegulation instance
        """
        # update location rules
        sd = regulation.social_distancing
        loc_type_rk = regulation.location_type_to_rule_kwargs

        for loc_type, locations in self._type_to_locations.items():
            rule_kwargs = {}
            if loc_type_rk is not None and loc_type in loc_type_rk:
                rule_kwargs.update(loc_type_rk[loc_type])

            if sd is not None:
                # cr is the same for all locations of a given type. So just use one location to compute the new cr.
                cr = (
                    DEFAULT
                    if sd == DEFAULT
                    else self._get_cr_from_social_distancing(
                        locations[0], cast(float, sd)
                    )
                )
                rule_kwargs.update(dict(contact_rate=cr))

            for loc in locations:
                loc.update_rules(loc.location_rule_type(**rule_kwargs))

        # update person policy
        for person in self._id_to_person.values():
            person.receive_regulation(regulation)

        self._state.regulation_stage = regulation.stage
        self._state.regulation_stage_sum += regulation.stage

    @property
    def state(self) -> PandemicSimState:
        """
        Property that returns the current state of the simulator.

        :return: Current state of the simulator.
        """

        return self._state

    def reset(self) -> None:
        for location in self._id_to_location.values():
            location.reset()
        for person in self._id_to_person.values():
            person.reset()

        self._infection_model.reset()
        self._infection_model_delta.reset()

        num_persons = len(self._id_to_person)
        self._state = PandemicSimState(
            id_to_person_state={
                person_id: person.state
                for person_id, person in self._id_to_person.items()
            },
            id_to_location_state={
                loc_id: loc.state for loc_id, loc in self._id_to_location.items()
            },
            location_type_infection_summary={
                type(location): 0 for location in self._id_to_location.values()
            },
            global_infection_summary={s: 0 for s in sorted_infection_summary},
            global_infection_summary_alpha={s: 0 for s in sorted_infection_summary},
            global_infection_summary_delta={s: 0 for s in sorted_infection_summary},
            global_location_summary=self._registry.global_location_summary,
            global_testing_state=GlobalTestingState(
                summary={
                    s: num_persons if s == InfectionSummary.NONE else 0
                    for s in sorted_infection_summary
                },
                num_tests=0,
            ),
            global_testing_state_alpha=GlobalTestingState(
                summary={
                    s: num_persons if s == InfectionSummary.NONE else 0
                    for s in sorted_infection_summary
                },
                num_tests=0,
            ),
            global_testing_state_delta=GlobalTestingState(
                summary={
                    s: num_persons if s == InfectionSummary.NONE else 0
                    for s in sorted_infection_summary
                },
                num_tests=0,
            ),
            sim_time=SimTime(),
            regulation_stage=0,
            regulation_stage_sum=0,
            infection_above_threshold=False,
        )
        self._delta_start = self._numpy_rng.randint(
            self._delta_start_lo, self._delta_start_hi
        )
