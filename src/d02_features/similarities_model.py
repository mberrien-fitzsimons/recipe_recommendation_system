import numpy as np
import pandas as pd
import time
import random

from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

basket_matrix_usr = pd.read_csv('../../data/03_processed/basket_matrix_usr.csv')

basket_matrix_usr.replace(np.nan, 0, inplace=True)

def calculate_similarity(dataframe):
    """Calculate the column-wise cosine similarity for a sparse
    matrix. Return a new dataframe matrix with similarities.
    """
    data_sparse = sparse.csr_matrix(dataframe)
    similarities = cosine_similarity(data_sparse.transpose())
    sim = pd.DataFrame(data=similarities, index= dataframe.columns, columns= dataframe.columns)
    return sim

data_matrix = calculate_similarity(basket_matrix_usr)

data_matrix.to_csv('../../data/05_model_output/data_matrix_sim.csv')
