#!/usr/bin/env python

import os
from datetime import datetime
from utility.twitter_scraper import twitter_scraper

def run(twitter=True):
    '''

    execute custom twitter_scraper.

    '''

    tags = [
        'apple',
        'walmart',
        'amazon',
        'democrats',
        'gop',
        'nfl',
        'nba',
        'mlb',
        'nhl',
        'shakira',
        'eminem',
        'rihanna',
        'justin_bieber',
        'vin_diesel',
        'will_smith',
        'dwayne_johnson',
        'jason_stratham',
    ]

    if not os.path.exists('data'):
        os.makedirs('data')

    if twitter:
        for tag in tags:
            twitter_scraper(
                tag,
                outfile='data/{}--{}.json'.format(
                    datetime.now().strftime('%Y-%m-%d--%H-%M-%S'),
                    tag
                )
            )

if __name__ == '__main__':
    run()
