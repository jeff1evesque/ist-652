#!/usr/bin/env python

import os
import datetime
from config import tags
from sys import argv
from utility.twitter_scraper import twitter_scraper
from utility.wikipedia_scraper import wikipedia_scraper
from dateutil.relativedelta import relativedelta

def run(twitter=True, wikipedia=True):
    '''

    execute custom twitter_scraper.

    '''

    prefix = 'data'
    types = ['twitter', 'wikipedia']
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
        for tag in tags:
            twitter_scraper(
                tag,
                outfile='{}/{}--{}.json'.format(
                    'data/twitter',
                    tag,
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

if __name__ == '__main__':
    run(*argv[1:])
