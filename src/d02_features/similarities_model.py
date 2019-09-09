import numpy as np
import pandas as pd
import time
import random

from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

# # read in data
# baskets = pd.read_csv('../../data/05_model_output/baskets_newprodlist_2.csv')
#
# # cut out numbers from dataframe
# mask = ((baskets['new_prod_list']!='1')&(baskets['new_prod_list']!='100')&(baskets['new_prod_list']!='11')&(baskets['new_prod_list']!='118')&(baskets['new_prod_list']!='2')&(baskets['new_prod_list']!='24')&(baskets['new_prod_list']!='3')&(baskets['new_prod_list']!='3 cheese')&(baskets['new_prod_list']!='30')&(baskets['new_prod_list']!='328')&(baskets['new_prod_list']!='4')&(baskets['new_prod_list']!='5')&(baskets['new_prod_list']!='50')&(baskets['new_prod_list']!='6')&(baskets['new_prod_list']!='6 cheese')&(baskets['new_prod_list']!='60')&(baskets['new_prod_list']!='7')&(baskets['new_prod_list']!='70')&(baskets['new_prod_list']!='8')&(baskets['new_prod_list']!='85')&(baskets['new_prod_list']!='9')&(baskets['new_prod_list']!='95')&(baskets['new_prod_list']!='97')&(baskets['new_prod_list']!='98')&(baskets['new_prod_list']!='a')&(baskets['new_prod_list']!='a garlic butter sauce')&(baskets['new_prod_list']!=np.nan)&(baskets['new_prod_list']!='nan'))
# # this will get rid of the unwated numbers in product new_prod_list
# baskets = baskets[mask]
#
# # Let's take a subsample now of the users (200k is too many)
# insta_users_lst = list(baskets.user_id.unique())
# random_usrids_100k = random.sample(insta_users_lst, 100000)
# mask_user = baskets['user_id'].isin(random_usrids_100k)
# baskets_100k = baskets.loc[mask_user]
#
#
# # Let's do
# baskets_100k.drop(columns=['user_id'], inplace=True)
# baskets_100k.reset_index(inplace=True)
# baskets_100k.dropna(inplace=True)
#
# product_list = list(baskets_100k.new_prod_list.unique())
#
# baskets_complete = baskets_100k.drop(columns=['index', 'product_name'])
#
# product_list_1 = product_list[:1000]
# mask_prod1 = baskets_complete['new_prod_list'].isin(product_list_1)
# baskets_prod1 = baskets_complete.loc[mask_prod1]
#
# # pivot the dataset
# basket_matrix_1 = (baskets_prod1.groupby(['order_id', 'new_prod_list'])['all_ones']
#           .sum().unstack().reset_index().fillna(0)
#           .set_index('order_id'))
#
# product_list_2 = product_list[1000:2000]
# mask_prod2 = baskets_complete['new_prod_list'].isin(product_list_2)
# baskets_prod2 = baskets_complete.loc[mask_prod2]
# # pivot the dataset
# basket_matrix_2 = (baskets_prod2.groupby(['order_id', 'new_prod_list'])['all_ones']
#           .sum().unstack().reset_index().fillna(0)
#           .set_index('order_id'))
#
# product_list_3 = product_list[2000:3000]
# mask_prod3 = baskets_complete['new_prod_list'].isin(product_list_3)
# baskets_prod3 = baskets_complete.loc[mask_prod3]
# # pivot the dataset
# basket_matrix_3 = (baskets_prod3.groupby(['order_id', 'new_prod_list'])['all_ones']
#           .sum().unstack().reset_index().fillna(0)
#           .set_index('order_id'))
#
# product_list_4 = product_list[3000:]
# mask_prod4 = baskets_complete['new_prod_list'].isin(product_list_4)
# baskets_prod4 = baskets_complete.loc[mask_prod4]
# # pivot the dataset
# basket_matrix_4 = (baskets_prod4.groupby(['order_id', 'new_prod_list'])['all_ones']
#           .sum().unstack().reset_index().fillna(0)
#           .set_index('order_id'))
#
# matrix1 = basket_matrix_1.merge(basket_matrix_2,
#                       how='outer',
#                       on='order_id')
#
# matrix2 = matrix1.merge(basket_matrix_3,
#                       how='outer',
#                       on='order_id')
#
# basket_matrix_usr = matrix2.merge(basket_matrix_4,
#                       how='outer',
#                       on='order_id')

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
