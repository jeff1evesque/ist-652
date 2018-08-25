#!/usr/bin/env python

import os
from datetime import datetime
from utility.twitter_scraper import twitter_scraper
import fb_scrape_public as fsp
import config

def run(twitter=True, facebook=True):
    '''

    execute custom twitter_scraper.

    '''

    base_dir = 'data'
    fb_token = config.token
    twitter_dir = '{}/twitter'.format(base_dir)
    facebook_dir = '{}/facebook'.format(base_dir)

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
                    datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                )
            )

    if facebook:
        for tag in tags:
            fsp.scrape_fb(
                token=fb_token,
                ids=tag,
                outfile='{}/{}--{}.json'.format(
                    facebook_dir,
                    tag,
                    datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
                )

if __name__ == '__main__':
    run()
