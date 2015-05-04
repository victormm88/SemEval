#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Word2vector Tools for calulate simalarity of words
'''

__author__ = 'Wang Junqi'

import numpy as np;

class Word2vector_Tool:
    '''
    '''
    def __init__(self,fname):
        self.fname = fname;
        self.his_dict = dict();
        pass;

    #load from the word2vec.txt or google-news-corpus
    def load_bin_vec(self,vocab=set()):
        """
        Loads 300x1 word vecs from Google (Mikolov) word2vec
        """
        fname = self.fname;
        word_vecs = {};
        with open(fname, "rb") as f:
            header = f.readline();
            vocab_size, layer1_size = map(int, header.split());
            binary_len = np.dtype('float32').itemsize * layer1_size;
            word_list = [];
            for line in xrange(vocab_size):
                if len(word_list)>100:
                    break;
                word = [];
                while True:
                    ch = f.read(1);
                    if ch == ' ':
                        word = ''.join(word);
                        print word;
                        word_list.append(word);
                        break;
                    if ch != '\n':
                        word.append(ch);
                    else:
                        print 'what?';
                if word in vocab:
                    word_vecs[word] = np.fromstring(f.read(binary_len),dtype='float32');
                else:
                    f.read(binary_len);
            print word_list;
        return word_vecs;


    #creat index of words
    def creat_index(self):
        """
        Create Word Index from Google (Mikolov) word2vec
        """
        word_index = {};
        with open(self.fname, "rb") as f:
            header = f.readline();
            vocab_size, layer1_size = map(int, header.split());
            self.featrue_longth = layer1_size;
            binary_len = np.dtype('float32').itemsize * layer1_size;
            line_size = 0L+len(header);
            temp_num = 0;
            for line in xrange(vocab_size):
                '''
                if temp_num>100:
                    break;
                temp_num+=1;
                #'''
                word = [];
                while True:
                    ch = f.read(1);
                    if ch == ' ':
                        word = ''.join(word);
                        break;
                    word.append(ch);
                #end while
                word_index[word]=line_size;
                line_size+=len(word)+1+binary_len;
                f.read(binary_len);
            #end for
        self.word_index = word_index;
        return;
    
    #Get the vector of word with the word name
    def get_word_feafure(self,word):
        '''
        word - the word name 
        caution:this function can only be invoked after the function
        'creat_index()' invoked
        '''
        f = open(self.fname,'rb');
        f.seek(self.word_index[word]);
        f.read(len(word)+1);
        binary_len = np.dtype('float32').itemsize * self.featrue_longth;
        result = np.fromstring(f.read(binary_len),dtype='float32');
        return result;

    #calculate the most sim word in the pos_set
    def get_Maxsim(self,word,pos_set,target='train'):
        if not self.word_index.has_key(word):
            return word,0.0 if target == 'train' else 1.0;
        max_word='';
        max_sim=0.0;
        for temp_word in pos_set:
            sim = self.get_sim(word,temp_word);
            if sim > max_sim:
                max_sim = sim;
                max_word = temp_word;
        return max_word,max_sim;

    #calculate the similarity of two words
    def get_sim(self,word_1,word_2):
        if not self.word_index.has_key(word_2):
            return 0.0;
        fea_1 = self.get_word_feafure(word_1);
        fea_2 = self.get_word_feafure(word_2);
        dist = np.linalg.norm(fea_1-fea_2);
        sim = 1.0 / (1.0 + dist);
        return sim;

def main():
    wt = Word2vector_Tool('../Word2vector/GoogleNews-vectors-negative300.bin');
    #wt.load_bin_vec();
    wt.creat_index();
    print wt.get_sim('Pizza','pizza');

if __name__ == '__main__':
    main();
