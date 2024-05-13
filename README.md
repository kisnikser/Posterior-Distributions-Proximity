# Sample Size Determination: Posterior Distributions Proximity

**Author:** Nikita Kiselev

**Advisor:** Andrey Grabovoy

## Abstract
The issue of sample size determination is crucial for constructing an effective machine learning model. 
However, the existing methods for determining a sufficient sample size are either not strictly proven, or relate to the specific statistical hypothesis about the distribution of model parameters. 
In this paper we present two approaches based on the proximity of posterior distributions of model parameters on similar subsamples. 
We show that these two methods are valid for the model with normal posterior distribution of parameters. 
Computational experiments demonstrate the convergence of the proposed functions as the sample size increases.

## Repository Structure
The repository is structured as follows:
- `paper`: This directory contains the main paper in PDF format (`main.pdf`) and the LaTeX source file (`main.tex`). Also there is a directory `figs` with images used in the paper.
- `code`: This directory contains the code used in the paper. It has its own `README.md` file providing a detailed description of the code files.
