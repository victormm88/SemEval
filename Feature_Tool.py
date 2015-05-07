#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

import sys;
sys.path.append('..');
from stanford_parser import parser;
import re;
from bs4 import BeautifulSoup;
from Word_Tokenize import tokenizer;
from nltk.tag.stanford import POSTagger;
from nltk.stem.porter import PorterStemmer;
import csv;

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
            text_token = self.tf.stanford_tokenize(text);
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
                            print count_letter,no_block;
                            if text_token[term_index].endswith('RB-'):
                                count_letter += 1;
                            else:
                                count_letter += len(text_token[term_index]);
                            count_letter -= text_token[term_index].count('/');
                            term_index+=1;
                        text_label[term_index]='B';
                        temp_list = self.tf.stanford_tokenize(term);
                        token_num = len(temp_list);
                        if token_num > 1:
                            for x in range(1,token_num):
                                text_label[term_index+x] = 'I';
            #end if
            for num in xrange(len(text_token)):
                w.write(text_token[num]+' '+text_label[num]+'\n');
            w.write('\n');
            print text_label,text_token;
        #end for
        return;
    
    #get token
    def get_token(self,target):
        f = open('row_%s'%target,'rb');
        all_token = list();
        now_list = list();
        for row in f:
            if row == '\n':
                all_token.append(now_list);
                now_list = list();
            else:
                temp_str = row.split()[0];
                now_list.append(temp_str);
        return all_token;

    #add POS feature
    def add_POS(self,row_file,target):
        '''
        row_str = '';
        f = open(row_file,'rb');
        for row in f:
            row_str+=row;
        soup = BeautifulSoup(row_str);
        self.soup = soup;
        sentences = soup.find_all('sentence');
        all_token = list();
        for block in sentences:
            text = block.text.strip();
            text_token = self.tf.stanford_tokenize(text);
            all_token.append(text_token);
        '''
        all_token = self.get_token(target);
        stanford_tagger = \
        POSTagger('../stanford-postagger-full-2015-01-30/models/english-bidirectional-distsim.tagger','../stanford-postagger-full-2015-01-30/stanford-postagger.jar');
        tag_list = list();
        for row in all_token:
            temp_list = list();
            for word in row:
                if len(word)>1 and re.match(r'^[A-Z]+',word):
                    temp_list.append(word.lower());
                else:
                    temp_list.append(word);
            tag_list.append(temp_list);1
        #end for
        tagged_result = stanford_tagger.tag_sents(tag_list);
        '''
        for row in tagged_result:
            index_list = list();
            for num,item in enumerate(row):
                if not re.match(r'.*[\w\d]+',item[0]):
                    index_list.append(num);
            for i in index_list:
                row[i]=(row[i][0],row[i][0]);
        #end for
        '''
        w = open('pos_%s'%target,'wb');
        for num1,row in enumerate(tagged_result):
            for num2,item in enumerate(row):
                w.write(all_token[num1][num2]+' '+item[1]+'\n');
            w.write('\n');
        #print tagged_result;
        return;

    #add Stemming Feature
    def add_Stem(self,row_file,target):
        stemmer = PorterStemmer();
        '''
        row_str = '';
        f = open(row_file,'rb');
        for row in f:
            row_str+=row;
        soup = BeautifulSoup(row_str);
        self.soup = soup;
        sentences = soup.find_all('sentence');
        all_token = list();
        for block in sentences:
            text = block.text.strip();
            text_token = self.tf.stanford_tokenize(text);
            for i in xrange(len(text_token)):
                text_token[i] = stemmer.stem(text_token[i]);
            all_token.append(text_token);
        #end for
        '''
        all_token = self.get_token(target);
        w = open('stem_%s'%target,'wb');
        for row in all_token:
            for item in row:
                w.write(stemmer.stem(item)+'\n');
            w.write('\n');
        return;

    #get dependency feature
    def get_dependency(self,row_file,target):
        stanford_parser = parser.Parser();
        row_str = '';
        f = open(row_file,'rb');
        for row in f:
            row_str+=row;
        soup = BeautifulSoup(row_str);
        self.soup = soup;
        sentences = soup.find_all('sentence');
        all_sentences = list();
        for block in sentences:
            text = block.text.strip();
            all_sentences.append(text);
        #end for
        temp_csv = csv.writer(open('dependency_%s'%target,'wb'));
        for sentence in all_sentences:
            temp_list = stanford_parser.parseToStanfordDependencies(sentence);
            for item in temp_list:
                temp_csv.writerow(item);
            temp_csv.writerow([]);
        return;

    #add dependency feature
    def add_dependency(self,target):
        f = csv.reader(open('dependency_%s'%target,'rb'));
        w = open('dep_%s'%target,'wb');
        all_token = self.get_token(target);
        #opinion_dict = self.add_opinion(target);
        for row in all_token:
            temp_list = ['none']*len(row);
            dep = f.next();
            while dep != list():
                if dep[0] == 'amod':
                    temp_list[int(dep[1])]='%s_1'%dep[0];
                    temp_list[int(dep[2])]='%s_2'%dep[0];
                '''
                if dep[0] == 'nsubj':
                    temp_list[int(dep[2])]='%s_2'%dep[0];
                if dep[0] == 'nn':
                    temp_list[int(dep[1])]='%s_1'%dep[0];
                    temp_list[int(dep[2])]='%s_2'%dep[0];
                '''
                dep = f.next();
            for item in temp_list:
                w.write(item+'\n');
            w.write('\n');
        return;
    
    #get opinion-lexicon feature:
    def add_opinion(self,target,filename = 'default'):
        opinion_dict = dict();
        if filename == 'default':
            pos_f = open('../opinion-lexicon-English/positive-words.txt','rb');
            neg_f = open('../opinion-lexicon-English/negative-words.txt','rb');
            for _ in xrange(35):
                pos_f.readline();
                neg_f.readline();
            for word in pos_f:
                opinion_dict[word.strip()]=True;
            for word in neg_f:
                opinion_dict[word.strip()]=False;
        else:
            f = \
            open('../subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff','rb');
            for row in f:
                row = row.split();
                word = row[2].split('=')[1];
                polar = row[5].split('=')[1];
                if True:#polar != 'neutral':
                    opinion_dict[word]=polar;#True if polar == 'positive' else False;
        all_token  = self.get_token(target);
        w = open('opinion_%s'%target,'wb');
        for row in all_token:
            for word in row :
                if opinion_dict.has_key(word):
                    w.write('opion\n'); #if opinion_dict[word] else 'neg\n');
                else:
                    w.write('order\n');
            w.write('\n');
        return opinion_dict;

if __name__ == '__main__':
    ft = Feature_Tool();
    train_file = '../Restaurants_Train_v2.xml';
    test_file = '../ABSA_TestData_PhaseB/Restaurants_Test_Data_phaseB.xml';
    target = 'train'
    #ft.get_row(train_file,target);
    #ft.add_POS(test_file,target);
    #ft.add_Stem(train_file,target);
    #ft.add_opinion(target);
    #ft.add_opinion('test');
    ft.add_dependency('test');
    ft.add_dependency('train');
