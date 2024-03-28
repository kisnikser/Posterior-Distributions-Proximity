import numpy as np
from tqdm.auto import tqdm


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
                                    B: int = 100):
    """
    Calculate KL-divergences, s-scores and minimum eigvals for given dataset and prior parameters.
    
    Args:
        mu_0: np.ndarray - Prior mean.
        Sigma_0: np.ndarray - Prior covariance matrix.
        X: np.ndarray - Matrix objects-features.
        y: np.ndarray - Target vector.
        B: int = 100 - Number of iterations to get mean.
    
    Returns:
        divergences: np.ndarray - KL-divergences.
        scores: np.ndarray - s-scores.
        eigvals: np.ndarray - minimum eigenvalues for X^T X matrix.
    """

    divergences = []
    scores = []
    eigvals = []

    for _ in tqdm(range(B)):
        
        tmp_divergences = []
        tmp_scores = []
        tmp_eigvals = []
        k = X.shape[0] - 1
        X_kp1, y_kp1 = X, y
        mu_kp1, Sigma_kp1 = posterior_parameters(mu_0, Sigma_0, X_kp1, y_kp1)

        while k >= X.shape[1] + 1:
            idx = np.random.randint(k)
            X_k, y_k = np.delete(X_kp1, idx, axis=0), np.delete(y_kp1, idx, axis=0)
            mu_k, Sigma_k = posterior_parameters(mu_0, Sigma_0, X_k, y_k)
            tmp_divergences.append(KL(mu_k, Sigma_k, mu_kp1, Sigma_kp1))
            tmp_scores.append(s_score(mu_k, Sigma_k, mu_kp1, Sigma_kp1))
            tmp_eigvals.append(np.linalg.eigvalsh(X_k.T @ X_k)[0])
            X_kp1, y_kp1 = X_k, y_k
            mu_kp1, Sigma_kp1 = mu_k, Sigma_k
            k -= 1
            
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
    
    