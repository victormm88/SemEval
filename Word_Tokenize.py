#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import nltk;
import re;

class tokenizer:
    def __init__(self):
        pass;

    def word_tokenize(self,row):
        temp_list = nltk.word_tokenize(row);
        list_length = len(temp_list);
        index_list = [];
        for i in xrange(list_length):
            if temp_list[i].startswith('\''):
                '''
                if i != list_length - 1:
                    if temp_list[i+1] == '\'':
                        temp_list[i]=temp_list[i][1:];
                        index_list.append(i);
                '''
                if len(temp_list[i]) > 3:
                    temp_list[i] = temp_list[i][1:];
                    index_list.append(i);
        #end for 
        count = 0;
        for index in index_list:
            temp_list.insert(index+count,'\'');
            count+=1;
        return temp_list;

    def no_block(self ,string):
        string = re.sub(r' ','',string);
        return len(string);


if __name__ == '__main__':
    t = tokenizer();
    print t.no_block('i like     you!');
