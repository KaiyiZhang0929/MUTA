# MUTA

Research code accompanying **Design, Implementation, and Deployment of Multi-Task Neural Networks in Programmable Data-Planes** by Kaiyi Zhang, Changgang Zheng, Nancy Samaan, Ahmed Karmouch, and Noa Zilberman.

MUTA enables multiple network prediction tasks to share a neural network and run inference in programmable switch data planes. It also supports distributing model layers across multiple switches.

## Code overview

- **`QoE Train`**: A Jupyter/Colab notebook stored without an extension. Includes video QoE data preparation, multi-task model training, quantization, and evaluation for stalling, startup delay, resolution, and bitrate prediction, with baseline experiments.
- **`P4Generator.ipynb`**: Generates P4 programs for individual neural network layers targeting Intel Tofino/TNA switches.
- **`P4/`**: Intended to contain the P4 implementations of the three model layers.
- **`Deployment Orchestrator/`**: Intended to contain topology and model-placement optimization code for distributed deployment.

The training notebook expects external datasets and uses Google Drive paths that need to be adapted. P4 deployment requires the appropriate Tofino development environment. The paper PDF is excluded from this repository.

## Source file status

The original files are preserved as supplied. At import, all four `.py` files in `Deployment Orchestrator/` and all three `.p4` files in `P4/` contained only `0xFF` bytes, rather than readable source code. These seven files need to be restored from working originals before use; their intended roles above are inferred from the paper and filenames. Both notebook files parse as valid notebook JSON. Experiments and switch deployment have not been run or validated.
