#!/bin/sh
#

echo 'Calculating the result....'
./Feature_Tool.py > /dev/null
cp sentence_test ../CRF++-0.54/example/semeval/
cd ../CRF++-0.54/example/semeval/;
awk -f my_awk sentence_test > test_model
./crf.sh > result.csv
./extract_term.py
