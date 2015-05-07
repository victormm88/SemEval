paste pos_train stem_train lower_train opinion_train dep_train r_train > train_data
paste pos_test stem_test lower_test opinion_test dep_test r_test > test_data
cp train_data test_data ~/download/CRF++-0.54/example/semeval/
