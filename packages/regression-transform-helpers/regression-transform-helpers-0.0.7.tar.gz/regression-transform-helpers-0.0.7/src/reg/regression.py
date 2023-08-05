from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from numpy import expm1, log1p, clip
from scipy.stats import boxcox
from scipy.special import inv_boxcox

class RightUnskewedLinearRegression(LinearRegression):
    def predict(self, X):
        return expm1(super().predict(X))

    def fit(self, X, y, sample_weight=None):
        return super().fit(X, log1p(y), sample_weight=sample_weight)

class RightUnskewedRidgeCV(RidgeCV):
    def predict(self, X):
        return expm1(super().predict(X))

    def fit(self, X, y, sample_weight=None):
        return super().fit(X, log1p(y), sample_weight=sample_weight)

class RightUnskewedLassoCV(LassoCV):
    def predict(self, X):
        return expm1(super().predict(X))

    def fit(self, X, y, sample_weight=None):
        return super().fit(X, log1p(y), sample_weight=sample_weight)

class LeftUnskewedLinearRegression(LinearRegression):
    def predict(self, X):
        return clip(super().predict(X), 0, None) ** (1/3)

    def fit(self, X, y, sample_weight=None):
        return super().fit(X, y ** 3, sample_weight=sample_weight)

class LeftUnskewedRidgeCV(RidgeCV):
    def predict(self, X):
        return clip(super().predict(X), 0, None) ** (1/3)

    def fit(self, X, y, sample_weight=None):
        return super().fit(X, y ** 3, sample_weight=sample_weight)

class LeftUnskewedLassoCV(LassoCV):
    def predict(self, X):
        return clip(super().predict(X), 0, None) ** (1/3)

    def fit(self, X, y, sample_weight=None):
        return super().fit(X, y ** 3, sample_weight=sample_weight)

class BoxcoxedLinearRegression(LinearRegression):
    def __init__(self, *, fit_intercept=True, normalize="deprecated", copy_X=True, n_jobs=None, positive=False):
        super().__init__(fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, n_jobs=n_jobs, positive=positive)
        self.lmbda = None
    def predict(self, X):
        return inv_boxcox(super().predict(X), self.lmbda)
    def fit(self, X, y, sample_weight=None):
        y, self.lmbda = boxcox(y)
        return super().fit(X, y, sample_weight=sample_weight)
