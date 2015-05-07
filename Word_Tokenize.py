#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import sys;
sys.path.append('..');
from stanford_parser import parser;
import nltk;
import re
from nltk.tokenize.stanford import StanfordTokenizer;

class tokenizer:
    def __init__(self):
        self.stanford_tokenizer = \
        StanfordTokenizer('../stanford-parser-2010-08-20/stanford-parser.jar'\
                         ,options={"americanize": False});
        pass;

    #tokenize with stanford_parser
    def stanford_tokenize(self,row):
        temp_list = self.stanford_tokenizer.tokenize(row);
        return temp_list;
    
    #tokenize with nltk word_tokenizer
    def word_tokenize(self,row):
        temp_list = nltk.word_tokenize(row);
        list_length = len(temp_list);
        index_list = list();
        for i in xrange(list_length):
            if temp_list[i].startswith('\''):
                if len(temp_list[i]) > 3:
                    temp_list[i] = temp_list[i][1:];
                    index_list.append(i);
        #end for
        count = 0;
        for index in index_list:
            temp_list.insert(index+count,'\'');
            count+=1;
        #end for
        return temp_list;

    def no_block(self ,string):
        string = re.sub(r' ','',string);
        return len(string);


if __name__ == '__main__':
    t = tokenizer();
    print t.no_block('i like     you!');
