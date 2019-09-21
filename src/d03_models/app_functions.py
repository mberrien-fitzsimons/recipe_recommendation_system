import pandas as pd
import numpy as np
import pickle
import collections
import random
from collections import Counter

def _extract_ingredients(single_recipe_ing_list):
    ret = []
    for ingredient in single_recipe_ing_list:
        ret.append(ingredient['name'])
    return ret

def _ingredient_recipe_matcher(ingredients_list, shopping_list, recipe_title):
    matching_recipes = []
    matching_ingredients = []
    return_recipes = []

    for element in shopping_list:
        if any(element in s for s in ingredients_list):
            matching_recipes.append(recipe_title)
        count_recipe_dict = dict(Counter(matching_recipes))

    for key, val in count_recipe_dict.items():
        if val >= 2:
            return_recipes.append(key)

    if len(return_recipes) > 0:
        return return_recipes

def _find_matching_recipe(recipe_dict, recipe_tags_dict, shopping_list, meal, dietary_preference):
    listofkeys = []
    recipes = []
    recipe_final = []
    restricted_recipes = []
    ret = []
    listofitems = recipe_dict.items()

    for item in listofitems:
        ingred_list = _extract_ingredients(item[1])
        recipe_title = item[0]
        recipes.append(_ingredient_recipe_matcher(ingred_list, shopping_list, recipe_title))
    filtered_recipes = list(filter(None, recipes))

    for lst in filtered_recipes:
        for item in lst:
            recipe_final.append(item)

    # check if meal and dietary preferences met
    if meal is not None:
        for title in recipe_final:
            if meal in recipe_tags_dict[title]:
                restricted_recipes.append(title)
    else:
        restricted_recipes = recipe_final

    if dietary_preference is not None:
        for diet in restricted_recipes:
            if dietary_preference in recipe_tags_dict[diet]:
                ret.append(diet)
    else:
        ret = restricted_recipes

    return ret

###################################################
############## MAIN APPLICATION ###################
###################################################

def recipe_recommendations_app(shopping_list, recipe_dict, recipe_tags_dict, meal, dietary_preference, recipe_links_dict):

    data_matrix = pd.read_csv('../../data/05_model_output/data_matrix_sim.csv')
    data_matrix.set_index('Unnamed: 0', inplace=True)
    database_food_list = list(data_matrix.columns)

    items_in_database = []
    item_missing = []
    for item in shopping_list:
        if item in database_food_list:
            items_in_database.append(item)
        else:
            item_missing.append(item)
#     if len(item_missing) > 0:
#         print('Items Not Found in Database: ', item_missing)
    ##############################################
    # search instacart matrix for similair items #
    ##############################################
    known_user_likes = items_in_database
    # Construct a new dataframe with the 10 closest neighbours (most similar)
    # for each artist.
    data_neighbours = pd.DataFrame(index=data_matrix.columns, columns=range(1,11))
    for i in range(0, len(data_matrix.columns)):
        data_neighbours.ix[i,:10] = data_matrix.ix[0:,i].sort_values(ascending=False)[:10].index
    # Get the artists the user has played.

    # Construct the neighbourhood from the most similar items to the
    # ones our user has already liked.
    most_similar_to_likes = data_neighbours.loc[known_user_likes]
    similar_list = most_similar_to_likes.values.tolist()
    similar_list = list(set([item for sublist in similar_list for item in sublist]))

    ret = _find_matching_recipe(recipe_dict, recipe_tags_dict, shopping_list, meal, dietary_preference)

    if len(ret) == 0:
        ret2 = ret
        print('\n\n Sorry, there are currently no recipes that meet your tastes.')

    elif len(ret) > 7:
        ret2 = random.choices(ret, k=5)
    else:
        ret2 = ret

    index = 0
    for i in ret2:
        index = index + 1
        link = recipe_links_dict[i]

        print('\nRecipe {}: '.format(index), i, link)
