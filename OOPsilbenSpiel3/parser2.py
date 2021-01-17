import wiktionary_de_parser
from wiktionary_de_parser import Parser
import copy_parser_class
from copy_parser_class import Parser2
import random
from lxml import etree
from importlib.machinery import SourceFileLoader
import os
import re

file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'

def get_bank():
    listesilben = []
    for record in Parser(file_path):
        #if record.has_key('syllables'): # has_key was removed from py3
        if 'syllables' in record:
            print(record['syllables'])
        listesilben.append(record['syllables'])
        if len(listesilben) == 1000:
             break


#def secondthousand(): #non iterable


