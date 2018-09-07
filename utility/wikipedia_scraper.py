#!/usr/bin/env python

import json
import requests
import wikipedia
from os import path
from functools import reduce

def wikipedia_scraper(date, project='en.wikipedia.org', outfile='facebook.json', endpoint=False):
    '''

    This file uses the v1 wikipedia api:

        - https://wikimedia.org/api/rest_v1/#/
        - https://wikimedia.org/api/rest_v1/#!/Pageviews_data

    '''

    rest_v1 = 'https://wikimedia.org/api/rest_v1'

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
            repls = {':': '--colon--', '/': '--fslash--'}
            article_filename = reduce(lambda a, kv: a.replace(*kv), repls.items(), article)
            filepath = 'data/wikipedia/articles/{}.txt'.format(article_filename)

            try:
                if not path.isfile(filepath):
                    with open(filepath, 'w') as txtfile:
                        txtfile.write(wikipedia.WikipediaPage(title=article).summary)
            except wikipedia.exceptions.DisambiguationError as e:
                print('{} not valid, alternative titles: {}'.format(article, e.options))
            except wikipedia.exceptions.PageError as e:
                print('{} not valid: {}'.format(article, e))
            except OSError as e:
                print('not a valid article: {}'.format(e))
            except KeyError as e:
                print('{} not valid: {}'.format(article, e))

        # report top 1000 article
        json.dump(r.json(), jsonfile, indent=4)

        #
        # send to endpoint: load_data, and login documentation can be reviewed:
        #
        #     - https://jeff1evesque.github.io/machine-learning.docs/latest
        #
        # Note: /registration is required for the supplied username + password
        #
        if endpoint:
            # get access token
            login = client.post(
                'https://{}:{}/login'.format(endpoint, port),
                headers={'Content-Type': 'application/json'},
                data={'user[login]': username, 'user[password]': password}
            )
            token = login.json['access_token']

            # send data
            endpoint = 'https://{}:{}/load-data'.format(endpoint, port)
            headers = {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            }

            requests.post(endpoint, headers=headers, data=json.dumps(r.json))

if __name__ == '__main__':
    wikipedia_scraper(*argv[1:])
