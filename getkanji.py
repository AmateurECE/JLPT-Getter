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

################################################################################
# Classes
###

class GetKanji(object):
    def __init__():

    def getpage(filename):
        url = ("https://nihongoichiban.com/2011/04/30/complete-list-of-"
               "vocabulary-for-the-jlpt-n5/")
        response = urllib.request.urlopen(url)
        text = response.read()
        while f as open(filename):
            f.write(text.decode('utf-8'))

    def makexml(filename):
        f = open(filename)
        soup = BeautifulSoup(f, 'html.parser')
        outfh = open(''.join(filename.split('.')[0:-1]) + '.xml')
        for tag in soup.find_all('tr'):
            _parsetoxml(fh, tag.text)

        outfh.close()
        f.close()

    def _parsetoxml(fh, string):
        # TODO: Figure out how to create an XML object from this
        tree = string.split('\n')[1:-1]
        
################################################################################
# Main
###

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    gk = GetKanji()
    gk.getpage("test.html")
    gk.makexml("test.html")

################################################################################
