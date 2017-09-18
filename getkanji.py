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

import os
import random
import sys
import getopt
import urllib.request
import locale
from bs4 import BeautifulSoup
import json

################################################################################
# Classes
###

class GetKanji(object):
    def __init__(self, filename, n):
        self.n = n
        self.filename = filename
        self.htmlfn = ''.join(filename.split('.')[0:-1]) + '.html'
        self.n5 = ("https://nihongoichiban.com/2011/04/30/complete-list-of-"
               "vocabulary-for-the-jlpt-n5/")

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
        response = None
        if self.n == 5:
            response = urllib.request.urlopen(self.n5)
        else:
            raise RuntimeError('List is not yet supported.')
        
        if response.getcode() != 200:
            raise RuntimeError(response.getcode())

        text = response.read()
        try:
            print('Filename: ', self.htmlfn)
            f = open(self.htmlfn, 'w')
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
            infh = open(self.htmlfn, 'r')
            outfh = open(self.filename, 'w')
            soup = BeautifulSoup(infh, 'html.parser')
            vocab = []
            fields = ['kanji', 'furigana', 'romaji', 'meaning', 'id', 'done']
            index = 0
            for tag in soup.find_all('tr'):
                li = tag.text.split('\n')[1:-1]
                li.append(index)
                li.append(False)
                vocab.append(dict(zip(fields, li)))
                index += 1

            json.dump(vocab[1:], outfh, ensure_ascii=False, indent='\t')
            outfh.close()
            infh.close()
            os.unlink(self.htmlfn)
        except OSError as e:
            raise

    def weeklyvocab(self):
        """
        weeklyvocab:
        Return a list of ten (tentative) vocab for the week.

        Args:
        	fh: An open readable filehandle.

        Returns:
        	A dict of vocab.

        Raises:
        	OSError: In the case of a bad filehandle.
                JSONDecodeError: In the case of a bad JSON file.
        """
        try:
            fh = open(self.filename, 'r')
            vocab = json.load(fh)
            fh.close()
            vlist = []
            while len(vlist) < 10:
                thisdict = vocab[random.randint(0, len(vocab) - 1)]
                if thisdict.get('done') == False:
                    thisdict['done'] = True
                    vlist.append(thisdict)
            fh = open(self.filename, 'w')
            json.dump(vocab, fh, ensure_ascii=False, indent='\t')
            fh.close()
            return vlist
        except OSError as o:
            raise
        except json.JSONDecodeError as j:
            raise

    def printvocab(self, vlist):
        """
        printvocab:
        Pretty-prints the vocab list for the week to STDOUT.

        Args:
        	vlist: The vocab list for the week.

        Returns:
        	none.

        Raises:
        	
        """
        formstr = '{:<20}{:^20}{:>20}'
        print(formstr.format('Meaning', 'Furigana', '\tKanji'))
        for entry in vlist:
            print(formstr.format(entry['meaning'],
                        entry['furigana'],
                        entry['kanji']))

################################################################################
# Main
###

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    usage = 'getkanji -n[1-5] [-g]'
    optlist, args = getopt.getopt(sys.argv[1:], 'n:g')

    g = False
    n = 0 # Bogus value to indicate error.
    for opt in optlist:
        if opt[0] == '-n':
            n = int(opt[1])
        elif opt[0] == '-g':
            g = True
    if n == 0:
        exit('Must specify a JLPT N level with the option -n\n' + usage)

    filename = 'jlptn' + str(n) + '.json'
    gk = GetKanji(filename, int(n))
    try:
        throwaway = open(filename, 'r')
        throwaway.close()
    except OSError as f:
        if not(g):
            exit('N' + n + ' file not found. Invoke with -g option to get.')
        else:
            try:
                print('Getting web page...')
                gk.getpage()
                print('Creating JSON File...')
                gk.makejson()
            except OSError as o:
                print('Error opening file: ', o)
            except RuntimeError as e:
                print('Server at nihongoichiban.com returned an error code: ',e)

    gk.printvocab(gk.weeklyvocab())

################################################################################
