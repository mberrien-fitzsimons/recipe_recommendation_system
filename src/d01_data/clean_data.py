import pandas as pd
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sys
import re


def combine_instacart_kaggle_datasets(aisles, departments, order, order_products__prior, products):
    '''
    Combines all documents used from the kaggle dataset.
    '''
    prod_ailes = products.merge(aisles,
                  how='outer',
                  on='aisle_id',
                  suffixes=('_x', '_y'))

    product_dataset = prod_ailes.merge(departments,
                    how='outer',
                    on='department_id')

    orders_full = order_products__prior.merge(order,
                             how='left',
                             on='order_id')

    ret = orders_full.merge(product_dataset,
                           how='left',
                           on='product_id')

    return ret


def intermediate_clean_recipes_sr(sr_recipes_raw):
    '''
    takes concatenated raw dataset from raw to intermediate clean.
    '''
    # let's clean the title
    titles = sr_recipes_raw.title
    title_new = []
    for title in titles:
        try:
            title_new.append(re.search("'(.*)\'", title).group(1))
        except:
            title_new.append(np.nan)

    # clean prep time column
    prep_time = sr_recipes_raw.prep_time
    prep_time_new = []
    for time in prep_time:
        try:
            prep_time_new.append(re.search("\'Prep time:\', \' \',\ \'(.*)\'", time).group(1))
        except:
            prep_time_new.append(np.nan)

    # clean cook time column
    cook_times = sr_recipes_raw.cook_time
    cook_time_new = []
    for time in cook_times:
        try:
            cook_time_new.append(re.search("\'Cook time:\', \' \',\ \'(.*)\'", time).group(1))
        except:
            cook_time_new.append(np.nan)

    # clean the recipe yield column
    recipe_yield = sr_recipes_raw.recipe_yield
    recipe_yield_new = []
    for element in recipe_yield:
        try:
            recipe_yield_new.append(re.search("\'Yield:\', \' \', \'(.*)\']", element).group(1))
        except:
            recipe_yield_new.append(np.nan)

    # clean tags column
    tags = sr_recipes_raw.tags
    tags_new = []
    for tag in tags:
        sub_list = []
        try:
            sub_list.append(re.search("\'Filed under:\', \' \',\ (.*)\]", tag).group(1))
        except:
            sub_list.append(np.nan)
        tags_new.append(sub_list)

    # clean ingredients column
    ingredient_lists = sr_recipes_raw.ingredients

    count = 0
    while count <= 3:
        count = count + 1
        for sub_list in ingredient_lists:
            for idx, element in enumerate(sub_list):
                try:
                    if element == "Ingredients":
                        sub_list.pop(idx)
                    if element == "'":
                        sub_list.pop(idx)
                    if element == "":
                        sub_list.pop(idx)
                    if element == "                        ', '":
                        sub_list.pop(idx)
                    if element == "                        ', 'For the sauce:', '":
                        sub_list.pop(idx)
                    if element == "                                                  ', ' Special equipment:', '":
                        sub_list.pop(idx)
                    if '\\\\t' in element:
                        sub_list.pop(idx)
                    if element == "                                              '":
                        sub_list.pop(idx)
                    if element == '':
                        sub_list.pop(idx)
                except:
                    pass

    ingredients_new = []
    for ingredient_list in ingredient_lists:
        try:
            ingredients_new.append(re.findall("\'(.*?)\'", ingredient_list))
        except:
            ingredients_new.append(np.nan)

    count = 0
    while count <= 3:
        count = count + 1
        for sub_list in ingredients_new:
            for idx, element in enumerate(sub_list):
                try:
                    if element == "Ingredients":
                        sub_list.pop(idx)
                    if element == "'":
                        sub_list.pop(idx)
                    if element == "":
                        sub_list.pop(idx)
                    if element == "                        ', '":
                        sub_list.pop(idx)
                    if element == "                        ', 'For the sauce:', '":
                        sub_list.pop(idx)
                    if element == "                                                  ', ' Special equipment:', '":
                        sub_list.pop(idx)
                    if '\\\\t' in element:
                        sub_list.pop(idx)
                    if element == "                                              '":
                        sub_list.pop(idx)
                    if element == '':
                        sub_list.pop(idx)
                    if "                        ', '" in element:
                        sub_list.pop(idx)
    #                 if element == "', '":
    #                     sub_list.pop(idx)
                except:
                    pass

    # Note, this line needs to be run three times. Fix this later.
    count = 0
    while count <= 3:
        for sub_list in ingredients_new:
            for idx, element in enumerate(sub_list):
                if "\\n" in element:
                    sub_list.pop(idx)
        count = count + 1

    nl = []
    for i in ingredients_new:
        sl = []
        for ele in i:
            sl.append(ele.strip('.][\,'))
        nl.append(sl)

    data_sr = []
    for i in nl:
        sl = []
        for ele in i:
            sl.append(ele.strip("').,('"))
        data_sr.append(sl)

    # clean byline
    bylines = list(sr_recipes_raw.byline)
    byline_new = []
    for byline in bylines:
        try:
            byline_new.append(re.search("\[\'by   \', \'   \', \'(.*)\', \'", byline).group(1))
        except:
            byline_new.append(byline)

    byline_new_2 = []
    for byline in byline_new:
        try:
            byline_new_2.append(re.search("\[\'by   \', \'   \', \'(.*)\'\]", byline).group(1))
        except:
            byline_new_2.append(byline)

    byline_new_3 = []
    for byline in byline_new_2:
        try:
            byline_new_3.append(re.search("\[\'   \', \'   \', (.*)\'\]", byline).group(1))
        except:
            byline_new_3.append(byline)

    # clean link
    link_food = list(sr_recipes_raw.link_food)
    link_food_new = []
    for link in link_food:
        try:
            link_food_new.append(re.search("\\\'<link rel=\"canonical\" href=\"(.*)\"\>\\\'\]", link).group(1))
        except:
            link_food_new.append(link)

    # make empty dataset
    recipe_sr_full_final = pd.DataFrame()
    # make empty thing.
    recipe_sr_full_final['title'] = title_new
    recipe_sr_full_final['prep_time'] = prep_time_new
    recipe_sr_full_final['cook_time'] = cook_time_new
    recipe_sr_full_final['tags'] = tags_new
    recipe_sr_full_final['ingredients'] = data_sr
    recipe_sr_full_final['recipe_yield'] = recipe_yield_new
    recipe_sr_full_final['byline'] = byline_new_3
    recipe_sr_full_final['link_food'] = link_food_new

    return recipe_sr_full_final


def intermediate_clean_marianos_prices(groceries):
    '''
    clean concatenated marianos prices dataframes to intermediate
    '''
    item_size = groceries['item_size']
    per_lb_final = []
    per_lb_pattern = r'\d*\.[0-9]{2}\/lb'
    for item in item_size:
        try:
            per_lb_final.append(re.search(per_lb_pattern, item).group())
        except:
            per_lb_final.append(np.nan)

    # MEASURE WORDS
    measure_word_pattern = 'each'
    measure_word_list = []
    for item in item_size:
        try:
            measure_word_list.append(re.search(measure_word_pattern, item).group())
        except:
            measure_word_list.append(np.nan)

    groceries.rename(columns={'unit_price':'main_price'}, inplace=True)

    # ITEM WEIGHT COUNT VOL
    item_weight_count_vol = []
    for item in item_size:
        try:
            item_weight_count_vol.append(re.search('aria-label=\"\.(.*)\">\d+', item).group(1))
        except:
            item_weight_count_vol.append(np.nan)

    groceries.drop(columns=['item_size'], inplace=True)

    # MAKE NEW DATAFRAME
    groceries['price_per_lb'] = per_lb_final
    groceries['measure_words_main_price'] = measure_word_list
    groceries['item_weight_count_vol'] = item_weight_count_vol
    groceries['date_collected'] = '2019-08-28'
    groceries['store'] = 'Marianos'
    groceries['location'] = '60615'

    return groceries
