#!/usr/bin/env python

from datetime import datetime
from utility import twitter_scraper

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

    if twitter:
        for tag in tags:
            twitter_scraper(
                tag,
                outfile='data/{}--{s}.json'.format(
                    datetime.now().strftime('%Y-%m-%d--%H-%M-%S'),
                    tag
                )
            )

if __name__ == '__main__':
    run()
