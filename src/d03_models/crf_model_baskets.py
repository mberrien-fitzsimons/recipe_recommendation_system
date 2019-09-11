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
