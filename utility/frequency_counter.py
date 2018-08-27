#!/usr/bin/env python

import wikipedia

def frequency_counter(article, outdir):
    '''

    This file downloads the specified article, and returns another json file,
    containing the unique word distribution.

    '''

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    with open('{}/{}.txt'.format(outdir, article), 'w') as file:
        file.write(wikipedia.WikipediaPage(title=article).summary)

if __name__ == '__main__':
    frequency_counter(*argv[1:])
