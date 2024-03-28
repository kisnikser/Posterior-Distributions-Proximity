import numpy as np
import scipy.stats as st
from matplotlib import pyplot as plt
from tqdm.auto import tqdm

myparams = {
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage{amsfonts}',
    'font.family': 'Djvu Serif',
    'font.size': 16,
    'axes.grid': True,
    'grid.alpha': 0.1,
    'lines.linewidth': 2
}
plt.rcParams.update(myparams)


def plot_eigvals(sample_sizes_synthetic, sample_sizes,
                 eigvals_synthetic, eigvals,
                 save=False, filename="eigvals.pdf"):

    fig, ax = plt.subplots(1, 2, figsize=(10, 4.5))

    ax[0].plot(sample_sizes_synthetic, eigvals_synthetic, label=r"$\lambda_{\min}(\mathbf{X}_k^\top \mathbf{X}_k)$")
    ax[0].plot(sample_sizes_synthetic, sample_sizes_synthetic ** 1/2, label=r"$\sqrt{k}$")
    ax[0].set_xlabel(r"$k$")
    ax[0].set_ylabel(r"$\lambda_{\min}(\mathbf{X}_k^\top \mathbf{X}_k)$")
    ax[0].set_title("Synthetic regression")
    ax[0].legend()

    ax[1].plot(sample_sizes, eigvals, label=r"$\lambda_{\min}(\mathbf{X}_k^\top \mathbf{X}_k)$")
    ax[1].plot(sample_sizes, 0.4 * sample_sizes ** 1/2, label=r"$\mathrm{const} \cdot \sqrt{k}$")
    ax[1].set_xlabel(r"$k$")
    ax[1].set_ylabel(r"$\lambda_{\min}(\mathbf{X}_k^\top \mathbf{X}_k)$")
    ax[1].set_title("Liver Disorders")
    ax[1].legend()

    plt.tight_layout()
    if save:
        plt.savefig(filename, bbox_inches="tight")
    plt.show()
    

def plot_divergences_scores(sample_sizes, divergences, scores,
                            save=False, filename="synthetic-regression.pdf"):
    
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    ax[0].plot(sample_sizes, divergences)
    ax[0].set_yscale("log")
    ax[0].set_ylabel(r"$KL(k)$")
    ax[0].set_xlabel(r"$k$")

    ax[1].plot(sample_sizes, scores)
    #ax[1][1].set_yscale('log')
    ax[1].set_ylabel(r"$S(k)$")
    ax[1].set_xlabel(r"$k$")
    ax[1].set_ylim(min(scores), 1)

    #plt.suptitle("Synthetic regression", fontsize=24)
    plt.tight_layout()
    if save:
        plt.savefig(filename, bbox_inches="tight")
    plt.show()
    
    
def plot_sufficient_vs_threshold(thresholds_synthetic,
                                 sufficient_synthetic,
                                 thresholds,
                                 sufficient,
                                 save=False, filename="sufficient-vs-threshold.pdf"):
    
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.5))

    ax[0].plot(thresholds_synthetic, sufficient_synthetic['kl-div'], label='KL-sufficient')
    ax[0].plot(thresholds_synthetic, sufficient_synthetic['s-score'], label='S-sufficient')
    ax[0].set_xscale('log')
    ax[0].set_xlabel(r"$\varepsilon$")
    ax[0].set_ylabel(r"$m^*$")
    ax[0].set_title("Synthetic regression")
    ax[0].legend()

    ax[1].plot(thresholds, sufficient['kl-div'], label='KL-sufficient')
    ax[1].plot(thresholds, sufficient['s-score'], label='S-sufficient')
    ax[1].set_xscale('log')
    ax[1].set_xlabel(r"$\varepsilon$")
    ax[1].set_ylabel(r"$m^*$")
    ax[1].set_title("Liver Disorders")
    ax[1].legend()

    plt.tight_layout()
    if save:
        plt.savefig(filename, bbox_inches="tight")
    plt.show()