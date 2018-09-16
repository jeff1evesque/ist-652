#!/usr/bin/env python

import os
import datetime
from sys import argv
from config import username, password, hashtags, endpoint, port, hashtags
from utility.twitter_scraper import twitter_scraper
from utility.wikipedia_scraper import wikipedia_scraper
from utility.tfidf_transform import tfidf_transform
from dateutil.relativedelta import relativedelta

def run(twitter=True, wikipedia=True):
    '''

    execute custom twitter + wikipedia scraping.

    '''

    prefix = 'data'
    types = [
        'twitter',
        'wikipedia/articles',
        'wikipedia/popular',
        'wikipedia/frequency',
        'wikipedia/tfidf',
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
            word_frequency = append(
                wikipedia_scraper(
                    username=username,
                    password=password,
                    date=date,
                    outfile='{}/{}--{}.json'.format(
                        'data/wikipedia/popular',
                        date.replace('/', '-'),
                        datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                    ),
                    endpoint=endpoint,
                    port=port
                }
            )

            # vectorize + apply tfidf
            tfidf_transform(
                word_frequency,
                outfile='{}/{}--{}.json'.format(
                    'data/wikipedia/tfidf',
                    date.replace('/', '-'),
                    datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                ),
            )

if __name__ == '__main__':
    run(*argv[1:])
