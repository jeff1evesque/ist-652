#!/usr/bin/env python

import json
import requests
from sys import argv
from twitterscraper import query_tweets
from config import endpoint, port, username, password

def twitter_scraper(query, quantity=10, outfile='twitter.json'):
    '''

    @query, may contain the following pattern:

        'happy hour' -> Finds tweets: containing the exact phrase 'happy hour'.

        'love OR hate' -> Finds tweets: containing either 'love' or 'hate' (or both).

        'beer -root' -> Finds tweets: containing 'beer' but not 'root.'

        '#haiku' -> Finds tweets: containing the hashtag 'haiku.'

        'from:alexiskold' -> Finds tweets: sent from person 'alexiskold.'

        'to:techcrunch' -> Finds tweets: sent to person 'techcrunch.'

        '@mashable' -> Finds tweets: Referencing person 'mashable.'

        '"happy hour" near:"san francisco"' -> Finds tweets: containing the exact phrase 'happy hour' and sent near 'san francisco.'

        'near:NYC within:15mi' -> Finds tweets: sent within 15 miles of 'NYC.'

        'superhero since:2010-12-27' -> Finds tweets: containing 'superhero' and sent since date '2010-12-27' (year-month-day).

        'ftw until:2010-12-27' -> Finds tweets: containing 'ftw' and sent up to date '2010-12-27.'

        'movie -scary :)' -> Finds tweets: containing 'movie', but not 'scary,' and with a positive attitude.

        'flight :(' -> Finds tweets: containing 'flight' and with a negative attitude.

        'traffic ?' -> Finds tweets: containing 'traffic' and asking a question.

        'hilarious filter:links' -> Finds tweets: containing 'hilarious' and linking to URLs.

        'news source:twitterfeed' -> Finds tweets: containing 'news' and entered via TwitterFeed

    Note: any advanced query supported by https://twitter.com/search-advanced?lang=en,
          can be implemented by the 'query_tweets' function.

    '''

    # local variables
    tweets = []

    # structure tweets
    for tweet in query_tweets(query, int(quantity)):
        tweets.append({
            'text': tweet.text,
            'likes': tweet.likes,
            'retweets': tweet.retweets,
            'replies': tweet.replies,
            'user': tweet.user,
            'timestamp': str(tweet.timestamp)
        })

    # write to file
    if len(tweets):
        with open(outfile, 'w') as file:
            json.dump(tweets, file, indent=4)

if __name__ == '__main__':
    twitter_scraper(*argv[1:])
