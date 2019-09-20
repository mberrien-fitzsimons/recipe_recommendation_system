import argparse
import nltk
import pandas as pd
import pycrfsuite
import numpy as np
import re
import pickle

import os
import sys

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer

nltk.download('averaged_perceptron_tagger')

src_dir = os.path.join(os.getcwd(), '..')
sys.path.append(src_dir)

from d00_utils.utils import singularize, word2features, extract_features, get_labels

# A function for extracting features in documents
def extract_features(doc):
    return [word2features(doc, i) for i in range(len(doc))]

def product_tagger(product_sentence_tokens, product_label_sentence):
    pre = []
    food = []
    post = []

    for word, label in zip(product_sentence_tokens, product_label_sentence):
        if label == 'pre':
            pre.append(word.lower())
        if label == 'food':
            food.append(word.lower())
        if label == 'post':
            post.append(word.lower())
    return {'pre': " ".join(pre), 'food': " ".join(food), 'post': " ".join(post)}

def token_labels_to_dict(tokens, labels, titles):
    final_dict = {}
    for token, label, title in zip(tokens, labels, titles):
        prod = product_tagger(token, label)
        final_dict[str(title).lower()] = prod
    return final_dict

def food_label_finder(token_list, label_list):
    pre = []
    food = []
    post = []

    for word, label in zip(token_list, label_list):
        if label == 'pre':
            pre.append(word.lower())
        if label == 'food':
            food.append(word.lower())
        if label == 'post':
            post.append(word.lower())
    return " ".join(food)

def crf_basket_feature_creation(instacart_baskets):
    instacart_baskets.drop(columns = ['add_to_cart_order', 'reordered', 'aisle_id',
                        'department_id', 'aisle', 'eval_set', 'order_number',
                        'order_dow', 'order_hour_of_day'], inplace=True)

    instacart_baskets_food = instacart_baskets.loc[(instacart_baskets['department']!='personal care')&
                                               (instacart_baskets['department']!='household')&
                                               (instacart_baskets['department']!='babies')&
                                               (instacart_baskets['department']!='pets')&
                                               (instacart_baskets['department']!='other')&
                                               (instacart_baskets['department']!='alcohol')&
                                               (instacart_baskets['department']!='missing')&
                                               (instacart_baskets['department']!='beverages')&
                                               (instacart_baskets['department']!='snacks')]

    products_list = list(instacart_baskets_food.product_name)

    # let's tokenize all the words and get rid of punctuation
    tokenizer = RegexpTokenizer(r'(\d\/\d |\w+)')

    token_sr = []
    for product in products_list:
        token_sr.append(tokenizer.tokenize(product))

    crf_data  = []
    for product in token_sr:
        pos = nltk.pos_tag(product)
        crf_data.append(pos)

    X = [extract_features(doc) for doc in crf_data]

    return [X, token_sr, products_list]

def crf_basket_dataset_creation(token_sr, labels, products_list, baskets):

    final_dict = token_labels_to_dict(token_sr, labels, products_list)

    prod_list_new = []
    for token, label in zip(token_sr, labels):
        prod_list_new.append(food_label_finder(token, label))

    baskets['new_prod_list'] = prod_list_new

    return baskets
