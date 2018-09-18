#!/usr/bin/env python

import json
from sys import argv
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_transform(corpus, outfile='tfidf.json'):

    '''

    This file requires sklearn's tokenizer + background tokenizer knowledge:

        - http://scikit-learn.org/stable/modules/feature_extraction.html
        - https://github.com/jeff1evesque/ist-652/files/2386056/PythonStartupTutorial-pt2.pdf

    @corpus, dict with the filename as the key, and the terms as a list of
        tokens in one long string.

    '''

    with open(outfile, 'w') as txtfile:
        # initialize tokenizer
        myTfidf = TfidfVectorizer()

        # calculate tf-idf for each word
        myTfidf = TfidfVectorizer()
        myTfs = myTfidf.fit_transform(corpus)

        # report top 1000 article
        json.dump(myTfs, txtfile, indent=4)
        return(myTfs)

if __name__ == '__main__':
    tfidf_transform(*argv[1:])
