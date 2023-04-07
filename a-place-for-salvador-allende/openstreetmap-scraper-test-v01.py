# workflow of this script:
# 1. get a CSV file generated from allende-scraper
# 2. for every row in that file: 
    # 2.1 get every unique country + locale pair
    # 2.2 pass 'salvador allende [country] [locale]' into a search query in openstreetmap [https://www.openstreetmap.org/search?query=]
    # 2.3 retrieve results list - each one returns an address string 
    # [Residential Road Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru]
    # 2.4 for every result:
        # 2.4.1 address string will be parsed into locale_2, zip_code, etc.
        # 2.4.2 add URL to openstreetmap_link


from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import re
import pandas as pd


# create a Google Chrome driver object
# https://stackoverflow.com/questions/69918148/deprecationwarning-executable-path-has-been-deprecated-please-pass-in-a-servic
s = Service('C:\\Users\\canogle\\.cache\\selenium\\chromedriver\\win32\\110.0.5481.77\\chromedriver.exe')
driver = webdriver.Chrome(service=s)


# ------------------------------------------------------ #



### 1. IMPORT DATAFRAME/CSV FROM ALLENDE-SCRAPER ###


# I think that we can just keep on using the dictionary of items from allende-scraper-main.
# Anyway, we'll test stuff here first.

csv_name = str(input('>>> Please enter a CSV file: '))

data_df = pd.read_csv(csv_name)
print('DataFrame loaded:\n')
print(data_df)


# for this script only, convert the dataframe back into a dictionary
data = data_df.to_dict(orient='list')


# we're working on one country per file so we can just save the country name as a variable
country_en = re.search(r'(.*)\.csv', csv_name)
country_en = str(country_en.group(1))



### we can copy the next line onwards to allende-scraper-main


# get a list of unique locale_1 names
locale_1_list = data_df['locale_1'].unique().tolist()

print(f'{len(locale_1_list)} distinct locale(s) found.\n')

for (i, locale) in enumerate(locale_1_list, start=1):
    print(f'{str(i)}: {locale}')


# generate OpenStreetMap search link for every locale_1
osm_search_links = []

for locale in locale_1_list:
    locale_link = f'https://www.openstreetmap.org/search?query=Salvador%20Allende%20{country_en}%20{locale}'
    osm_search_links.append(locale_link)


# run every locale_1 through OpenStreetMap
for (i, link) in enumerate(osm_search_links, start=1):
    driver.get(link)
    osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer("div", class_="search_results_entry mx-n3"))
    print(f'\n>>> Searching locale {str(i)} of {str(len(osm_search_links))}: {link}...\n')
    osm_text = osm_soup.get_text()
    #
    # if there are no results found, skip to the next locale (if any)
    #
    if 'No results found' in osm_text:
        print(f'No results found - manual search needed for this locale.')
    #
    # if there are results, iterate through each of them
    #
    else:
        results_list = osm_soup.find_all("a")
        for result in results_list:
            #
            # get ID (null)
            #
            id = ''
            data['id']
            print(f'ID: {id}')
