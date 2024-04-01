import numpy as np
import scipy.stats as st
from tqdm.auto import tqdm
from prettytable import PrettyTable

#!pip install ucimlrepo
from ucimlrepo import fetch_ucirepo
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer


def synthetic_regression(n_samples: int = 500,
                         n_features: int = 10,
                         mu_x: np.ndarray = None,
                         Sigma_x: np.ndarray = None,
                         alpha: float = 1,
                         sigma2: float = 1):
    """
    Generate synthetic regression dataset.
    We suppose x to be gaussian with parameters (mu_x, Sigma_x).
    Also we suppose w to be gaussian with parameters (0, alpha**(-1)*I).
    Target y is normal with guassian noise sigma2.
    
    Args:   
        n_samples: int = 500 - Number of samples.
        n_features: int = 10 - Number of features.
        mu_x: np.ndarray = None - Expectation of x normal distribution.
        Sigma_x: np.ndarray = None - Covariance matrix of x normal distribution.
        alpha: float = 1 - Scale of parameters normal distribution.
        sigma2: float = 1 - Target normal distribution variance.
        
    Returns:
        X: np.ndarray of shape (n_samples, n_features).
        y: np.ndarray of size n_samples.
    """

    if mu_x is None:
        mu_x = np.zeros(n_features)
    if Sigma_x is None:
        Sigma_x = np.identity(n_features)

    X = st.multivariate_normal(mean=mu_x, cov=Sigma_x).rvs(size=n_samples)
    w = st.multivariate_normal(mean=np.zeros(n_features), cov=alpha**(-1)*np.identity(n_features)).rvs(size=1)
    eps = st.multivariate_normal(mean=np.zeros(n_samples), cov=sigma2*np.identity(n_samples)).rvs(size=1)
    y = X @ w + eps
    
    return X, y


def liver_disorders():
    """
    Returns a preprocessed Liver Disorders dataset from UCI repository.
    """
    data = fetch_ucirepo(id=60) # Liver Disorders
    df = data.variables[['name', 'role', 'type']]
    target = df[df.role == 'Target'].name.values[0]
    columns = df[df.role == 'Feature'][['name', 'type']]
    num_columns = columns.loc[(columns.type == 'Continuous') | (columns.type == 'Integer')].name.values
    cat_columns = columns.loc[(columns.type == 'Categorical') | (columns.type == 'Binary')].name.values
    columns = columns.name.values

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_columns),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_columns)
        ]
    )

    df = data.data.original
    if data.metadata.has_missing_values:
        df = df.dropna(ignore_index=True)
    X = df.drop(columns=[target])
    X = preprocessor.fit_transform(X)
    y = df[target].to_numpy().flatten()
    
    return X, y


def get_datasets_regression():
    """
    Returns dict of preprocessed datasets with regression task from UCI repository.
    """
    datasets_regression_names = {
        1: 'Abalone',
        9: 'Auto MPG',
        10: 'Automobile',
        60: 'Liver Disorders',
        87: 'Servo',
        162: 'Forest Fires',
        186: 'Wine Quality',
        242: 'Energy Efficiency',
        320: 'Student Performance',
        368: 'Facebook Metrics',
        477: 'Real Estate Valuation',
        519: 'Heart Failure Clinical Records',
        565: 'Bone marrow transplant: children',
    }

    datasets_regression = {}
    
    for idx, name in tqdm(datasets_regression_names.items()):
    
        data = fetch_ucirepo(id=idx)
        df = data.variables[['name', 'role', 'type']]
        #print(name)
        target = df[df.role == 'Target'].name.values[0]
        columns = df[df.role == 'Feature'][['name', 'type']]
        num_columns = columns.loc[(columns.type == 'Continuous') | (columns.type == 'Integer')].name.values
        cat_columns = columns.loc[(columns.type == 'Categorical') | (columns.type == 'Binary')].name.values
        columns = columns.name.values

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), num_columns),
                ('cat', OneHotEncoder(handle_unknown='ignore'), cat_columns)
            ]
        )

        df = data.data.original
        if data.metadata.has_missing_values:
            df = df.dropna(ignore_index=True)
        X = df.drop(columns=[target])
        X = preprocessor.fit_transform(X)
        y = df[target].to_numpy().flatten()
        
        datasets_regression[name] = (X, y)
        
    return datasets_regression, datasets_regression_names


def get_datasets_regression_info():
    """
    Returns dict of the info about preprocessed datasets with regression task from UCI repository.
    """
    datasets_regression_names = {
        1: 'Abalone',
        9: 'Auto MPG',
        10: 'Automobile',
        60: 'Liver Disorders',
        87: 'Servo',
        162: 'Forest Fires',
        186: 'Wine Quality',
        242: 'Energy Efficiency',
        320: 'Student Performance',
        368: 'Facebook Metrics',
        477: 'Real Estate Valuation',
        519: 'Heart Failure Clinical Records',
        565: 'Bone marrow transplant: children',
    }
    
    table = PrettyTable()
    table.field_names = ["Dataset", "# objects", "# features"]
    
    for idx, name in tqdm(datasets_regression_names.items()):
        data = fetch_ucirepo(id=idx) # Liver Disorders
        df = data.data.original
        if data.metadata.has_missing_values:
            df = df.dropna(ignore_index=True)
        table.add_row([name, df.shape[0], df.shape[1] - 1])
        
    return table
        