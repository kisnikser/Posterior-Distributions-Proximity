<div align="center">
<h1>Sample Size Determination: Posterior Distributions Proximity </h1>

[Nikita Kiselev](https://github.com/kisnikser)<sup>1 :email:</sup>, [Andrey Grabovoy](https://github.com/andriygav)<sup>1</sup>

<sup>1</sup> Moscow Institute of Physics and Technology

<sup>:email:</sup> Corresponding author

[📝 Paper](https://rdcu.be/d5x08), [</> Code](https://github.com/kisnikser/Posterior-Distributions-Proximity/tree/main/code), [🎬 Video](https://www.youtube.com/watch?v=WnIRaRl730A&t=1728s)

</div>

## 💡 Abstract
The issue of sample size determination is crucial for constructing an effective machine learning model. 
However, the existing methods for determining a sufficient sample size are either not strictly proven, or relate to the specific statistical hypothesis about the distribution of model parameters. 
In this paper we present two approaches based on the proximity of posterior distributions of model parameters on similar subsamples. 
We show that these two methods are valid for the model with normal posterior distribution of parameters. 
Computational experiments demonstrate the convergence of the proposed functions as the sample size increases.
We also compare the proposed methods with other approaches on different datasets.

## 🔎 Overview
<div align="center">
  <img alt="overview" src="https://github.com/kisnikser/Posterior-Distributions-Proximity/assets/70231416/1765dacb-a3f0-4be2-84c6-c997a0a22884">
</div>

## ⚖️ Comparison

### Size estimations for various sample sets
To compare our proposed methods with baselines, we used the following experiment setup. 

We have chosen 4 open-source datasets with regression task: 
- Boston,
- Diabetes,
- Forestfires,
- Servo.

We have applied 9 different baseline methods of sample size estimation on them: 
- Lagrange Multipliers Test,
- Likelihood Ratio Test,
- Wald Test,
- Cross Validation,
- Bootstrap,
- Average Posterior Variance Criterion (APVC),
- Average Coverage Criterion (ACC),
- Average Length Criterion (ALC),
- Utility function.
  
Default parameters values were used for this purpose.
All these methods were utilized with the help of [SampleSizeLib](https://github.com/andriygav/SampleSizeLib).

| Methods and sample sets | Boston | Diabetes | Forest Fires | Servo |
| --- | --- | --- | --- | --- |
| Lagrange Multipliers Test | 18 | 25 | 44 | 38 |
| Likelihood Ratio Test | 17 | 25 | 43 | 18 |
| Wald Test | 66 | 51 | 46 | 76 |
| Cross Validation | 178 | 441 | 171 | 120 |
| Bootstrap | 113 | 117 | 86 | 60 |
| APVC | 98 | 167 | 351 | 20 |
| ACC | 228 | 441 | 346 | 65 |
| ALC | 98 | 267 | 516 | 25 |
| Utility function | 148 | 172 | 206 | 105 |
| **KL (ours)** | **493** | **437** | **86** | **165** |
| **S (ours)** | **28** | **22** | **26** | **10** |

The results show that KL-divergence criterion is much more conservative, as it requires more sample size. 
In contrast, S-sufficiency tells us that an almost minimal number of objects in the sample is required. 

### Dependence of the sufficient sample size on available sample set
We have made a comprehensive analysis of the various sample size determination methods. 
We have analysed, how the sufficient sample size depends on the available sample set. 
Particularly, we increased the sample size, and calculated the sufficient one, based on the different methods. 

<div align="center">
  <img alt="overview" src="https://github.com/user-attachments/assets/83b8a68d-c41d-4601-bfc6-19ae2b13e29a">
</div>

- One can see that S-sufficient sample size is often the minimum one. <br>
  The reason lies in the fact that it was developed to compare different machine learning models, in particular for the case of uninformative distributions.
  This means that if the distributions have a large variance, then the proximity function will be close to one.
  Because of this, even with a small sample size, the criterion considers it sufficient.
- Also, the KL-sufficient sample size tends to require an almost total sample. <br>
  In our opinion, this is due to the fact that the Kullback-Leibler divergence is extremely sensitive to changes in the mean and variance of the distributions being compared. 
  Thus, the stabilization of the distance between them occurs quite late.

## 🛠️ Repository Structure
The repository is structured as follows:
- `paper`: This directory contains the main paper in PDF format (`main.pdf`) and the LaTeX source file (`main.tex`). Also there is a directory `figs` with images used in the paper.
- `code`: This directory contains the code used in the paper. It has its own `README.md` file providing a detailed description of the code files.
```shell
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

## 📚 Citation
```BibTeX
@article{kiselev2025ssdposterior,
  author = {Kiselev, Nikita and Grabovoy, Andrey},
  title = {Sample size determination: posterior distributions proximity},
  journal = {Computational Management Science},
  year = {2025},
  volume = {22},
  number = {1},
  pages = {1}
}
```
