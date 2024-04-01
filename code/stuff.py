import numpy as np
from tqdm.auto import tqdm
from prettytable import PrettyTable


def posterior_parameters(mu_0, Sigma_0, X, y, sigma2=1):
    """Calculate posterior parameters in the Linear Regression model with normal prior."""
    Sigma = np.linalg.inv(np.linalg.inv(Sigma_0) + 1 / sigma2 * X.T @ X)
    mu = Sigma @ (1 / sigma2 * X.T @ y + np.linalg.inv(Sigma_0) @ mu_0)
    return mu, Sigma


def KL(mu_k, Sigma_k, mu_kp1, Sigma_kp1):
    """Calculate Kullback-Leibler divergence between two gaussians."""
    return (
        1
        / 2
        * (
            np.trace(np.linalg.inv(Sigma_kp1) @ Sigma_k)
            + (mu_kp1 - mu_k) @ np.linalg.inv(Sigma_kp1) @ (mu_kp1 - mu_k)
            - mu_k.size
            + np.log(np.linalg.det(Sigma_kp1) / np.linalg.det(Sigma_k))
        )
    )


def s_score(mu_k, Sigma_k, mu_kp1, Sigma_kp1):
    """Calculate s-score function between two gaussians."""
    return np.exp(
        -1 / 2
        * ((mu_kp1 - mu_k) @ np.linalg.inv(Sigma_k + Sigma_kp1) @ (mu_kp1 - mu_k))
    )


def get_divergences_scores_eigvals(mu_0: np.ndarray,
                                    Sigma_0: np.ndarray,
                                    X: np.ndarray,
                                    y: np.ndarray,
                                    B: int = 100,
                                    num_sample_size: int = None):
    """
    Calculate KL-divergences, s-scores and minimum eigvals for given dataset and prior parameters.
    
    Args:
        mu_0: np.ndarray - Prior mean.
        Sigma_0: np.ndarray - Prior covariance matrix.
        X: np.ndarray - Matrix objects-features.
        y: np.ndarray - Target vector.
        B: int = 100 - Number of iterations to get mean.
        num_sample_sizes: int = None - Number of sample sizes to use (for computational simplicity)
        
    Returns:
        divergences: np.ndarray - KL-divergences.
        scores: np.ndarray - s-scores.
        eigvals: np.ndarray - minimum eigenvalues for X^T X matrix.
    """

    divergences = []
    scores = []
    eigvals = []
    
    if num_sample_size is None:
        sample_sizes = np.arange(X.shape[1]+1, X.shape[0]+1)[::-1]
    else:
        if X.shape[0] - X.shape[1] < num_sample_size:
            sample_sizes = np.arange(X.shape[1]+1, X.shape[0]+1)[::-1]
        else:
            sample_sizes = np.linspace(X.shape[1]+1, X.shape[0], num_sample_size, dtype=int)[::-1]

    for _ in tqdm(range(B)):
        
        tmp_divergences = []
        tmp_scores = []
        tmp_eigvals = []
        X_kp1, y_kp1 = X, y
        mu_kp1, Sigma_kp1 = posterior_parameters(mu_0, Sigma_0, X_kp1, y_kp1)

        for i in range(1, len(sample_sizes)):
            idx = np.random.randint(sample_sizes[i])
            X_k, y_k = np.delete(X_kp1, idx, axis=0), np.delete(y_kp1, idx, axis=0)
            mu_k, Sigma_k = posterior_parameters(mu_0, Sigma_0, X_k, y_k)
            tmp_divergences.append(KL(mu_k, Sigma_k, mu_kp1, Sigma_kp1))
            tmp_scores.append(s_score(mu_k, Sigma_k, mu_kp1, Sigma_kp1))
            tmp_eigvals.append(np.linalg.eigvalsh(X_k.T @ X_k)[0])
            X_kp1, y_kp1 = X_k, y_k
            mu_kp1, Sigma_kp1 = mu_k, Sigma_k
            
        divergences.append(tmp_divergences)
        scores.append(tmp_scores)
        eigvals.append(tmp_eigvals)
        
    divergences = np.mean(divergences, axis=0)[::-1]
    scores = np.mean(scores, axis=0)[::-1]
    eigvals = np.mean(eigvals, axis=0)[::-1]
    
    return divergences, scores, eigvals


def sufficient_sample_size(sample_sizes: np.ndarray,
                           divergences: np.ndarray = None,
                           scores: np.ndarray = None,
                           eps=1e-4, 
                           method="kl-div"):
    """
    Calculate sufficient sample size. Use method with threshold eps.
    """
    
    if method not in ["kl-div", "s-score"]:
        raise NotImplementedError

    if method == 'kl_div' and divergences is None:
        return ValueError
    
    if method == 's-score' and scores is None:
        return ValueError

    m_star = np.inf
        
    if method == "kl-div":
        for k, div in zip(sample_sizes, divergences):
            if div <= eps and m_star == np.inf:
                m_star = k
            elif div > eps:
                m_star = np.inf
        
    elif method == "s-score":
        for k, score in zip(sample_sizes, scores):
            if score >= 1 - eps and m_star == np.inf:
                m_star = k
            elif score < 1 - eps:
                m_star = np.inf
        
    return m_star


def sufficient_vs_threshold(sample_sizes: np.ndarray,
                            divergences: np.ndarray,
                            scores: np.ndarray,
                            thresholds: np.ndarray):
    """
    Calculate sufficient sample sizes for each eps in thresholds.
    """
    sufficient = {'kl-div': [],
                  's-score': []}
    
    for method in ['kl-div', 's-score']:
        for eps in thresholds:
            sufficient[method].append(sufficient_sample_size(sample_sizes=sample_sizes,
                                                            divergences=divergences,
                                                            scores=scores,
                                                            eps=eps,
                                                            method=method))
    
    return sufficient
    
    
def get_regression_results(eps: float, 
                           num_sample_size: int = 50,
                           datasets_regression=None,
                           datasets_regression_names=None,
                           divergences_regression=None,
                           scores_regression=None):
    """Return table with sufficient sample size determination results on different datasets."""

    table = PrettyTable()
    table.field_names = ["Dataset", "KL-sufficient", "S-sufficient"]
    for name in datasets_regression_names.values():
        
        X = datasets_regression[name][0]
        if X.shape[0] - X.shape[1] < num_sample_size:
            sample_sizes = np.arange(X.shape[0]+1, X.shape[0])
        else:
            sample_sizes = np.linspace(X.shape[1]+1, X.shape[0], num_sample_size, dtype=int)
        
        kl_sufficient = sufficient_sample_size(sample_sizes=sample_sizes,
                                                divergences=divergences_regression[name],
                                                scores=scores_regression[name],
                                                eps=eps,
                                                method='kl-div')
        s_sufficient = sufficient_sample_size(sample_sizes=sample_sizes,
                                                divergences=divergences_regression[name],
                                                scores=scores_regression[name],
                                                eps=eps,
                                                method='s-score')
        table.add_row([name, kl_sufficient, s_sufficient])
    
    return table