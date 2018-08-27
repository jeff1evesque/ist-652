#!/usr/bin/env python

import json
import requests
import wikipedia

def wikipedia_scraper(date, project='en.wikipedia.org', outfile='facebook.json'):
    '''

    This file uses the v1 wikipedia api:

        - https://wikimedia.org/api/rest_v1/#/
        - https://wikimedia.org/api/rest_v1/#!/Pageviews_data

    '''

    rest_v1 = 'https://wikimedia.org/api/rest_v1'
    result = []

    with open(outfile, 'w') as jsonfile:
        # scrape wikipedia api
        r = requests.get(
            '{}/metrics/pageviews/top/{}/all-access/{}'.format(
                rest_v1,
                project,
                date
            )
        )

        # write article to textfile
        for item in json.loads(r.text)['items'][0]['articles']:
            article = item['article']
            with open('data/wikipedia/articles/{}.txt'.format(article), 'w') as txtfile:
                txtfile.write(wikipedia.WikipediaPage(title=article).summary)

        # report top 1000 article
        json.dump(r.json(), jsonfile, indent=4)

        return(result)

if __name__ == '__main__':
    wikipedia_scraper(*argv[1:])
