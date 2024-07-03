<div align="center">
<h1>Sample Size Determination: Posterior Distributions Proximity </h1>

[Nikita Kiselev](https://github.com/kisnikser)<sup>1 :email:</sup>, [Andrey Grabovoy](https://github.com/andriygav)<sup>1</sup>

<sup>1</sup> Moscow Institute of Physics and Technology

<sup>:email:</sup> corresponding author

[📝 Paper](https://github.com/kisnikser/Posterior-Distributions-Proximity/blob/main/paper/main.pdf), [</> Code](https://github.com/kisnikser/Posterior-Distributions-Proximity/tree/main/code), [🎬 Video](https://www.youtube.com/watch?v=WnIRaRl730A&t=1728s)

</div>

## 🔍 Abstract
The issue of sample size determination is crucial for constructing an effective machine learning model. 
However, the existing methods for determining a sufficient sample size are either not strictly proven, or relate to the specific statistical hypothesis about the distribution of model parameters. 
In this paper we present two approaches based on the proximity of posterior distributions of model parameters on similar subsamples. 
We show that these two methods are valid for the model with normal posterior distribution of parameters. 
Computational experiments demonstrate the convergence of the proposed functions as the sample size increases.

## 📚 Overview
<div align="center">
  <img alt="overview" src="https://github.com/kisnikser/Posterior-Distributions-Proximity/assets/70231416/1765dacb-a3f0-4be2-84c6-c997a0a22884">
</div>


## 🗃️ Repository Structure
The repository is structured as follows:
- `paper`: This directory contains the main paper in PDF format (`main.pdf`) and the LaTeX source file (`main.tex`). Also there is a directory `figs` with images used in the paper.
- `code`: This directory contains the code used in the paper. It has its own `README.md` file providing a detailed description of the code files.
```bash
Posterior-Distributions-Proximity
├── LICENSE
├── README.md
├── code
│   ├── README.md
│   ├── data.py
│   ├── figs
│   ├── main.ipynb
│   ├── requirements.txt
│   ├── stuff.py
│   └── visualize.py
└──  paper
    ├── figs
    ├── main.pdf
    ├── main.tex
    ├── preamble.tex
    ├── references.bib
    ├── sn-jnl.cls
    └── sn-mathphys-num.bst
```
