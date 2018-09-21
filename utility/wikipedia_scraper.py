#!/usr/bin/env python

import re
import json
import requests
import wikipedia
from os import path
from sys import argv
from functools import reduce
from nltk.stem import PorterStemmer


def wikipedia_scraper(
    username,
    password,
    date,
    project='en.wikipedia.org',
    outfile='wikipedia.json',
    endpoint=False,
    port=8585,
    use_sample=False
):

    '''

    This file uses the v1 wikipedia api:

        - https://wikimedia.org/api/rest_v1/#/
        - https://wikimedia.org/api/rest_v1/#!/Pageviews_data

    '''

    # local variables
    sklearn_tfidf = {}
    search_count = {}
    ps = PorterStemmer()
    alpha_regex = '[^a-zA-Z]'
    rest_v1 = 'https://wikimedia.org/api/rest_v1'

    # use sample
    if use_sample:
        with open('data/2016-08-01--sample-train.json', 'r') as f:
            articles = json.load(f)['items'][0]['articles']
            articles = [a for a in articles if a['category'] != 'other']

    # scrape wikipedia api
    else:
        r = requests.get(
            '{}/metrics/pageviews/top/{}/all-access/{}'.format(
                rest_v1,
                project,
                date
            )
        )
        top1000 = r.json()
        articles = json.loads(r.text)['items'][0]['articles']

        # report top 1000 article
        with open(outfile, 'w') as jsonfile:
            json.dump(top1000, jsonfile, indent=4)

    # report article word count
    for item in articles:
        article = item['article']
        repls = {':': '--colon--', '/': '--fslash--'}
        filename = reduce(lambda a, kv: a.replace(*kv), repls.items(), article)
        filepath = 'data/wikipedia/articles/{}.txt'.format(filename)

        try:
            if not path.isfile(filepath):
                search_count[filename] = {}

                with open(filepath, 'w') as txtfile:
                    # article content
                    summary = wikipedia.WikipediaPage(title=article).summary
                    txtfile.write(summary)

                    #
                    # article word count
                    #
                    # @sklearn_tfidf, is required by the
                    #     TfidfVectorizer.fit_tranform.
                    #
                    words = summary.split()
                    for word in words:
                        stemmed = ps.stem(re.sub(alpha_regex, '', word).lower().strip())
                        if stemmed in search_count[filename]:
                            search_count[filename][stemmed] += 1
                        else:
                            search_count[filename][stemmed] = 1

        except wikipedia.exceptions.DisambiguationError as e:
            print('{} not valid, alternative titles: {}'.format(article, e.options))
        except wikipedia.exceptions.PageError as e:
            print('{} not valid: {}'.format(article, e))
        except OSError as e:
            print('not a valid article: {}'.format(e))
        except KeyError as e:
            print('{} not valid: {}'.format(article, e))

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
            if use_sample:
                filepath = 'data/wikipedia/train/frequency/{}.json'.format(
                    filename
                )
            else:
                filepath = 'data/wikipedia/frequency/{}.json'.format(
                    filename
                )

            with open(filepath, 'w') as f:
                json.dump(search_count, f)

    # return search count
    return({'search_count': search_count, 'articles': articles})

if __name__ == '__main__':
    wikipedia_scraper(*argv[1:])