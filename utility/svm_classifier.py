#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

def svm_fit(X, y, test=False):
    '''

    fit and return an svm model.

    '''

    # fit svm
    clf = SVC(probability=True)

    # train + test
    if test:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.33,
            random_state=42
        )

        # fit + predict
        clf.fit(X_train, y_train)
        pred = clf.predict(X_test)

        # error rate: computed with confusion matrix
        labels = clf.classes_

        # report: confusion matrix + error rate
        cm = confusion_matrix(y_test, pred, labels)
        error = 1-sum(np.diagonal(cm)/cm.sum())
        with open('{}/error.txt'.format(test), 'r') as txtfile:
            txtfile.writelines([
                '=================',
                'Confusion Matrix:',
                '=================',
                '',
                cm,
                '',
                '=================',
                'Error Rate:',
                '=================',
                error
            ])
        print(cm)
        print('error rate: {}'.format(error))

        # plot: confusion matrix
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(cm)
        plt.title('Confusion matrix of the classifier')
        fig.colorbar(cax)
        fig.savefig('{}/svm_confusion_matrix.png'.format(test))
        ax.set_xticklabels([''] + [str(i) for i in labels])
        ax.set_yticklabels([''] + [str(i) for i in labels])
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.show()

    # train
    else:
        clf.fit(X, y)

    return(clf)

def svm_predict(clf, pred, outfile='svm.txt'):
    '''

    predict using provided svm model.

    '''

    input = vec.transform(pred)
    result = clf.predict(input)
    with open(outfile, 'w') as txtfile:
        txtfile.write(result)
