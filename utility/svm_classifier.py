#!/usr/bin/env python

from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

def svm_fit(X, y):
    '''

    fit and return an svm model.

    '''

    # fit svm
    clf = SVC(probability=True)
    clf.fit(X,y)
    return(clf)

def svm_predict(clf, pred, outfile='svm.txt'):
    '''

    predict using provided svm model.

    '''

    input = vec.transform(pred)
    result = clf.predict(input)
    with open(outfile, 'w') as txtfile:
        txtfile.write(result)
