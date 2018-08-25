#!/usr/bin/env python

import os
from datetime import datetime
from utility.twitter_scraper import twitter_scraper

def run(twitter=True):
    '''

    execute custom twitter_scraper.

    '''

    twitter_dir = 'data/twitter'
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

    if not os.path.exists(twitter_dir):
        os.makedirs(twitter_dir)

    if twitter:
        for tag in tags:
            twitter_scraper(
                tag,
                outfile='{}/{}--{}.json'.format(
                    twitter_dir,
                    tag,
                    datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
                )
            )

if __name__ == '__main__':
    run()
