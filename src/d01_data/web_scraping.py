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

def marianos_insta_scraping():
    # dictionary of Marianos Aile Numbers on Instacart

    url = "https://www.instacart.com/"
    browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    browser.get(url) #navigate to the page

    time.sleep(70)

    instacart_ailes = {'produce': [1370, 1365, 1367, 1368, 1373, 1366],
        'frozen': [1473, 1472, 1478, 1476, 4302, 1474, 1489, 2997, 1475, 3799, 1477],
         'bakery': [1443, 1442, 1479, 1441, 1444],
         'alcohol': [1445, 1446, 1450, 1449, 1448, 1447, 2708],
         'international': [1408, 1409, 1483, 1410, 1411],
         'beverages': [1455, 1453, 1451, 1452, 1456, 1491, 1454, 2780],
         'pets': [1378, 1379, 1380],
         'dry goods pasta': [1429, 3798, 1482, 1431, 1430, 2745, 3600, 2746],
         'bulk': [3657, 3662, 3664, 6374, 6378, 3658, 3661, 3663, 3659, 6377, 3665],
         'personal care': [3793, 1384, 2720, 1395, 1392, 3794, 3795, 1387, 3796, 1388, 3651, 6458, 1390, 3792, 1393, 1382, 1383, 3412, 3011, 3012, 6492],
         'meat seafood': [1464, 1470, 1465, 1488, 2768, 1487, 1471],
         'pantry': [1419, 1420, 1428, 1421, 1426, 1423, 1422, 3747, 1496, 1496, 1424, 1425, 3605],
         'breakfast': [1413, 1481, 1480, 1412],
         'canned goods': [1414, 1415, 1416, 1417, 1418],
         'dairy eggs': [1459, 1462, 1461, 1457, 1460, 1458, 4251, 1463, 1498],
         'household': [1402, 1403, 1398, 1405, 1404, 1399, 1400, 1401, 1407, 1406, 6493],
         'babies': [1437, 1438, 1440, 1439, 3642],
         'snacks': [1435, 1432, 1433, 1434, 1497, 1485, 1486, 1436, 2709, 3014, 1484],
         'deli': [1375, 1374, 1494, 3603, 1377, 6664]}

    # Convert dictionary to list of aile numbers
    aile_numbers = []
    for list in instacart_ailes.values():
        for val in list:
            aile_numbers.append(val)
    aile_numbers.sort()

    # Now let's start scraping the website
    aile_numbers
    total_num_ailes = len(aile_numbers)
    count = 1

    for aile in aile_numbers[62:]:

        browser.get("https://www.instacart.com/store/marianos/departments/199/aisles/{}".format(aile))

        time.sleep(3)

        for i in range(0,40):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        sel = Selector(text = browser.page_source)

        time.sleep(5)
        count = count + 1


        product = sel.xpath("//span[@class='full-item-name']/text()").extract()
        unit_price = sel.xpath('//div[@class="item-price"]/span/span[1]/text()').extract()
    #     item_size = sel.xpath("//span[@class='item-size muted']//text()").extract()
        item_size = sel.xpath('//*[@class="item-card"]').extract()
        product_aile = sel.xpath("//h1[@data-radium]//text()").extract()
        prod_aile_count = (product_aile * len(product))

        exec("df{} = pd.DataFrame(zip(product, unit_price, item_size, prod_aile_count), columns =['product', 'unit_price', 'item_size', 'prod_aile'])".format(aile))

        exec("df{}.to_csv('../../data/01_raw/prod_aile_{}.csv', index=False)".format(aile, aile))
