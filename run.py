#!/usr/bin/env python

import os
import datetime
from config import hashtags
from sys import argv
from utility.twitter_scraper import twitter_scraper
from utility.wikipedia_scraper import wikipedia_scraper
from utility.nasdaq_scraper import nasdaq_scraper
from dateutil.relativedelta import relativedelta

def run(twitter=False, wikipedia=False, nasdaq=True):
    '''

    execute custom twitter, wikipedia, nasdaq scraping.

    '''

    prefix = 'data'
    types = ['twitter', 'wikipedia/articles', 'nasdaq']
    dirs = [prefix + '/' + type for type in types]

    today = datetime.date.today()
    before = datetime.date(2016, 8, 1)
    dates = []

    while before <= today:
        dates.append(datetime.datetime.strftime(before, '%Y/%m/01'))
        before += relativedelta(months=1)

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
            wikipedia_scraper(
                date,
                outfile='{}/{}--{}.json'.format(
                    'data/wikipedia',
                    date.replace('/', '-'),
                    datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                )
            )

    if nasdaq:
        nasdaq_scraper(today, outfile='data/nasdaq')

if __name__ == '__main__':
    run(*argv[1:])
