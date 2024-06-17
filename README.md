# NitroBlast Project

Welcome to the TU Delft iGEM 2024 NitroBlast project repository. This repository contains all the code and data used in the project.

## Repository Structure

- `data/`: Contains all data files
  - `adk1075-data/`: Data from Tyler H. Coale et al., Nitrogen-fixing organelle in a marine alga.Science384, 217-222(2024).
  - `plmsearch-data/`: Results from the PLM search
  - `ucyn-a_enriched/`: Sequence data, embeddings, alignments, and other data for UCYN-A enriched proteins
  - `utp-data/`: Sequence data, MEME results, HMM profiles, and other data related to the ucyn-a transit peptide
- `notebooks/`: Jupyter notebooks for data analysis
- `scripts/`: Python scripts for data processing
- `results/`: Final, cleaned results such as figures and tables
- [`JOURNAL.md`](./JOURNAL.md): Detailed notes on the project progress

## Setup

The project uses Python and conda for package management. To set up the project:

1. Clone the repository
2. Create a new conda environment: `conda env create -f environment.yml`
3. Activate the environment: `conda activate nitroblast`

_Tip:_ [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html) is a faster alternative to `conda`.

## External Data

- Protein embeddings for UCYN-A enriched proteins: [embeddings.h5](https://drive.google.com/file/d/1if9G5A8y1yuj26wgD8ZvvAIppa_i1hVN/view?usp=drive_link)
