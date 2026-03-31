from typing import List

import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso

from .watershed import *
from .similarity import *


def grade(similarity:float):
    ""
    if similarity > 1:
        raise ValueError("Similarity Should Be Less than 1!")
    elif similarity > 0.80:
        return 1 # 高度相似
    elif similarity > 0.60:
        return 2 # 大致相似
    else:
        return 3 # 不相似
grade = np.vectorize(grade)


class SimilarityModel:


    def __init__(self, similarity_S, similarity_H, scaler_S=None, scaler_H=None, full=True):
        """"""
        self.similarity_S = similarity_S
        self.similarity_H = similarity_H
        self.scaler_S = scaler_S
        self.scaler_H = scaler_H
        self.core = None
        self.full = full

    def _load_feature(self, datalist_1:List[Watershed], datalist_2:List[Watershed]):
        """"""
        X = []
        Y = []
        for example_1 in datalist_1:
            for example_2 in datalist_2:
                if self.scaler_S is None:
                    X.append(self.similarity_S(example_1.feature_S(self.full), example_2.feature_S(self.full)))
                else:
                    X.append(self.similarity_S(self.scaler_S.transform(example_1.feature_S(self.full).reshape(1, -1)).reshape(-1),
                                                self.scaler_S.transform(example_2.feature_S(self.full).reshape(1, -1)).reshape(-1)))
                if self.scaler_H is None:
                    Y.append(self.similarity_S(example_1.feature_H(), example_2.feature_H()))
                else:
                    Y.append(self.similarity_H(self.scaler_H.transform(example_1.feature_H().reshape(1, -1)).reshape(-1),
                                                self.scaler_H.transform(example_2.feature_H().reshape(1, -1)).reshape(-1)))
        return np.array(X), np.array(Y)


    def fit(self, train_set_1:List[Watershed], train_set_2:List[Watershed], alpha=None, R="Ridge"):
        """"""
        X, Y = self._load_feature(train_set_1, train_set_2)
        if alpha is None:
            self.core = LinearRegression().fit(X, Y)
        elif R == "Ridge":
            self.core = Ridge(alpha=alpha).fit(X, Y)
        elif R == "Lasso":
            self.core = Lasso(alpha=alpha).fit(X, Y)
        else:
            raise ValueError("Unknown Regularisation Type!")


    def predict(self, valid_set_1:List[Watershed], valid_set_2:List[Watershed]):
        """"""
        X, Y = self._load_feature(valid_set_1, valid_set_2)
        pred = self.core.predict(X)
        pred = np.minimum(pred, np.ones_like(pred))
        pred = np.maximum(pred, np.zeros_like(pred))
        return pred, Y


if __name__ == "__main__":

    pass
