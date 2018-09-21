#!/usr/bin/env python

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

def chi_squared(X, y, k=5):
    '''

    feature reduction using chi-squared.

    '''

    ch2 = SelectKBest(chi2, k=k)
    X_new = ch2.fit_transform(X, y)

    return(X_new)
