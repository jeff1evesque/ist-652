#!/usr/bin/env python

import re
import json
import requests
import wikipedia
from os import path
from functools import reduce
from nltk.stem import PorterStemmer


def wikipedia_scraper(
    username,
    password,
    date,
    project='en.wikipedia.org',
    outfile='wikipedia.json',
    endpoint=False,
    port=8585
):

    '''

    This file uses the v1 wikipedia api:

        - https://wikimedia.org/api/rest_v1/#/
        - https://wikimedia.org/api/rest_v1/#!/Pageviews_data

    '''

    search_count = {}
    regex = re.compile('[^a-zA-Z]')
    rest_v1 = 'https://wikimedia.org/api/rest_v1'
    ps = PorterStemmer()

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
            filename = reduce(lambda a, kv: a.replace(*kv), repls.items(), article)
            filepath = 'data/wikipedia/articles/{}.txt'.format(filename)

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

            # article word count
            words = article.split()
            for word in words:
                word = regex.sub('', ps.stem(word)).lower()
                if word in search_counts:
                    search_count[word] += 1
                else:
                    search_count[word] = 1

            #
            # word frequency: each word will contain a frequency count, used for
            #     sentiment related analysis. The corresponding 'load_data', and
            #     'login' endpoint documentation, can be reviewed:
            #
            #     - https://jeff1evesque.github.io/machine-learning.docs/latest
            #
            # Note: /registration is required for the supplied username + password
            #
            if endpoint:
                # get access token
                login = requests.post(
                    'https://{}:{}/login'.format(endpoint, port),
                    headers={'Content-Type': 'application/json'},
                    data={'user[login]': username, 'user[password]': password}
                )
                token = login.json['access_token']

                # data into payload
                payload = {
                    'properties': {
                        'session_name': filename,
                        'collection': 'ist-652-wikipedia',
                        'dataset_type': 'file_upload',
                        'session_type': 'data_append',
                        'model_type': 'svm',
                        'stream': 'True'
                    },
                    'dataset': [search_count]
                }

                # send data
                endpoint = 'https://{}:{}/load-data'.format(endpoint, port)
                headers = {
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                }

                requests.post(endpoint, headers=headers, data=json.dumps(payload))

            else:
                with open('data/wikipedia/word_frequency.json', 'w') as f:
                    json.dump(payload, f)

        # report top 1000 article
        json.dump(r.json(), jsonfile, indent=4)

if __name__ == '__main__':
    wikipedia_scraper(*argv[1:])
