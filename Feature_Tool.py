#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

from bs4 import BeautifulSoup;
from Word_Tokenize import tokenizer;
from nltk.tag.stanford import POSTagger;
from nltk.stem.porter import PorterStemmer;

class Feature_Tool:
    '''
    '''
    def __init__(self):
        self.tf = tokenizer();
        pass;
    
    #get row train data
    def get_row(self,row_file,target):
        row_str = '''''';
        f = open(row_file,'rb');
        w = open('row_%s'%target,'wb');
        for row in f:
            row_str+=row;
        soup = BeautifulSoup(row_str);
        self.soup = soup;
        sentences = soup.find_all('sentence');
        for block in sentences:
            text = block.text.strip();
            text_token = self.tf.word_tokenize(text);
            text_label = ['O']*len(text_token);
            #print block.children;
            aspectTerms = block.aspectterms;
            if aspectTerms == None:
                pass;
            else:
                for aspectterm in aspectTerms.contents:
                    if str(type(aspectterm)).endswith('Tag\'>'):
                        term = aspectterm['term'];
                        beg = aspectterm['from'];
                        end = aspectterm['to'];
                        beg = int(beg);
                        end = int(end);
                        no_block = self.tf.no_block(text[:beg]);
                        count_letter  = 0;
                        term_index = 0;
                        while count_letter != no_block:
                            count_letter += len(text_token[term_index]);
                            term_index+=1;
                        text_label[term_index]='B';
                        temp_list = self.tf.word_tokenize(term);
                        token_num = len(temp_list);
                        if token_num > 1:
                            for x in range(1,token_num):
                                text_label[term_index+x] = 'I';
            #end if
            for num in xrange(len(text_token)):
                w.write(text_label[num]+'\n');
            w.write('\n');
            #print text_label,text_token;
        #end for
        return;
    
    #add POS feature
    def add_POS(self,row_file,target):
        row_str = '''''';
        f = open(row_file,'rb');
        for row in f:
            row_str+=row;
        soup = BeautifulSoup(row_str);
        self.soup = soup;
        sentences = soup.find_all('sentence');
        all_token = list();
        for block in sentences:
            text = block.text.strip();
            text_token = self.tf.word_tokenize(text);
            all_token.append(text_token);
        stanford_tagger = \
        POSTagger('../stanford-postagger-full-2015-01-30/models/english-bidirectional-distsim.tagger','../stanford-postagger-full-2015-01-30/stanford-postagger.jar');
        tagged_result = stanford_tagger.tag_sents(all_token);
        for row in tagged_result:
            index_list = list();
            for num,item in enumerate(row):
                if item[0] == '(' or item[0] == ')':
                    index_list.append(num);
            for i in index_list:
                row[i]=(row[i][0],row[i][0]);
        #end for
        w = open('pos_%s'%target,'wb');
        for row in tagged_result:
            for item in row:
                w.write(item[0]+' '+item[1]+'\n');
            w.write('\n');
        #print tagged_result;
        return;

    #add Stemming Feature
    def add_Stem(self,row_file,target):
        '''
        '''
        stemmer = PorterStemmer();
        row_str = '''''';
        f = open(row_file,'rb');
        for row in f:
            row_str+=row;
        soup = BeautifulSoup(row_str);
        self.soup = soup;
        sentences = soup.find_all('sentence');
        all_token = list();
        for block in sentences:
            text = block.text.strip();
            text_token = self.tf.word_tokenize(text);
            for i in xrange(len(text_token)):
                text_token[i] = stemmer.stem(text_token[i]);
            all_token.append(text_token);
        #end for
        w = open('stem_%s'%target,'wb');
        for row in all_token:
            for item in row:
                w.write(item+'\n');
            w.write('\n');
        pass;

if __name__ == '__main__':
    ft = Feature_Tool();
    target = 'train'
    ft.get_row('../Restaurants_Train_v2.xml','train');
    ft.add_POS('../Restaurants_Train_v2.xml','train');
    ft.add_Stem('../Restaurants_Train_v2.xml','train');
