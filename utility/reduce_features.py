#!/usr/bin/env python

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

def chi2(X, y, k=5):
    '''

    feature selection using chi-squared.

    '''

    X_new = SelectKBest(chi2, k=k).fit_transform(X, y)
    y_new = X.columns.values[selector.get_support()]

    return({'features': X_new, 'labels': y_new})
