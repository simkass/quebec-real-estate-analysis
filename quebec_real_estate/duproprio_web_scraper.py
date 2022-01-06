import os.path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import URL_base, URL_end


def format(text):
    return text.replace('\n', '').replace('$', '').replace(',', '').replace(' ', '')


def format_dimensions(text):
    text = text.replace('\n', '').replace(',', '').replace(' ', '').split('f')[0]
    if 'x' in text:
        values = text.split('x')
        return int(float(values[0]) * float(values[1]))
    return text


def format_location(text):
    text = text.replace('\n', '').replace(',', '').split('(')[0].split('/')[0]
    return ' '.join(text.split())


def format_price(text):
    text = format(text)
    if text == '':
        return None
    else:
        return text


def find_style(soup):
    div = soup.find('div', text='Property Style')
    if div is not None:
        return div.find_next_sibling('div').find_next_sibling('div').text
    else:
        return None


def find_lot_dimensions(soup):
    div = soup.find(
        'div', class_='listing-main-characteristics__item listing-main-characteristics__item--lot-dimensions')
    if div is not None:
        return format_dimensions(div.find('span').find_next_sibling('span').text)
    else:
        return None


def find_living_area(soup):
    div = soup.find(
        'div', class_='listing-main-characteristics__item-dimensions')
    if div is not None:
        value = format_dimensions(
            div.find('span').find_next_sibling('span').text)
    else:
        value = '??'
    if value == find_lot_dimensions(soup):
        div = soup.find('div', text='Building dimensions')
        if div is not None:
            return format_dimensions((div.find_next_sibling('div').find_next_sibling('div').text))
        else:
            return None
    return value


def find_icon_description(soup, parameter):
    descriptions = soup.findAll(
        'div', class_='listing-main-characteristics__label')
    for desc in descriptions:
        if parameter in desc.text:
            return format(desc.find('span').text)
    return None


def find_location(soup):
    div = soup.find('div', class_='listing-location__address')
    if div is not None:
        return format_location((div.find('a').text))
    else:
        return None


def find_listing_date(soup):
    photo_link = 'for_sale/'
    metas = soup.findAll(name='meta')
    for meta in metas[1:]:
        if photo_link in meta['content']:
            date = meta['content']
            date = date.split(photo_link)[1].split('/')
            return date[0]
    return None


def find_year_of_construction(soup):
    div = soup.find('div', text='Year of construction')
    if div is not None:
        return format((div.find_next_sibling('div').find_next_sibling('div').text))
    else:
        return None


def find_municipal_eval(soup):
    div = soup.find('div', text='Municipal Assessment')
    if div is not None:
        return format((div.find_next_sibling('div').find_next_sibling('div').text))
    else:
        return None


def find_price(soup):
    div = soup.find('div', class_='listing-price__amount')
    if div is not None:
        return format_price(div.next_element)
    else:
        return None


def append_to_csv(filename, page_content):
    df = pd.DataFrame([page_content])

    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False)
    else:
        df.to_csv(filename)


def parse_page_listing_urls(filename, page, page_num):
    soup = BeautifulSoup(page.content, 'html.parser')

    links = 0
    for a in soup.find_all('a', href=True, class_='search-results-listings-list__item-image-link'):
        with open(filename, 'a') as f:
            f.write(str(a['href']) + '\n')
        links += 1
    print('Parsed ' + str(links) + ' listing URLs from page ' + str(page_num))


def parse_listing_urls(filename, start_page = 1, end_page = 12800):
    for i in range(start_page, end_page):
        URL = URL_base + str(i) + URL_end
        page = requests.get(URL)

        if page.status_code == 200:
            parse_page_listing_urls(filename, page, i)


def parse_listing(URL, filename):
    page = requests.get(URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        page_content = {
            'style': find_style(soup),
            'living_area': find_living_area(soup),
            'lot_dimensions': find_lot_dimensions(soup),
            'bedrooms': find_icon_description(soup, 'bedroom'),
            'bathrooms': find_icon_description(soup, 'bathroom'),
            'levels': find_icon_description(soup, 'level'),
            'location': find_location(soup),
            'listing_date': find_listing_date(soup),
            'year_of_construction': find_year_of_construction(soup),
            'municipal_eval': find_municipal_eval(soup),
            'price': find_price(soup),
        }

        append_to_csv(filename, page_content)


def parse_listings(URLs_filename, output_filename):
    for url in open(URLs_filename, 'r'):
        parse_listing(url[:-1], output_filename)
