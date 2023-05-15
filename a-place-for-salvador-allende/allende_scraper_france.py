# allende-scraper-france.py
# Main repo: https://github.com/GoGroGlo/a-place-for-salvador-allende
# Automates the data collection by verifying the list from http://www.abacq.org/calle/index.php?2009/05/13/349-salvador-allende-en-francia using https://www.openstreetmap.org

'''
PSEUDOCODE

use firefox driver

if allende_in_france_locales.txt doesn't exist yet:
    open allende_in_france.txt
    for each line in allende_in_france.txt:
        extract postal code and locale and save in list
        if postal code + locale already exists in list, skip
        save list in a new file allende_in_france_locales.txt and close
    
if allende_in_france_links.txt doesn't exist yet:
    retrieve list of abacq france links from TOC using bs4
    remove exclusions from list
    save in a new file allende_in_france_links.txt and close

open allende_in_france_locales.txt
split lines into groups of 20
make dict to store results
for locale in locale_20s:
    search in OSM using 'salvador allende [postcode] [locale]'
    if there are results:
        [A] load more results if present
        if all results are loaded:
            convert each result into data items in dict
            [B] using the raw address, check allende_in_france_links.txt for any matching article
            if article(s) are found:
                have user verify if this matches
                if yes:
                    put as abacq_reference
                else:
                    skip
            if exact specific place + locale already exists in dict, skip
            save whatever we can in dict
    if there are no results:
        search in OSM using 'allende [postcode] [locale]'
        if there are results:
            do [A]
        if there are no results:
            do [B]
            save whatever we can in dict
export dict into excel file

'''

# ------------------------------------------------------ #


### IMPORTS ###


# web scraping tutorial courtesy of https://www.educative.io/blog/python-web-scraping-tutorial


from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
import pandas as pd 
import re
import os
import math


# local import - I hope this works
import allende_scraper_main as asm


# ------------------------------------------------------ #


### CONSTANTS ###


country_en = 'France'


# how long (in seconds) would you like sleep timers to wait before continuing with the scraping?
timer = 30


# URLs
homepage = 'http://www.abacq.org'
toc = 'http://www.abacq.org/calle/index.php?toc/toc'
links_exceptions = ['http://www.abacq.org/calle/index.php?2009/05/13/349-salvador-allende-en-francia', 
                    'http://www.abacq.org/calle/index.php?2007/02/18/2-francia-le-blanc-mesnil', 
                    'http://www.abacq.org/calle/index.php?2009/12/08/445-victor-jara-francia', 
                    'http://www.abacq.org/calle/index.php?2007/02/18/56-pablo-neruda-en-francia', 
                    'http://www.abacq.org/calle/index.php?2007/02/18/22-victor-jara']


# create a dictionary of lists that's easily translatable into our existing db
data = {
    'id'                         : [],
    'name'                       : [],
    'type'                       : [],
    'region'                     : [],
    'country'                    : [],
    'locale_1'                   : [],
    'locale_2'                   : [],
    'locale_3'                   : [],
    'locale_4'                   : [],
    'locale_5'                   : [],
    'zip_code'                   : [],
    'latitude'                   : [],
    'longitude'                  : [],
    'oldest_known_year'          : [],
    'oldest_known_month'         : [],
    'oldest_known_day'           : [],
    'oldest_known_source'        : [],
    'desc'                       : [],
    'desc_language'              : [],
    'alt_name'                   : [],
    'former_name'                : [],
    'verified_in_maps'           : [],
    'openstreetmap_link'         : [],
    'google_maps_link'           : [],
    'abacq_reference'            : [],
}


# ------------------------------------------------------ #


### FUNCTIONS ###


# create a Firefox driver object
def create_driver():
    s = Service()
    global driver
    driver = webdriver.Firefox(service=s)


# maximize window for every open page
def browser_window(link):
    driver.get(link)
    driver.maximize_window()


# Modified OpenStreetMap checker of LOCALE_1
def osm_check(locale_1):

    # store search results here
    global locale_results_list
    locale_results_list = []


    # first, do a specific search for 'Salvador Allende'
    print(f'Searching OpenStreetMap for \'Salvador Allende {locale_1} France\'...')
    locale_link = f'https://www.openstreetmap.org/search?query=Salvador%20Allende%20{locale_1}%20{country_en}'
    browser_window(locale_link)

    # humanizer fixes the problem of the script getting no OSM info sometimes when you can see in the browser that there actually is
    asm.humanizer(timer)

    # press 'More results' button while it's present
    try:
        driver.find_element(By.CSS_SELECTOR, '.search_more > a:nth-child(1)')
    except:
        pass
    else:
        driver.find_element(By.CSS_SELECTOR, '.search_more > a:nth-child(1)').send_keys(Keys.ENTER)

    # collect search results - at this point, it looks like this

    # <a class="set_position" data-lat="-12.1102763" data-lon="-77.0104283"
    # data-min-lat="-12.1103037" data-max-lat="-12.1102452" data-min-lon="-77.0109212" data-max-lon="-77.0097999"
    # data-prefix="Residential Road" data-name="Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru"
    # data-type="way" data-id="426845566" href="/way/426845566">Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru</a>
    
    osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
        "ul", class_="results-list list-group list-group-flush"))
    locale_results_list.extend(
        list(osm_soup.find_all("a", class_="set_position")))
    print(f'{len(locale_results_list)} results found.')

    # if there are no results for 'Salvador Allende', try a more general search for 'Allende'
    if len(locale_results_list) == 0:
        print(f'Searching OpenStreetMap for \'Allende {locale_1} France\'...')
        locale_link = f'https://www.openstreetmap.org/search?query=Allende%20{locale_1}%20{country_en}'
        browser_window(locale_link)

        # humanizer fixes the problem of the script getting no OSM info sometimes when you can see in the browser that there actually is
        asm.humanizer(timer)

        # press 'More results' button while it's present
        try:
            driver.find_element(By.CSS_SELECTOR, '.search_more > a:nth-child(1)')
        except:
            pass
        else:
            driver.find_element(By.CSS_SELECTOR, '.search_more > a:nth-child(1)').send_keys(Keys.ENTER)

        # collect search results - at this point, it looks like this

        # <a class="set_position" data-lat="-12.1102763" data-lon="-77.0104283"
        # data-min-lat="-12.1103037" data-max-lat="-12.1102452" data-min-lon="-77.0109212" data-max-lon="-77.0097999"
        # data-prefix="Residential Road" data-name="Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru"
        # data-type="way" data-id="426845566" href="/way/426845566">Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru</a>
        
        osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
            "ul", class_="results-list list-group list-group-flush"))
        locale_results_list.extend(
            list(osm_soup.find_all("a", class_="set_position")))
        print(f'{len(locale_results_list)} results found.')

    return locale_results_list




# ------------------------------------------------------ #


### PREPARE LISTS ###


# prune and save list of locales for verification
if os.path.exists('france\\allende_in_france_locales.txt') == False:


    # placeholder list
    allende_in_france_locales = []


    # pruning process
    with open('france\\allende_in_france.txt','r') as f:
        for l in f.readlines():
            l = re.search(r'.+\s+((?:\d{5})?\s+.+)(?=\.)', l)
            l = l.group(1).strip()
            if l not in allende_in_france_locales:
                allende_in_france_locales.append(l)


    # create and write to allende_in_france_locales.txt
    with open('france\\allende_in_france_locales.txt','w') as w:
        for l in allende_in_france_locales:
            w.write(f'{l}\n')


    # print for logging purposes
    print('allende_in_france_locales.txt created.')


# otherwise, just let user know that there is already a file
else:
    print('allende_in_france_locales.txt found.')


# prune and save list of links for verification
if os.path.exists('france\\allende_in_france_links.txt') == False:


    # open up the table of contents
    create_driver()
    browser_window(toc)
    asm.humanizer(asm.timer)
    soup = BeautifulSoup(driver.page_source, 'html.parser',
                         parse_only=SoupStrainer("div", id="toc"))
    links_soup = soup.find_all("li")
    

    # create a list of France links
    allende_in_france_links = []

    for link in links_soup:
        link = str(link)
        if 'francia' in link:
            link = re.search(
                r'(\/calle\/index.php\?\d{4}\/\d{2}\/\d{2}\/\d*(?:-\w*)*)', link)
            link = str(homepage) + str(link.group(1))
            allende_in_france_links.append(link)


    # remove exceptions from France links
    for link in links_exceptions:
        if link in allende_in_france_links:    
            allende_in_france_links.remove(link)

    for link in allende_in_france_links:
        for i in ['victor-jara', 'pablo-neruda']:
            if i in str(link):
                allende_in_france_links.remove(link)


    # create and write to allende_in_france_links.txt
    with open('france\\allende_in_france_links.txt','w') as w:
        for l in allende_in_france_links:
            w.write(f'{l}\n')


    # print for logging purposes
    print('allende_in_france_links.txt created.')


# otherwise, just let user know that there is already a file
else:
    print('allende_in_france_links.txt found.')


# ------------------------------------------------------ #


### SPLIT LOCALE LIST INTO GROUPS OF 20 ###


with open('france\\allende_in_france_locales.txt','r', encoding="utf=8") as f:
    f = f.readlines()


    # number of items in a chunk (default 20 for France)
    chunk_number = 1


    # ask user which chunk to work on
    try:
        target_chunk = int(input(
            f'>>> {math.ceil(len(f) / chunk_number)} chunks generated - Enter the number of the chunk you want to work on: '))
    # typo prevention
    except:
        target_chunk = int(input(
            f'>>> Try again - {math.ceil(len(f) / chunk_number)} chunks generated - Enter the number of the chunk you want to work on: '))
    while target_chunk > math.ceil(len(f) / 20):
        target_chunk = int(input(
            f'>>> Try again - {math.ceil(len(f) / chunk_number)} chunks generated - Enter the number of the chunk you want to work on: '))
        

    # do the split
    locale_chunk = asm.chunks(f, chunk_number)


    # skip through chunks that we don't need
    _i = 1
    while _i < target_chunk:
        next(locale_chunk)
        _i += 1
    # this next iteration is the chunk we want to work with
    locale_chunk = next(locale_chunk)


    # for debuging purposes
    print(locale_chunk)


# ------------------------------------------------------ #


### WORK WITH EACH LOCALE ###


for (i, locale) in enumerate(locale_chunk, start=1):


    # skip if null string
    if locale == '':
        continue


    # sanitize and print current locale
    locale = locale.strip()
    print(f'\nProcessing locale {i} of {len(locale_chunk)} : {locale}')


    # load OSM and search for the locale
    create_driver()
    osm_check(locale, data)


# ------------------------------------------------------ #


### EXPORT THE DATA ###


# quit the browser
# driver.quit()


# ------------------------------------------------------ #
