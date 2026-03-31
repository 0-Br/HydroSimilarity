import numpy as np


def quotient(feature_1:np.ndarray, feature_2:np.ndarray):
    """商形式"""
    return (np.minimum(feature_1, feature_2) + 1e-6) \
            / (np.maximum(feature_1, feature_2) + 1e-6)


def delta(feature_1:np.ndarray, feature_2:np.ndarray):
    """差形式"""
    return 1 - np.abs(feature_1 - feature_2)


def exponent(feature_1:np.ndarray, feature_2:np.ndarray):
    """指数形式"""
    return np.exp(-(feature_1 - feature_2) ** 2)


def quadratic(feature_1:np.ndarray, feature_2:np.ndarray):
    """距离形式"""
    return 1 - (feature_1 - feature_2) ** 2
