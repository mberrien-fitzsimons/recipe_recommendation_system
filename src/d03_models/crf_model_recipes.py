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

src_dir = os.path.join(os.getcwd(), '..')
sys.path.append(src_dir)

from d00_utils.utils import singularize, word2features, extract_features, get_labels

nltk.download('averaged_perceptron_tagger')

def clumpFractions(s):
    """
    Replaces the whitespace between the integer and fractional part of a quantity
    with a dollar sign, so it's interpreted as a single token. The rest of the
    string is left alone.

        clumpFractions("aaa 1 2/3 bbb")
        # => "aaa 1$2/3 bbb"
    """
    return re.sub(r'(\d+)\s+(\d)/(\d)', r'\1$\2/\3', s)

def ingredient_tagger(ingredient_sentence, ingredient_label_sentence):
    qty = []
    unit = []
    name = []
    comment = []

    for word, label in zip(ingredient_sentence, ingredient_label_sentence):
        if label == 'qty':
            qty.append(word)
        if label == 'unit':
            unit.append(word)
        if label == 'name':
            name.append(word)
        if label == 'comment':
            comment.append(word)
    return {'qty': " ".join(qty), 'unit': " ".join(unit), 'name': " ".join(name), 'comment': " ".join(comment)}


def recipe_tagger(single_recipe, matching_recipe_labels):
    ret = []
    for ingredient, ingredient_label in zip(single_recipe, matching_recipe_labels):
        ret.append(ingredient_tagger(ingredient, ingredient_label))
    return ret

def token_labels_to_dict(tokens, labels, recipe_titles, links):
    recipe_dict = {}
    recipe_link_dict = {}
    for recipe, label, title, link in zip(tokens, labels, recipe_titles, links):
        ing = recipe_tagger(recipe, label)
        recipe_dict[str(title).lower()] = ing
        recipe_link_dict[str(title).lower()] = link
    return [recipe_dict, recipe_link_dict]

def crf_model_recipe_tagger(recipe_sr):
    ingredients_lists = list(recipe_sr.ingredients)

    count = 0
    while count <= 3:
        count = count + 1
        for sub_list in ingredients_lists:
            for idx, element in enumerate(sub_list):
                try:
                    if element == "                                              ":
                        sub_list.pop(idx)
                    if element.startswith('For'):
                        sub_list.pop(idx)
                    if element.startswith('Wire'):
                        sub_list.pop(idx)
                    if element.startswith('DAD'):
                        sub_list.pop(idx)
                    if element.startswith('Sauce'):
                        sub_list.pop(idx)
                    if element.startswith(' Special equipment'):
                        sub_list.pop(idx)
                    if element.startswith(' to serve'):
                        sub_list.pop(idx)
                    if element == "":
                        sub_list.pop(idx)
                    if element.startswith(' or store'):
                        sub_list.pop(idx)
                    if element.startswith('homemade'):
                        sub_list.pop(idx)
                    if element.startswith('Rimmed'):
                        sub_list.pop(idx)
                    if element.startswith(' 9x13'):
                        sub_list.pop(idx)
                    if element.startswith('Instant Pot'):
                        sub_list.pop(idx)
                    if element.startswith(' on the'):
                        sub_list.pop(idx)
                    if element.startswith('slow cook'):
                        sub_list.pop(idx)
                except:
                    pass

    ingredients_lists_new = []
    for recipe in ingredients_lists:
        sub_list = []
        for ingredient in recipe:
            sub_list.append(clumpFractions(ingredient))
        ingredients_lists_new.append(sub_list)

    # let's tokenize all the words and get rid of punctuation
    tokenizer = RegexpTokenizer(r'(\d\/\d |\w+)')
    token_sr = []
    for recipe in ingredients_lists_new:
        sub_list = []
        for ingredient in recipe:
            sub_list.append(tokenizer.tokenize(ingredient))
        token_sr.append(sub_list)

    crf_data  = []
    index = 0
    for recipe in token_sr:
        sub_list = []
        for ingredient in recipe:
            pos = nltk.pos_tag(ingredient)
            sub_list.append((pos))
        crf_data.append(sub_list)
        index = index + 1

    crf_data_final = []
    for recipe in crf_data:
        X = [extract_features(doc) for doc in recipe]
        crf_data_final.append(X)

    tagger = pycrfsuite.Tagger()
    tagger.open('../../data/04_models/crf_ing_final.model')

    sr_labels = []
    for recipe in crf_data_final:
        y_pred = [tagger.tag(xseq) for xseq in recipe]
        sr_labels.append(y_pred)

    recipe_titles = list(recipe_sr.title)

    links = list(recipe_sr.link_food)

    recipe_ing_dict, recipe_links_dict = token_labels_to_dict(token_sr, sr_labels,
                                                           recipe_titles, links)

    recipe_tag_list = list(recipe_sr.tags)

    # create a dictionary of recipe tags
    tags_recipes = []
    for tag_list in recipe_tag_list:
        sub_list = []
        for tags in tag_list:
            tag_new = tags.split("', '")
            tags_recipes.append(tag_new)

    recipe_tags_dict = {}
    for title, tag in zip(recipe_titles, tags_recipes):
        recipe_tags_dict[str(title).lower()] = tag

    return [recipe_ing_dict, recipe_links_dict, recipe_tags_dict]
