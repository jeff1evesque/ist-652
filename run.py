#!/usr/bin/env python

import os
import datetime
from sys import argv
from config import username, password, hashtags, endpoint, port, hashtags
from utility.twitter_scraper import twitter_scraper
from utility.wikipedia_scraper import wikipedia_scraper
from utility.tfidf_transform import tfidf_transform
from utility.svm_classifier import svm_fit, svm_predict
from utility.reduce_features import chi_squared
from dateutil.relativedelta import relativedelta

def run(twitter=True, wikipedia=True):
    '''

    execute custom twitter + wikipedia scraping.

    '''

    prefix = 'data'
    types = [
        'twitter',
        'wikipedia/test',
        'wikipedia/articles',
        'wikipedia/popular',
        'wikipedia/frequency',
        'wikipedia/tfidf',
        'wikipedia/train/articles',
        'wikipedia/train/popular',
        'wikipedia/train/frequency',
        'wikipedia/train/tfidf',
        'wikipedia/prediction',
    ]
    dirs = [prefix + '/' + type for type in types]

    today = datetime.date.today()
    current = datetime.date(2016, 8, 1)
    dates = []

    while current <= today:
        dates.append(datetime.datetime.strftime(current, '%Y/%m/01'))
        current += relativedelta(months=1)

    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

    if twitter:
        for hashtag in hashtags:
            twitter_scraper(
                hashtag,
                outfile='{}/{}--{}.json'.format(
                    'data/twitter',
                    hashtag,
                    datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                )
            )

    if wikipedia:
        for date in dates:
            # return word frequency: top 1000 articles per date
            word_frequency = wikipedia_scraper(
                username=username,
                password=password,
                date=date,
                outfile='{}/{}--{}.json'.format(
                    'data/wikipedia/popular',
                    date.replace('/', '-'),
                    datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                )
            )

            # vectorize + apply tfidf
            tfidf = tfidf_transform(
                word_frequency,
                outfile='{}/{}--{}'.format(
                    'data/wikipedia/tfidf',
                    date.replace('/', '-'),
                    datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                ),
            )

        # train dataset: use first month instance
        for date in dates[0:1]:
            # return word frequency: top 1000 articles per date
            word_frequency = wikipedia_scraper(
                username=username,
                password=password,
                date=date,
                outfile='{}/{}--{}.json'.format(
                    'data/wikipedia/train/popular',
                    date.replace('/', '-'),
                    datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                ),
                use_sample=True
            )

            # vectorize + apply tfidf
            tfidf = tfidf_transform(
                word_frequency['search_count'],
                outfile='{}/{}--{}'.format(
                    'data/wikipedia/train/tfidf',
                    date.replace('/', '-'),
                    datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                ),
            )

        # data
        X = tfidf
        y = [a['category'] for a in word_frequency['articles']]

        #
        # generate svm
        #
        # @test, provides basepath to store the confusion matrix, and
        #     erro rate results.
        #
        svm_fit(X, y, test='data/wikipedia/test')

        #
        # generate svm: iterative feature reduction
        #
        # @test, provides basepath to store the confusion matrix, and
        #     erro rate results.
        #
        features = [10, 25, 50]
        for num in features:
            selected = chi_squared(X, y, k=num)
            svm = svm_fit(
                selected['features'],
                selected['labels'],
                test='data/wikipedia/test',
                suffix=num
            )

#        # svm prediction
#        svm_predict(
#            clf,
#            outfile='{}/svm--{}.json'.format(
#                'data/wikipedia/prediction',
#                datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
#            )
#        )

if __name__ == '__main__':
    run(*argv[1:])
