#!/usr/bin/env python

import requests

def wikipedia_scraper(date, project='en.wikipedia.org', outfile='facebook.json'):
    '''

    This file uses the v1 wikipedia api:

        - https://wikimedia.org/api/rest_v1/#/
        - https://wikimedia.org/api/rest_v1/#!/Pageviews_data

    '''

    rest_v1 = 'https://wikimedia.org/api/rest_v1'
    with open(outfile, 'w') as file:
        r = requests.get(
            '{}/metrics/pageviews/top/{}/all-access/{}'.format(
                rest_v1,
                project,
                date
            )
        )

if __name__ == '__main__':
    wikipedia_scraper(*argv[1:])
