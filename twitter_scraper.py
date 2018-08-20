#
# twitter_scraper.py
#
# Note: the following modules are required:
#
#     sudo apt-get install -y python-lxml
#     sudo pip install twitterscraper
#
from twitterscraper import query_tweets

def twitter_scraper(hashtag):
    '''

    @hashtag, may contain queries in the following pattern

        'happy hour' -> Finds tweets: containing the exact phrase 'happy hour.'

        'love OR hate' -> Finds tweets: containing either 'love' or 'hate' (or both).

        'beer -root' -> Finds tweets: containing 'beer' but not 'root.'

        '#haiku' -> Finds tweets: containing the hashtag 'haiku.'

        'from:alexiskold' -> Finds tweets: sent from person 'alexiskold.'

        'to:techcrunch' -> Finds tweets: sent to person 'techcrunch.'

        '@mashable' -> Finds tweets: Referencing person 'mashable.'

        ''happy hour' near:'san francisco'' -> Finds tweets: containing the exact phrase 'happy hour' and sent near 'san francisco.'

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

    with open('output.txt', 'a') as f:

        for tweet in query_tweets(hashtag, 10):
            f.write('text: {}, likes: {}'.format(repr(tweet.text), repr(tweet.likes)))
        file.close()

if __name__ == '__main__':
    twitter_scraper()
