# Pandemic Environment
This code was adapted for "Preventing Reward Hacking using Occupancy Measure Regularization". More details about how to run experiments can be found within our main repository and our paper. We have edited the environment so that safe policy actions can be generated, and the proxy and true reward can be calculated simultaneously. 

This repository is based on the [code](https://github.com/aypan17/reward-misspecification/tree/main/pandemic) of [Pan et al.](https://arxiv.org/abs/2201.03544). 

The original code release for the Sony Research Pandemic Simulator environment can be found [here](https://github.com/SonyResearch/PandemicSimulator).

## Installation
Running 
```
pip install -r requirements.txt
```
from our main repository will install this package along with all of its depedencies. 

## Citation
If you plan to use the simulator in your research, please cite us using: 
```
@misc{kompella2020reinforcement,
      title={Reinforcement Learning for Optimization of COVID-19 Mitigation policies}, 
      author={Varun Kompella* and Roberto Capobianco* and Stacy Jong and Jonathan Browne and Spencer Fox and Lauren Meyers and Peter Wurman and Peter Stone},
      year={2020},
      eprint={2010.10560},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```


