from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller as chromedriver
import re


s = Service(chromedriver.install())
driver = webdriver.Chrome(service=s)


locale_1 = 'Pedro Aguirre Cerda'
country_en = 'Chile'


def osm_check():
    global locale_1
    #
    # when we have this abacq locale, we then cross-check this with OpenStreetMap
    #
    locale_link = f'https://www.openstreetmap.org/search?query=Salvador%20Allende%20{locale_1}%20{country_en}'
    driver.get(locale_link)
    osm_soup = BeautifulSoup(driver.page_source, 'html.parser', parse_only=SoupStrainer("ul", class_="results-list list-group list-group-flush"))

    #
    # go through each search result and have the user verify it
    #
    locale_results_list = list(osm_soup.find_all("a", class_="set_position"))
    print(f'locale_results_list: {len(locale_results_list)} items.\n')
    for (i, item) in enumerate(locale_results_list, start=1):
        print(f'{i} -- {item}')
    #
    # a single result looks like this - we can derive lots of info from here once user verifies that it looks good
    #
    # <a class="set_position" data-lat="-12.1102763" data-lon="-77.0104283"
    # data-min-lat="-12.1103037" data-max-lat="-12.1102452" data-min-lon="-77.0109212" data-max-lon="-77.0097999"
    # data-prefix="Residential Road" data-name="Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru"
    # data-type="way" data-id="426845566" href="/way/426845566">Salvador Allende, Villa Victoria, Surquillo, Province of Lima, Lima Metropolitan Area, Lima, 15000, Peru</a>
    #
    if len(locale_results_list) == 0:
        print('\nNo addresses found in OpenStreetMap. Will use the locale derived from the article...')
        # data['locale_1'].append(locale_1)
        print(f'Locale 1: {locale_1}')
        # clear the previous entry's osm_address and osm_info so that it doesn't get copied into the current entry
        global osm_address
        osm_address = ''
        global osm_info
        osm_info = ''
    else:
        print(f'\n{str(len(locale_results_list))} possible address(es) found in OpenStreetMap.\n')
        for result in locale_results_list:
            result = str(result)
            osm_address = re.search(r'data-name="(.*?)"', result)
            osm_address = str(osm_address.group(1))
            #
            # have user verify the address - this decides what this loop should do next
            #
            print(f'Please verify if this address matches the place in this article:\n{osm_address}')
            user_verification = input('>>> Type y if yes, n if no: ')
            if user_verification == 'n' and len(locale_results_list) == 1:
                print('OpenStreetMap address does not match the place in this article. Will use the locale derived from the article...')
                # clear the previous entry's osm_address and osm_info so that it doesn't get copied into the current entry
                osm_address = ''
                osm_info = ''
                # data['locale_1'].append(locale_1)
                print(f'Locale 1: {locale_1}')
                break
            elif user_verification == 'n' and len(locale_results_list) > 1:
                # clear the previous entry's osm_address and osm_info so that it doesn't get copied into the current entry
                osm_address = ''
                osm_info = ''
                continue
            elif user_verification == 'y':
                # we'll save the whole result in a variable for later parsing. we can then close the loop.
                osm_info = result
                break


osm_check()


print(f'\nosm_info: {osm_info}')
print(f'\nosm_address: {osm_address}')

