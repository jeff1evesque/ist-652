#!/usr/bin/env python

import json
from sys import argv
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_transform(corpus, outfile='tfidf.json'):

    '''

    This file requires sklearn's tokenizer + background tokenizer knowledge:

        - http://scikit-learn.org/stable/modules/feature_extraction.html
        - https://github.com/jeff1evesque/ist-652/files/2386056/PythonStartupTutorial-pt2.pdf

    @corpus, dict with the filename as the key, and the terms as a list of
        tokens in one long string.

    '''

    # initialize tokenizer
    myTfidf = TfidfVectorizer()

    # calculate tf-idf for each word
    myTfs = myTfidf.fit_transform(corpus)

    # report top 1000 article
    sparse.save_npz(outfile, myTfs)
    return(myTfs)

if __name__ == '__main__':
    tfidf_transform(*argv[1:])
