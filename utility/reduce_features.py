#!/usr/bin/env python

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

def chi_squared(X, y, k=5):
    '''

    feature selection using chi-squared.

    '''

    ch2 = SelectKBest(chi2, k=k)
    X_new = ch2.fit_transform(X, y)
    y_new = [feature_names[i] for i in ch2.get_support(indices=True)]

    return({'features': X_new, 'labels': y_new})
