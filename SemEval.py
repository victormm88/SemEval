#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Some methods for the task of SemEval 2015

'''

__author__ = 'Wang Junqi'

import nltk;
import re;
from nltk.tag.stanford import POSTagger;
import csv;
import numpy as np;
import word2vector;
import pickle;
from Word_Tokenize import tokenizer;

class SemEval_Tool:
    '''
    '''
    def __init__(self):
        self.tk = tokenizer();
        pass;

    #Get train_data and test_data
    def get_Data(self,file_name,ratio=0.8):
        print '正在构建训练集和验证集....';
        f_reader = open(file_name,'rb');
        data=[];
        label=[];
        for row in f_reader:
            row = row[:-1];
            row = row.split('|');
            temp_str = row[0];
            #process the sentence
            temp_str = re.sub(r'[()]',' ',temp_str);
            #temp_str = re.sub(r' \'',' ',temp_str);
            data.append(temp_str);
            label.append(row[1:]);
        data_num = len(data);
        self.train_data=data[:int(ratio*data_num)];
        self.train_label=label[:int(ratio*data_num)];
        self.test_data=data[int(ratio*data_num):];
        self.test_label=label[int(ratio*data_num):];
        #create label_dir
        label_dir = dict();
        for row in label:
            for temp_l in row:
                if not label_dir.has_key(temp_l):
                    label_dir[temp_l]=1;
                else:
                    label_dir[temp_l]+=1;
        self.label_dir=label_dir;
        #create words lebal
        train_word_label = list();
        for row in self.train_label:
            temp_list = list();
            for item in row:
                if ' ' in item:
                    temp_result = nltk.pos_tag(item.split());
                    temp_result = [x for x,y in temp_result if \
                                   y.startswith('N')];
                    temp_list+=temp_result;
                else:
                    temp_list.append(item);
            train_word_label.append(temp_list);
        #end for
        test_word_label = list();
        for row in self.test_label:
            temp_list = list();
            for item in row:
                if ' ' in item:
                    temp_result = nltk.pos_tag(item.split());
                    temp_result = [x for x,y in temp_result if \
                                   y.startswith('N')];
                    temp_list+=temp_result;
                else:
                    temp_list.append(item);
            test_word_label.append(temp_list);
        #end for
        self.train_word_label = train_word_label;
        self.test_word_label = test_word_label;
        print '完成！';
        return;
    
    #pos train/test data 
    def pos_data(self,method='stanford'):
        '''
        pos data with alternative method --stanford with pos-tagger writen by
        stanford,or --nltk (other word) with the pos-tagger inside NLTK
        '''
        print '正在标注语料....';
        my_tag=int;
        if method == 'stanford':
            st=POSTagger('../stanford-postagger-full-2015-01-30/models/english-bidirectional-distsim.tagger'\
                        ,'../stanford-postagger-full-2015-01-30/stanford-postagger.jar');
            my_tag = st.tag_sents;
            #get tagged train_data
            sentences = list();
            for sentence in self.train_data:
                sentences.append(self.tk.word_tokenize(sentence));
            self.tagged_train_data = my_tag(sentences);
            #get tagged test_data
            sentences = list();
            for sentence in self.test_data:
                sentences.append(self.tk.word_tokenize(sentence));
            self.tagged_test_data = my_tag(sentences);
        elif method == 'nltk':
            my_tag = nltk.pos_tag;
            #get tagged train_data 
            tagged_train_data = list();
            for row in self.train_data:
                tagged_train_data.append(my_tag(row.split()));
            #get tagged test_data
            tagged_test_data = list();
            for row in self.test_data:
                tagged_test_data.append(my_tag(row.split()));

            self.tagged_train_data=tagged_train_data;
            self.tagged_test_data = tagged_test_data;
        pickle.dump(self.tagged_train_data,open('__tagged_train_data','wb'));
        pickle.dump(self.tagged_test_data,open('__tagged_test_data','wb'));
        #self.tagged_train_data=pickle.load(open('__tagged_train_data','rb'));
        #self.tagged_test_data=pickle.load(open('__tagged_test_data','rb'));
        print '完成！';
        return;

    #get pattern for train data
    def get_pattern(self,befor_num=1,after_num=0):
        print '正在获取词性搭配....';
        self.befor_num=befor_num;
        self.after_num=after_num;
        pos_pattern = dict();
        for num,row in enumerate(self.tagged_train_data):
            pos_result = row;
            word_list = [x for x,_ in pos_result];
            pos_list = [x for _,x in pos_result];
            for term in self.train_label[num]:
                if ' ' in term:
                    continue;
                if word_list.count(term) == 0:
                    continue;
                temp_index = word_list.index(term);
                temp_pattern = pos_list[temp_index];
                if not temp_pattern.startswith('N'):
                    temp_pattern='NN';
                #calculate part of before
                for i in range(1,befor_num+1):
                    if temp_index-i>=0 and pos_list[temp_index-i].isupper():
                        temp_pattern = pos_list[temp_index-i]+' '+temp_pattern;
                    else:
                        temp_pattern='NN';
                        break;
                
                #calculate part of after
                for i in range(1,after_num+1):
                    if temp_index+i <len(word_list) and \
                            pos_list[temp_index+i].isupper():
                        temp_pattern+=' '+pos_list[temp_index+i];

                if ' ' in temp_pattern:
                    if pos_pattern.has_key(temp_pattern):
                        pos_pattern[temp_pattern]+=1;
                    else:
                        pos_pattern[temp_pattern]=1;

        self.patter_dict = pos_pattern;
        print '完成！';
        return;
    

    #generate aspect terms of a sentence
    def aspect_terms_extracter(self,method = 'tag'):
        print 'pass';
        if method == 'tag':
            self.aspect_terms_extracter_tag();
        elif method == 'word2vector':
            self.aspect_terms_extracter_w2v();
            pass;
        print 'done';
        return;

    #generate aspect terms of a sentence by pos_tagging
    def aspect_terms_extracter_tag(self):
        print '正在计算结果....';
        final_result = list();
        for pos_result in self.tagged_test_data:
            result=list();
            word_list = [x for x,_ in pos_result];
            pos_list = [x for _,x in pos_result];
            for key in self.patter_dict.keys():
                temp_list = key.split(' ');
                inner_index = 0;
                for word in temp_list:
                    if word.startswith('N'):
                        break;
                    inner_index+=1;
                temp_index = self.get_index(temp_list,pos_list);
                while temp_index>=0:
                    result.append(word_list[temp_index+self.befor_num]);
                    temp_index = self.get_index(temp_list,pos_list,temp_index+1);
            temp_result=list();
            for candid in result:
                if not candid in self.neg_set:
                    temp_result.append(candid);
            final_result.append(temp_result);
        print '完成！';
        return final_result;

    def aspect_terms_extracter_w2v(self,min_sim=0.4):
        print '正在计算结果....';
        final_result = list();
        wt=word2vector.Word2vector_Tool('../Word2vector/GoogleNews-vectors-negative300.bin');
        wt.creat_index();
        '''
        min_sim = 0.0;
        for row in self.tagged_train_data:
            for word,pos in row :
                if pos.startswith('N') and word not in self.pos_set:
                    _,temp_sim = wt.get_Maxsim(word,self.pos_set);
                    if temp_sim > min_sim:
                        min_sim = temp_sim;
                        print _,word;
        #end for
        print min_sim;
        '''
        count=0;
        for row in self.tagged_test_data:
            result = list();
            for word,pos in row:
                if pos.startswith('N'):
                    if word in self.pos_set:
                        result.append(word);
                    else:
                        _,temp_sim = wt.get_Maxsim(word,self.pos_set);
                        if temp_sim > min_sim:
                            result.append(word);
                            count += 1;
                            print word,_;
            #end for
            final_result.append(result);
        print count;
        print '完成！';
        return final_result;


    #generate pos_dict 
    def generate_pos_set(self):
        print '正在构建正性集词典....';
        pos_dict = dict();
        pos_set=set();
        sentences = list();
        for row in self.train_label:
            for key in row:
                if ' ' in key:
                    sentences.append(self.tk.word_tokenize(key));
                else:
                    pos_dict[key] = pos_dict.setdefault(key,0) + 1;
                    #pos_set.add(key);
        #end for
        st=POSTagger('../stanford-postagger-full-2015-01-30/models/english-bidirectional-distsim.tagger'\
                        ,'../stanford-postagger-full-2015-01-30/stanford-postagger.jar');
        result = st.tag_sents(sentences);
        for row in result:
            for item in row:
                if item[1].startswith('NN'):
                    pos_dict[item[0]] = pos_dict.setdefault(item[0],0) + 1;
                    #pos_set.add(item[0]);
        #end for
        neg_dict = dict();
        for num,row in enumerate(self.tagged_train_data):
            for item in row :
                if item[1].startswith('NN') and item[0] not in self.train_word_label[num]:
                    neg_dict[item[0]] = neg_dict.setdefault(item[0],0) + 1;
        for key in pos_dict.keys():
            if pos_dict[key] > 1:
                if neg_dict.has_key(key):
                    if neg_dict[key]/pos_dict[key] < 2:
                        pos_set.add(key);
                else:
                    pos_set.add(key);
        self.pos_set=pos_set;
        print '完成！';
        return;

    #generate neg_dict
    def generate_neg_set(self):
        print '正在构建负性词典....';
        neg_set=set();
        for num,row in enumerate(self.tagged_train_data):
            result=list();
            pos_result = row;
            word_list = [x for x,_ in pos_result];
            pos_list = [x for _,x in pos_result];
            for key in self.patter_dict.keys():
                temp_list = key.split(' ');
                temp_index = self.get_index(temp_list,pos_list);
                inner_index = 0;
                for word in temp_list:
                    if word.startswith('N'):
                        break;
                    inner_index+=1;
                while temp_index>=0:
                    result.append(word_list[temp_index+self.befor_num]);
                    temp_index = self.get_index(temp_list,pos_list,temp_index+1);
            for candid in result:
                if not candid in self.pos_set:
                    neg_set.add(candid);
        neg_set.add('restaurant');
        self.neg_set = neg_set;
        print '完成！';
        return;
        

    #calculate F1 scores in test
    def get_f1(self,final_result):
        my_num=0;
        correct_num=0;
        answer_num=0;
        for num in xrange(len(self.test_data)):
            test_label=self.test_word_label[num];
            result=final_result[num];
            answer_num+=len(test_label);
            my_num+=len(result);
            for candid in result:
                if candid in test_label:
                    correct_num+=1;
                    test_label.remove(candid);
        p=float(correct_num)/my_num;
        r=float(correct_num)/answer_num;
        f=2*p*r/(p+r);
        print '准确率：',p;
        print '召回率：',r;
        print 'F1值：',f;
        return;

    #clean the word from both sides
    def clean_word(self,word):
        if len(word) == 1:
            return word;
        if not re.match(r"[a-zA-Z]",word[0]):
            word = word[1:];
        if not re.match(r"[a-zA-Z]",word[-1]):
            word = word[:-1];
        return word;
    
    #calculate index of a list in another
    def get_index(self,list_short,list_long,beg=0):
        while len(list_long)-beg >= len(list_short):
            temp_l=beg;
            temp_s=0;
            while list_long[temp_l] == list_short[temp_s]:
                temp_l+=1;
                temp_s+=1;
                if temp_s == len(list_short):
                    return beg;
            beg+=1;
        return -1;


def main():
    sem_tool = SemEval_Tool();
    sem_tool.get_Data('row_train.csv',0.8);
    #print sem_tool.test_word_label;
    sem_tool.pos_data();
    #sem_tool.get_pattern(befor_num=1);
    sem_tool.generate_pos_set();
    #sem_tool.generate_neg_set();
    final_result=sem_tool.aspect_terms_extracter_w2v(0.33);
    #print final_result;
    sem_tool.get_f1(final_result);
    #'''
    return;

if __name__ == '__main__':
    main();
        
