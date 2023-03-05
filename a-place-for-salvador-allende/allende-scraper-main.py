# web scraping tutorial courtesy of https://www.educative.io/blog/python-web-scraping-tutorial


from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from types import NoneType
import os
import re
import pandas as pd


# countries with a Salvador Allende presence, according to http://www.abacq.org/calle/index.php?toc/toc
allende_countries = {
    'Alemania'                  : 'Germany',
    'Angola'                    : 'Angola',
    'Arabia Saudita'            : 'Saudi Arabia',
    'Argelia'                   : 'Algeria',
    'Argentina'                 : 'Argentina',
    'Australia'                 : 'Australia',
    'Austria'                   : 'Austria',
    'Bélgica'                   : 'Belgium',
    'Bosnia-Herzegovina'        : 'Bosnia and Herzegovina',
    'Brasil'                    : 'Brazil',
    'Bulgaria'                  : 'Bulgaria',
    'Canadá'                    : 'Canada',
    'Chile'                     : 'Chile',
    'Colombia'                  : 'Colombia',
    'Cuba'                      : 'Cuba',
    'Dinamarca'                 : 'Denmark',
    'Ecuador'                   : 'Ecuador',
    'Eslovaquia'                : 'Slovakia',
    'España'                    : 'Spain',
    'Estados Unidos'            : 'United States',
    'Francia'                   : 'France',
    'Guinea-Bissáu'             : 'Guinea-Bissau',
    'Holanda'                   : 'Netherlands',
    'Hungría'                   : 'Hungary',
    'India'                     : 'India',
    'Irán'                      : 'Iran',
    'Israel'                    : 'Israel',
    'Italia'                    : 'Italy',
    'Luxemburgo'                : 'Luxembourg',
    'México'                    : 'Mexico',
    'Mozambique'                : 'Mozambique',
    'Nicaragua'                 : 'Nicaragua',
    'Pakistán'                  : 'Pakistan',
    'Palestina'                 : 'Palestine',
    'Paraguay'                  : 'Paraguay',
    'Perú'                      : 'Peru',
    'Portugal'                  : 'Portugal',
    'Reino Unido'               : 'United Kingdom',
    'República Checa'           : 'Czechia',
    'República del Congo'       : 'Republic of the Congo',
    'República de Macedonia'    : 'North Macedonia',
    'República Dominicana'      : 'Dominican Republic',
    'Rusia'                     : 'Russia',
    'Salvador'                  : 'El Salvador',
    'Serbia'                    : 'Serbia',
    'Turquía'                   : 'Turkey',
    'Uruguay'                   : 'Uruguay',
    'Venezuela'                 : 'Venezuela'
}


country_to_region = {
    'Alemania'                  : 'Europe',
    'Angola'                    : 'Africa',
    'Arabia Saudita'            : 'Middle East',
    'Argelia'                   : 'Africa',
    'Argentina'                 : 'South America',
    'Australia'                 : 'ANZ and Oceania',
    'Austria'                   : 'Europe',
    'Bélgica'                   : 'Europe',
    'Bosnia-Herzegovina'        : 'Europe',
    'Brasil'                    : 'South America',
    'Bulgaria'                  : 'Europe',
    'Canadá'                    : 'North America',
    'Chile'                     : 'South America',
    'Colombia'                  : 'South America',
    'Cuba'                      : 'Central America',
    'Dinamarca'                 : 'Europe',
    'Ecuador'                   : 'South America',
    'Eslovaquia'                : 'Europe',
    'España'                    : 'Europe',
    'Estados Unidos'            : 'North America',
    'Francia'                   : 'Europe',
    'Guinea-Bissáu'             : 'Africa',
    'Holanda'                   : 'Europe',
    'Hungría'                   : 'Europe',
    'India'                     : 'Asia',
    'Irán'                      : 'Asia',
    'Israel'                    : 'Middle East',
    'Italia'                    : 'Europe',
    'Luxemburgo'                : 'Europe',
    'México'                    : 'North America',
    'Mozambique'                : 'Africa',
    'Nicaragua'                 : 'Central America',
    'Pakistán'                  : 'Asia',
    'Palestina'                 : 'Middle East',
    'Paraguay'                  : 'South America',
    'Perú'                      : 'South America',
    'Portugal'                  : 'Europe',
    'Reino Unido'               : 'Europe',
    'República Checa'           : 'Europe',
    'República del Congo'       : 'Africa',
    'República de Macedonia'    : 'Europe',
    'República Dominicana'      : 'Central America',
    'Rusia'                     : 'Europe',
    'Salvador'                  : 'Central America',
    'Serbia'                    : 'Europe',
    'Turquía'                   : 'Middle East',
    'Uruguay'                   : 'South America',
    'Venezuela'                 : 'South America'
}


# non-exhaustive lists of words that correspond to a specific type of establishment
types = {
    'street'                : ['calle', 'avenida', 'pasaje', 'rue', 'rua', 'avenue', 'circunvalación', 'boulevard', 'bulevar', 'street', 'straat', 'strada'],
    'monument'              : ['monumento', 'escultura', 'monument', 'sculpture', 'busto', 'bust'],
    'park'                  : ['plaza', 'parque', 'square', 'park', 'place', 'plazoleta'],
    'school'                : ['escuela', 'colegio', 'school', 'schule', 'école'],
    'healthcare facility'   : ['hospital', 'salud'],
    'bridge'                : ['puente', 'bridge', 'pont', 'brücke'],
    'sports center'         : ['complexe sportif', 'sports complex', 'complejo de deporte'],
    'multipurpose center'   : ['espace', 'hall'],
    'port'                  : ['puerto', 'port'],
    'neighborhood'          : ['población', 'village']
}


months = {
    'enero'         : int(1),
    'febrero'       : int(2),
    'marzo'         : int(3),
    'abril'         : int(4),
    'mayo'          : int(5),
    'junio'         : int(6),
    'julio'         : int(7),
    'agosto'        : int(8),
    'septiembre'    : int(9),
    'octubre'       : int(10),
    'noviembre'     : int(11),
    'diciembre'     : int(12),
    '01'            : int(1),
    '02'            : int(2),
    '03'            : int(3),
    '04'            : int(4),
    '05'            : int(5),
    '06'            : int(6),
    '07'            : int(7),
    '08'            : int(8),
    '09'            : int(9),
    '10'            : int(10),
    '11'            : int(11),
    '12'            : int(12)
}


days = {
    '01'    : int(1),
    '02'    : int(2),
    '03'    : int(3),
    '04'    : int(4),
    '05'    : int(5),
    '06'    : int(6),
    '07'    : int(7),
    '08'    : int(8),
    '09'    : int(9)
}



# ------------------------------------------------------ #



### 1. RETRIEVE ALL LINKS ###


# create a Google Chrome driver object
# https://stackoverflow.com/questions/69918148/deprecationwarning-executable-path-has-been-deprecated-please-pass-in-a-servic
s = Service('C:\\Users\\canogle\\.cache\\selenium\\chromedriver\\win32\\110.0.5481.77\\chromedriver.exe')
driver = webdriver.Chrome(service=s)


# base URLs
homepage = 'http://www.abacq.org'
toc = 'http://www.abacq.org/calle/index.php?toc/toc'


# fetch all urls from the site map
driver.get(toc)
soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer("div", id="toc"))


# all links are under an <li> tag
links_soup = soup.find_all("li")
print(f'>>> Parsing the site map {toc}...\n')
# print(links_soup, '\n')


# create a list of bare links
links_list = []

for link in links_soup:
    link = str(link)
    link = re.search(r'(\/calle\/index.php\?\d{4}\/\d{2}\/\d{2}\/\d*(?:-\w*)*)', link)
    link = str(homepage) + str(link.group(1))
    links_list.append(link)
print('>>> Fetching all links...')
print(f'{str(len(links_list))} links found.\n')
# print(links_list, '\n')



# ------------------------------------------------------ #



### 2. GROUP LINKS BY COUNTRY ###


countries_links = {
    'Alemania'                  : [],
    'Angola'                    : [],
    'Arabia Saudita'            : [],
    'Argelia'                   : [],
    'Argentina'                 : [],
    'Australia'                 : [],
    'Austria'                   : [],
    'Bélgica'                   : [],
    'Bosnia-Herzegovina'        : [],
    'Brasil'                    : [],
    'Bulgaria'                  : [],
    'Canadá'                    : [],
    'Chile'                     : [],
    'Colombia'                  : [],
    'Cuba'                      : [],
    'Dinamarca'                 : [],
    'Ecuador'                   : [],
    'Eslovaquia'                : [],
    'España'                    : [],
    'Estados Unidos'            : [],
    'Francia'                   : [],
    'Guinea-Bissáu'             : [],
    'Holanda'                   : [],
    'Hungría'                   : [],
    'India'                     : [],
    'Irán'                      : [],
    'Israel'                    : [],
    'Italia'                    : [],
    'Luxemburgo'                : [],
    'México'                    : [],
    'Mozambique'                : [],
    'Nicaragua'                 : [],
    'Pakistán'                  : [],
    'Palestina'                 : [],
    'Paraguay'                  : [],
    'Perú'                      : [],
    'Portugal'                  : [],
    'Reino Unido'               : [],
    'República Checa'           : [],
    'República del Congo'       : [],
    'República de Macedonia'    : [],
    'República Dominicana'      : [],
    'Rusia'                     : [],
    'Salvador'                  : [],
    'Serbia'                    : [],
    'Turquía'                   : [],
    'Uruguay'                   : [],
    'Venezuela'                 : []
}


# assign links according to the country in their url
for link in links_list:
    for key in allende_countries.keys():
        if key.lower() in link:
            countries_links[key].append(link)


# enter here the country name (in Spanish) you want to do
country = 'Dinamarca'


# retrieve the links for that country
print(f'>>> Fetching links for {allende_countries[country]}...')
# print(countries_links[country])


# most links have the format http://www.abacq.org/calle/index.php?2009/11/06/435-sierra-gorda-chile
# this corresponds to one locale in one country.
# links with this format http://www.abacq.org/calle/index.php?2009/01/08/303-chile
# contains multiple locales within one country.
#
# sort links according to whether they're single-locale or multi-locale

single_locale = []
multi_locale = []

for link in countries_links[country]:
    link_check = re.search(r'(\/calle\/index.php\?\d{4}\/\d{2}\/\d{2}\/\d*(?:-\w*){2,})', link)
    if isinstance(link_check, NoneType):
        multi_locale.append(link)
    else:
        single_locale.append(link)

print(f'{str(len(countries_links[country]))} links found: {str(len(single_locale))} single-locale, {str(len(multi_locale))} multi-locale.\n')
print(f'Single-locale links:\n{single_locale}\n')
print(f'Multi-locale links:\n{multi_locale}\n')



# ------------------------------------------------------ #



### 3. SCRAPE EVERY LINK IN A BATCH ###


### WHAT TO COLLECT ###

# for each post, let's collect the following and connect them with the existing columns from the current db:
# name - image_alt - <img alt=[alt]>
# type - derived from the post's name and/or text
# _region - derived from country_to_region
# country - country - regex-ed from post title <h2 class="post-title">
# locale - <strong>
# oldest_known_year,month,day - scraped from the post's text
# desc - desc - <em>
# abacq-reference - post_url - <h2><a href=[]>


# create a dictionary of lists that's easily translatable into our existing db
data = {
    'name'                       : [],
    'type'                       : [],
    'region'                     : [],
    'country'                    : [],
    'locale_1'                   : [],
    'oldest_known_year'          : [],
    'oldest_known_month'         : [],
    'oldest_known_day'           : [],
    'desc'                       : [],
    'abacq_reference'            : [],
}



# ------------------------------------------------------ #



### SINGLE-LOCALE SCRAPER ###


# every link is basically an article so we'll retrieve their contents
for (i, link) in enumerate(single_locale, start=1):
    driver.get(link)
    #
    # we are only interested in the article itself, not the comments, sidebar, etc.
    #
    article_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
        "div", class_="post"), from_encoding='windows-1252', exclude_encodings=['unicode', 'utf-8'])
    print(f'\n>>> Parsing single-locale article {str(i)} of {str(len(single_locale))}: {link}...\n')
    text = article_soup.get_text()
    lower_text = text.lower()
    print(text)
    #
    # get NAME
    #
    name = article_soup.find("img", alt=True)
    name = str(name)
    name = re.search(r'alt="(.*?)"\s*', name)
    try:
        str(name.group(1))
    except:
        # fallback for when the article has no alt text for the main image for some reason
        name = 'A memorial to Salvador Allende'
    else:
        name = str(name.group(1))
    data['name'].append(name)
    print(f'Name: {name}')
    #
    # get TYPE
    # the dict used here is pretty rudimentary so this is prone to errors and needs human verification
    #
    type = ''
    for key, value in types.items():
        for item in value:
            if item in name.lower():
                type = key
    data['type'].append(type)
    print(f'Type: {type}')
    #
    # get COUNTRY
    #
    country_es = article_soup.find("h2", class_="post-title")
    country_es = str(country_es)
    country_es = re.search(r'(?:\.|,)\s*(.*)<\/h2>', country_es)
    country_es = str(country_es.group(1))
    country_en = allende_countries[country_es]
    data['country'].append(country_en)
    print(f'Country: {country_en}')
    #
    # get REGION
    #
    region = country_to_region[country_es]
    data['region'].append(region)
    print(f'Region: {region}')
    #
    # get LOCALE_1
    #
    locale_1 = article_soup.find("strong")
    locale_1 = str(locale_1)
    locale_1 = re.search(r'<strong>(.*)<\/strong>', locale_1)
    try:
        str(locale_1.group(1))
    except:
        locale_1 = article_soup.find("h2", class_="post-title")
        locale_1 = str(locale_1)
        locale_1 = re.search(r'<h2 class="post-title">(.*)(?:\.|,)\s*.*<\/h2>', locale_1)
        locale_1 = str(locale_1.group(1))
    else:
        locale_1 = str(locale_1.group(1))
    data['locale_1'].append(locale_1)
    print(f'Locale: {locale_1}')
    #
    # get OLDEST_KNOWN_YEAR
    # retrieve the year from the url; when an older year is found within the text, get that instead
    #
    oldest_known_year = re.search(r'(\d{4})', link)
    oldest_known_year = int(oldest_known_year.group(1))
    years_in_text = re.findall(r'\d{4}', text)
    years_in_text = list(years_in_text)
    for year in years_in_text:
        year = int(year)
        if year < oldest_known_year and year > int(1973):
            oldest_known_year = year
    data['oldest_known_year'].append(oldest_known_year)
    print(f'Oldest known year: {oldest_known_year}')
    #
    # get OLDEST_KNOWN_MONTH
    # retrieve the month from the url; when another month is found within the text, get that instead
    # unlike in oldest_known_year (more straightforward), we will list all months in the text if they're not the same as the one in the url
    #
    oldest_known_month = re.search(r'\d{4}\/(\d{2})\/\d{2}', link)
    oldest_known_month = months[oldest_known_month.group(1)]
    # compare oldest_known_year to the year in the url.
    # if they're different (i.e. we derived the year from the text), we'll proceed with collecting months_in_text.
    year_in_url = re.search(r'(\d{4})', link)
    year_in_url = int(year_in_url.group(1))
    months_in_text = re.findall(
        r'(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)', lower_text)
    months_in_text = list(months_in_text)
    if oldest_known_year != year_in_url and len(months_in_text) == 0:
        oldest_known_month = ''
    elif oldest_known_year != year_in_url and len(months_in_text) > 0:
        for month in months_in_text:
            list_months = []
            month = months[month]
            list_months.append(month)
        oldest_known_month = list_months
    data['oldest_known_month'].append(oldest_known_month)
    print(f'Oldest known month: {oldest_known_month}')
    #
    # get OLDEST_KNOWN_DAY
    # retrieve the day from the url; when another day is found within the text, get that instead
    # unlike in oldest_known_year (more straightforward), we will list all days in the text if they're not the same as the one in the url
    #
    oldest_known_day = re.search(r'\d{4}\/\d{2}\/(\d{2})', link)
    oldest_known_day = str(oldest_known_day.group(1))
    if oldest_known_day in list(days.keys()):
        oldest_known_day = days[oldest_known_day]
    else:
        oldest_known_day = int(oldest_known_day)
        # compare oldest_known_year to the year in the url.
        # if they're different (i.e. we derived the year from the text), we'll proceed with collecting days_in_text.
    days_in_text = re.findall(r'(\d{1,2})\s+', lower_text)
    days_in_text = list(days_in_text)
    # remove numbers that are invalid days of a month
    for day in days_in_text:
        if int(day) > int(32):
            days_in_text.remove(day)
    if oldest_known_year != year_in_url and len(days_in_text) == 0:
        oldest_known_day = ''
    elif oldest_known_year != year_in_url and len(days_in_text) > 0:
        for day in days_in_text:
            list_days = []
            if day in list(days.keys()):
                day = days[day]
            else:
                day = int(day)
            list_days.append(day)
        oldest_known_day = list_days
    data['oldest_known_day'].append(oldest_known_day)
    print(f'Oldest known day: {oldest_known_day}')
    #
    # get DESC
    #
    desc = ''
    desc_soup = article_soup.find_all("em")
    desc_soup = list(desc_soup)
    for item in desc_soup:
        item = str(item)
        item = item.strip('</em>')
        desc += item + '\n'
    data['desc'].append(desc)
    print(f'Desc: {desc}')
    #
    # get ABACQ_REFERENCE
    # basically the url we're working with
    #
    data['abacq_reference'].append(link)



# ------------------------------------------------------ #



### MULTI-LOCALE SCRAPER ###


# every link is basically an article so we'll retrieve their contents
for (i, link) in enumerate(multi_locale, start=1):
    driver.get(link)
    #
    # we are only interested in the article itself, not the comments, sidebar, etc.
    #
    article_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer(
        "div", class_="post"), from_encoding='windows-1252', exclude_encodings=['unicode', 'utf-8'])
    print(f'\n>>> Parsing multi-locale article {str(i)} of {str(len(multi_locale))}: {link}...\n')
    text = article_soup.get_text()
    lower_text = text.lower()
    print(text)
    #
    # honestly, the multi-locale articles are less organized but are concise enough for manual human investigation.
    # each locale is still within <strong> tags so we'll take advantage of those
    #
    # get all LOCALE_1
    #
    locale_1_soup = article_soup.find_all("strong")
    locale_1_soup = list(locale_1_soup)
    locale_1 = []
    for item in locale_1_soup:
        item = str(item)
        item = re.search(r'<strong>(.*)<\/strong>', item)
        item = str(item.group(1))
        locale_1.append(item)
    # for each LOCALE_1, give them the same information as the rest of the article
    for item in locale_1:
        #
        # get NAME
        #
        name = 'A memorial to Salvador Allende'
        data['name'].append(name)
        print(f'Name: {name}')
        #
        # get TYPE
        # the dict used here is pretty rudimentary so this is prone to errors and needs human verification
        #
        type = ''
        data['type'].append(type)
        print(f'Type: {type}')
        #
        # get COUNTRY
        #
        country_es = article_soup.find("h2", class_="post-title")
        country_es = str(country_es)
        country_es = re.search(r'<h2 class="post-title">(.*?)(?:\s*\.*)*<\/h2>', country_es)
        country_es = str(country_es.group(1))
        country_en = allende_countries[country_es]
        data['country'].append(country_en)
        print(f'Country: {country_en}')
        #
        # get REGION
        #
        region = country_to_region[country_es]
        data['region'].append(region)
        print(f'Region: {region}')
        #
        # get LOCALE_1
        #
        data['locale_1'].append(item)
        print(f'Locale: {item}')
        #
        # get OLDEST_KNOWN_YEAR
        # retrieve the year from the url; when an older year is found within the text, get that instead
        #
        oldest_known_year = re.search(r'(\d{4})', link)
        oldest_known_year = int(oldest_known_year.group(1))
        years_in_text = re.findall(r'\d{4}', text)
        years_in_text = list(years_in_text)
        for year in years_in_text:
            year = int(year)
            if year < oldest_known_year and year > int(1973):
                oldest_known_year = year
        data['oldest_known_year'].append(oldest_known_year)
        print(f'Oldest known year: {oldest_known_year}')
        #
        # get OLDEST_KNOWN_MONTH
        # retrieve the month from the url; when another month is found within the text, get that instead
        # unlike in oldest_known_year (more straightforward), we will list all months in the text if they're not the same as the one in the url
        #
        oldest_known_month = re.search(r'\d{4}\/(\d{2})\/\d{2}', link)
        oldest_known_month = months[oldest_known_month.group(1)]
        # compare oldest_known_year to the year in the url.
        # if they're different (i.e. we derived the year from the text), we'll proceed with collecting months_in_text.
        year_in_url = re.search(r'(\d{4})', link)
        year_in_url = int(year_in_url.group(1))
        months_in_text = re.findall(
            r'(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)', lower_text)
        months_in_text = list(months_in_text)
        if oldest_known_year != year_in_url and len(months_in_text) == 0:
            oldest_known_month = ''
        elif oldest_known_year != year_in_url and len(months_in_text) > 0:
            for month in months_in_text:
                list_months = []
                month = months[month]
                list_months.append(month)
            oldest_known_month = list_months
        data['oldest_known_month'].append(oldest_known_month)
        print(f'Oldest known month: {oldest_known_month}')
        #
        # get OLDEST_KNOWN_DAY
        # retrieve the day from the url; when another day is found within the text, get that instead
        # unlike in oldest_known_year (more straightforward), we will list all days in the text if they're not the same as the one in the url
        #
        oldest_known_day = re.search(r'\d{4}\/\d{2}\/(\d{2})', link)
        oldest_known_day = str(oldest_known_day.group(1))
        if oldest_known_day in list(days.keys()):
            oldest_known_day = days[oldest_known_day]
        else:
            oldest_known_day = int(oldest_known_day)
            # compare oldest_known_year to the year in the url.
            # if they're different (i.e. we derived the year from the text), we'll proceed with collecting days_in_text.
        days_in_text = re.findall(r'(\d{1,2})\s+', lower_text)
        days_in_text = list(days_in_text)
        # remove numbers that are invalid days of a month
        for day in days_in_text:
            if int(day) > int(32):
                days_in_text.remove(day)
        if oldest_known_year != year_in_url and len(days_in_text) == 0:
            oldest_known_day = ''
        elif oldest_known_year != year_in_url and len(days_in_text) > 0:
            for day in days_in_text:
                list_days = []
                if day in list(days.keys()):
                    day = days[day]
                else:
                    day = int(day)
                list_days.append(day)
            oldest_known_day = list_days
        data['oldest_known_day'].append(oldest_known_day)
        print(f'Oldest known day: {oldest_known_day}')
        #
        # get DESC
        #
        desc = ''
        data['desc'].append(desc)
        print(f'Desc: {desc}\n')
        #
        # get ABACQ_REFERENCE
        # basically the url we're working with
        #
        data['abacq_reference'].append(link)


# ------------------------------------------------------ #


### EXPORT THE DATA ###


# create a dataframe of all info collected
data_df = pd.DataFrame(data=data)
print('\nDataFrame created:\n')
print(data_df)

# export dataframe to csv
data_df.to_csv(f'a-place-for-salvador-allende/{allende_countries[country]}.csv', index=False)



# ------------------------------------------------------ #



### A REMARK ON CHARACTER ENCODING ###


# I don't know how to fix the replacement characters (question marks) because the website's encoding is messed up.
# here https://www.i18nqa.com/debug/utf8-debug.html there is a table for the correct characters vs. how they are printed in the csv.