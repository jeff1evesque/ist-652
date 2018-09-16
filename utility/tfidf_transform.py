#!/usr/bin/env python

import json
from sklearn.feature_extraction.text import TfidfVectorizer


def tfidf_transform(corpus, outfile='tfidf.json'):

    '''

    This file requires sklearn's tokenizer:

        - http://scikit-learn.org/stable/modules/feature_extraction.html

    '''

    with open(outfile, 'w') as jsonfile:
        # initialize tokenizer
        myTfidf = TfidfVectorizer()

        # calculate tf-idf for each word
        myTfs = myTfidf.fit_transform(corpus)

        # report top 1000 article
        json.dump(myTfs, jsonfile, indent=4)

if __name__ == '__main__':
    tdif_transform(*argv[1:])
