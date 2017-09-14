#!/usr/bin/env python3
################################################################################
# NAME:		    getkanji.py
#
# AUTHOR:	    Ethan D. Twardy
#
# DESCRIPTION:	    This file downloads the JLPT Kanji list and parses it into
#                   XML.
#
# CREATED:	    09/13/2017
#
# LAST EDITED:	    09/13/2017
###

################################################################################
# Imports
###

import urllib.request
import locale
from bs4 import BeautifulSoup
import json

################################################################################
# Classes
###

class GetKanji(object):
    def __init__(self, filename):
        self.filename = filename


    def getpage(self):
        """
        getpage:
        Get the webpage that contains the JLPT Vocab list

        Args:
        	None.

        Returns:
        	None.

        Raises:
        	RuntimeError: If getting the page is unsuccessful
                OSError: If there is an error in open().
        """
        url = ("https://nihongoichiban.com/2011/04/30/complete-list-of-"
               "vocabulary-for-the-jlpt-n5/")
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            raise RuntimeError(response.getcode())

        text = response.read()
        try:
            print('Filename: ', self.filename)
            f = open(self.filename, 'w')
            f.write(text.decode('utf-8'))
            f.close()
        except OSError as e:
            raise
        response.close()

    def makejson(self):
        """
        makejson:
        Prints the vocab words to a JSON file.

        Args:
        	None.

        Returns:
        	None.

        Raises:
        	OSError: If there is an issue in open()
        """
        try:
            infh = open(self.filename, 'r')
            outfh = open(''.join(self.filename.split('.')[0:-1]) + '.json', 'w')
            soup = BeautifulSoup(infh, 'html.parser')
            vocab = []
            fields = ['kanji', 'furigana', 'romaji', 'meaning']
            for tag in soup.find_all('tr'):
                li = tag.text.split('\n')[1:-1]
                vocab.append(dict(zip(fields, li)))

            json.dump(vocab, outfh, ensure_ascii=False, indent='\t')
            outfh.close()
            infh.close()
        except OSError as e:
            raise

################################################################################
# Main
###

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    gk = GetKanji('test.html')
    try:
        print('Getting web page...')
        gk.getpage()
        print('Creating JSON File...')
        gk.makejson()
    except OSError as o:
        print('Error opening file: ', o)
    except RuntimeError as e:
        print('Server at nihongoichiban.com returned an error code: ', e)

################################################################################
