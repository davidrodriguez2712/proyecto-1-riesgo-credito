from sklearn.base import BaseEstimator, TransformerMixin

class MissingIndicatorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y= None):
        return self
    
    def transform(self, X):
        X = X.copy()
        
        for i in self.columns:
            X[f'{i}_missing'] = X[i].isna().astype(int)
        
        return X