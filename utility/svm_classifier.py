#!/usr/bin/env python

from sys import argv
from sklearn.svm import SVC

def svm_classify(X, y, pred = None, outfile='svm.txt'):

    '''

    This file requires sklearn's tokenizer + background tokenizer knowledge:

        - http://scikit-learn.org/stable/modules/feature_extraction.html
        - https://github.com/jeff1evesque/ist-652/files/2386056/PythonStartupTutorial-pt2.pdf

    @corpus, dict with the filename as the key, and the terms as a list of
        tokens in one long string.

    '''

    # fit svm
    clf = SVC()
    clf.fit(X,y)

    # predict
    if pred:
        clf.predict(pred)

if __name__ == '__main__':
    tfidf_transform(*argv[1:])
