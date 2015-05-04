#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' '''

__author__ = 'Wang Junqi'

def main(file_name,target_file):
    row_f = open(file_name,'rb');
    target_f = open(target_file,'wb');
    first_flag=True;
    for row in row_f:
        row=row.lstrip();
        if row.startswith('<text>'):
            if first_flag:
                first_flag = False;
            else:
                target_f.write('\n');
            target_f.write(row[6:-8]);
        elif row.startswith('<aspectTerm term'):
            begin=row.index('\"');
            end=row.index('\"',begin+1);
            target_f.write('|'+row[begin+1:end]);
                
    

if __name__ == '__main__':
    main('../Restaurants_Train_v2.xml','row_train.csv');
