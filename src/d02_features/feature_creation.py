import pandas as pd
import numpy as np
import argparse
import nltk
import pandas as pd
import pycrfsuite
import numpy as np
import re
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer

from d00_utils.utils import singularize, word2features, extract_features, get_labels

src_dir = os.path.join(os.getcwd(), '..')
sys.path.append(src_dir)

def nyt_ingredients_crf_feature_creation(nyt_ing):

    nyt_ing_tuple = []
    for index, row in nyt_ing.iterrows():
        name = row[1]
        qty = row[2]
        unit = row[4]
        comment = row[5]
        nyt_ing_tuple.append([(qty, 'qty'), (unit, 'unit'),
        (name, 'name'),
        (comment, 'comment')])
    # break up tuples with multiple words
    nyt_ing_tuple_new = []
    for sub_list in nyt_ing_tuple:
        sub_ls = []
        for elem in sub_list:
            if " " in str(elem[0]):
                elem2 = elem[0].split(" ")
                for el in elem2:
                    sub_ls.append((el, elem[1]))
            else:
                sub_ls.append((elem[0], elem[1]))
        nyt_ing_tuple_new.append(sub_ls)
    # erase tuples with missing values
    for idx_big, ingredient in enumerate(nyt_ing_tuple_new):
        for idx, word in enumerate(ingredient):
            if word[0] == 'missing':
                nyt_ing_tuple_new[idx_big].remove(word)
            if word[0] == '':
                nyt_ing_tuple_new[idx_big].remove(word)

    # strip all puncctuation from tuple
    crf_data = []
    for sub_list in nyt_ing_tuple_new:
        sublist = []
        for word in sub_list:
            word2 = str(word[0]).strip(')!,.?(')
            sublist.append((word2, word[1]))
        crf_data.append(sublist)

    count = 1
    while count <= 2:
        count = count + 1
        for idx_big, ingredient in enumerate(crf_data):
            for idx, word in enumerate(ingredient):
                if word[0] == 'missing':
                    crf_data[idx_big].remove(word)
                if word[0] == '':
                    crf_data[idx_big].remove(word)
     # add parts of speech
    data_nyt = []
    for i, doc in enumerate(crf_data):

        # Obtain the list of tokens in the document
        tokens = [t for t, label in doc]

        # Perform POS tagging
        try:
            tagged = nltk.pos_tag(tokens)
        except:
            tagged = 'missing'

        # Take the word, POS tag, and its label
        data_nyt.append([(w, pos, label) for (w, label), (word, pos) in zip(doc, tagged)])

    X = [extract_features(doc) for doc in data_nyt]
    y = [get_labels(doc) for doc in data_nyt]

    return [X, y]

from d00_utils.utils import singularize, word2features, extract_features, get_labels

nltk.download('averaged_perceptron_tagger')

def instacart_prod_crf_feature_creation(instacart_prod_train):

    instacart_prod_train.fillna("missing", inplace=True)
    insta_product_tuple = []

    for index, row in instacart_prod_train.iterrows():
        pre_description = row[1].lower()
        food = row[2].lower()
        post_description = row[3].lower()
        insta_product_tuple.append([(pre_description, 'pre'), (food, 'food'), (post_description, 'post')])

    # break up the tuple into multiple WORDS
    insta_product_tuple_new = []
    for sub_list in insta_product_tuple:
        sub_ls = []
        for elem in sub_list:
            if " " in str(elem[0]):
                elem2 = elem[0].split(" ")
                for el in elem2:
                    sub_ls.append((el, elem[1]))
            else:
                sub_ls.append((elem[0], elem[1]))
        insta_product_tuple_new.append(sub_ls)

    # erase tuples with missing values
    for idx_big, product in enumerate(insta_product_tuple_new):
        for idx, word in enumerate(product):
            if word[0] == 'missing':
                insta_product_tuple_new[idx_big].remove(word)
            if word[0] == '':
                insta_product_tuple_new[idx_big].remove(word)

    # strip puncctuation
    crf_data = []
    for sub_list in insta_product_tuple_new:
        sublist = []
        for word in sub_list:
            word2 = str(word[0]).strip(')!,.?(')
            sublist.append((word2, word[1]))
        crf_data.append(sublist)

    count = 1
    while count <= 2:
        count = count + 1
        for idx_big, ingredient in enumerate(crf_data):
            for idx, word in enumerate(ingredient):
                if word[0] == 'missing':
                    crf_data[idx_big].remove(word)
                if word[0] == '':
                    crf_data[idx_big].remove(word)

    # construct Features
    data_instacart = []
    for i, doc in enumerate(crf_data):

        # Obtain the list of tokens in the document
        tokens = [t for t, label in doc]

        # Perform POS tagging
        try:
            tagged = nltk.pos_tag(tokens)
        except:
            tagged = 'missing'

        # Take the word, POS tag, and its label
        data_instacart.append([(w, pos, label) for (w, label), (word, pos) in zip(doc, tagged)])

    X = [extract_features(doc) for doc in data_instacart]
    y = [get_labels(doc) for doc in data_instacart]

    return [X, y]
