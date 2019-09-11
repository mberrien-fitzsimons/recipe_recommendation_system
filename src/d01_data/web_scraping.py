import pandas as pd
from selenium import webdriver    #open webdriver for specific browser
from selenium.webdriver.common.keys import Keys   # for necessary browser action
from selenium.webdriver.common.by import By    # For selecting html code
import scrapy
from scrapy import Selector
import time
import re
from scrapy.linkextractors import LinkExtractor

def sr_scraping():
    # List of main URLs to scrape (collected by hand from simplyrecipes.com)
    main_url_list = ['https://www.simplyrecipes.com/recipes/main-ingredient/pork/',
                'https://www.simplyrecipes.com/recipes/ingredient/chicken/',
                'https://www.simplyrecipes.com/category/eat-your-food/',
                'https://www.simplyrecipes.com/recipes/type/quick/',
                'https://www.simplyrecipes.com/recipes/ingredient/beef/',
                'https://www.simplyrecipes.com/recipes/main-ingredient/pork/',
                'https://www.simplyrecipes.com/recipes/ingredient/fish_and_seafood/',
                'https://www.simplyrecipes.com/recipes/ingredient/pasta/',
                'https://www.simplyrecipes.com/recipes/type/budget/',
                'https://www.simplyrecipes.com/recipes/type/baking/',
                'https://www.simplyrecipes.com/recipes/course/dessert/',
                'https://www.simplyrecipes.com/recipes/diet/allergy-friendly/',
                'https://www.simplyrecipes.com/recipes/diet/dairy-free/',
                'https://www.simplyrecipes.com/recipes/diet/gluten-free/',
                'https://www.simplyrecipes.com/recipes/diet/low_carb/',
                'https://www.simplyrecipes.com/recipes/diet/paleo/',
                'https://www.simplyrecipes.com/recipes/diet/vegan/',
                'https://www.simplyrecipes.com/recipes/diet/vegetarian/',
                'https://www.simplyrecipes.com/recipes/ingredient/egg/',
                'https://www.simplyrecipes.com/recipes/ingredient/rice/',
                'https://www.simplyrecipes.com/recipes/ingredient/vegetable/']

    url = "https://www.simplyrecipes.com/"
    browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    browser.get(url) #navigate to the page

    links_done = []
    for url in main_url_list:
        browser.get(url)
        for pg_num in range(1, 11):
            page = 'page/{}/'.format(pg_num)
            next_page = url+"{}".format(page)

            try:
                browser.get(next_page)
            except:
                break

            time.sleep(5)

            sel = Selector(text = browser.page_source)

            time.sleep(5)

            all_links = sel.xpath('//*[@id="content"]/ul//li/a').extract()

            for links in all_links:
                links_done.append(re.search('a href=\"(.*)\" title=\"', links).group(1))

    links_df = pd.DataFrame(links_done)
    links_df.rename(columns={0:'links'}, inplace=True)

    links_list_complete = links_df['links']

    title = []
    prep_time = []
    cook_time = []
    recipe_yield = []
    tags = []
    ingredients = []
    entire_card = []
    byline = []
    link_food = []

    count = 1
    for link in links_list_complete:

        print(str(count) + ' out of ' + str(998))
        browser.get(link)

        time.sleep(3)

        sel = Selector(text = browser.page_source)

        title.append(sel.xpath("//h1[@class='entry-title']/text()").extract())
        prep_time.append(sel.xpath("//div[@class='recipe-meta']/ul/li[1]//text()").extract())
        cook_time.append(sel.xpath("//div[@class='recipe-meta']/ul/li[2]//text()").extract())
        recipe_yield.append(sel.xpath("//div[@class='recipe-meta']/ul/li[3]//text()").extract())
        tags.append(sel.xpath("//div[@class='category-bar']//text()").extract())
        ingredients.append(sel.xpath("//div[@class='entry-details recipe-ingredients']//text()").extract())
        entire_card.append(sel.xpath("//div[@id='sr-recipe-callout']//text()").extract())
        byline.append(sel.xpath("//span[@class='entry-byline']//text()").extract())
    #     link_food.append(sel.xpath("//div[@id='sr-recipe-callout']//text()").extract())

        exec("df{} = pd.DataFrame(zip(title, prep_time, cook_time, recipe_yield, tags, ingredients, entire_card, byline), columns =['title', 'prep_time', 'cook_time', 'recipe_yield', 'tags', 'ingredients', 'entire_card', 'byline'])".format(count))
        exec("df{}.to_csv('../../data/01_raw/simply_recipes/simply_recipes_{}.csv')".format(count, count))

        count = count + 1
