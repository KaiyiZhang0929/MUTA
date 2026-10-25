# MUTA

**Design, Implementation, and Deployment of Multi-Task Neural Networks in Programmable Data-Planes**, TNSM.

MUTA enables multiple network prediction tasks to share a neural network and run inference in programmable switch data planes. It also supports distributing model layers across multiple switches.

## Code overview

- **`QoE_Train.ipynb`**: A Jupyter/Colab notebook. Includes video QoE data preparation, multi-task model training, quantization, and evaluation for stalling, startup delay, resolution, and bitrate prediction, with baseline experiments.
- **`P4Generator.ipynb`**: Generates P4 programs for individual neural network layers targeting Intel Tofino/TNA switches.
- **`P4/`**: Intended to contain the P4 implementations of the three model layers.
- **`Deployment Orchestrator/`**: Intended to contain topology and model-placement optimization code for distributed deployment.
