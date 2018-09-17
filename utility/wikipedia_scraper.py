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
    alpha_regex = '[^a-zA-Z]'
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
            search_count[filename] = {}
            filepath = 'data/wikipedia/articles/{}.txt'.format(filename)

            # write to file
            try:
                if not path.isfile(filepath):
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
                        sklearn_tfidf = {}
                        words = summary.split()
                        for word in words:
                            sklearn_tfidf[filename] = ' '.join(word)

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
                filepath = 'data/wikipedia/frequency/{}.json'.format(
                    filename
                )
                with open(filepath, 'w') as f:
                    json.dump(search_count, f)

        # report top 1000 article
        json.dump(r.json(), jsonfile, indent=4)

        # return concatenated tfidf
        return(sklearn_tfidf)

if __name__ == '__main__':
    wikipedia_scraper(*argv[1:])
