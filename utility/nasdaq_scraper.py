#!/usr/bin/env python

import time
import urllib.request
from dateutil.relativedelta import relativedelta

def nasdaq_scraper(date, years='5', delta='1mo', outfile='nasdaq.json'):
    '''

    This file downloads historical nasdaq data:

        - https://finance.yahoo.com/quote/%5EIXIC/history

    '''

    base_url = 'https://query1.finance.yahoo.com/v7/finance/download'
    pattern = '%Y/%m/%d'
    period1 = int(time.mktime(time.strptime(str(date - relativedelta(years=years)), pattern)))
    period2 = int(time.mktime(time.strptime(str(date), pattern)))

    # scrape wikipedia api
    urllib.request.urlretrieve(
        '{}/%5EIXIC/history?period1={}&period2={}&interval={}&events=history&crumb=Ajh2eBQLgdL'.format(
            base_url,
            period1,
            period2,
            delta
        ), outfile
    )

if __name__ == '__main__':
    nasdaq_scraper(*argv[1:])
