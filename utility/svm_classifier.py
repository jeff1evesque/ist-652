#!/usr/bin/env python

from sklearn.svm import SVC

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

    result = clf.predict(pred)
    with open(outfile, 'w') as txtfile:
        txtfile.write(result)
