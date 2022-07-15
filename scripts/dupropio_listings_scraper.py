# --------------------------------------------------------------------------------------------------
# duproprio_listings_scraper.py
# Web scraping script to acquire data on sold properties from a list of listing urls.
# --------------------------------------------------------------------------------------------------
# Author: Simon Kassab
# --------------------------------------------------------------------------------------------------

import os

import config
import pandas as pd
import requests
from bs4 import BeautifulSoup

def format(value: str):
    return value.replace('\n', '').replace('$', '').replace(',', '').replace(' ', '')


def format_dimensions(value: str):
    """Format dimension value by removing unwanted characters and executing relevant multiplications."""
    value = value.replace('\n', '').replace(',', '').replace(' ', '').split('f')[0]
    if 'x' in value:
        values = value.split('x')
        return int(float(values[0]) * float(values[1]))
    return value


def format_location(text):
    text = text.replace('\n', '').replace(',', '').split('(')[0].split('/')[0]
    return ' '.join(text.split())


def append_to_csv(output_filename: str, data: dict):
    df = pd.DataFrame([data])

    if os.path.isfile(output_filename):
        df.to_csv(output_filename, mode='a', header=False, index=False)
    else:
        df.to_csv(output_filename, index=False)


def parse_subtype(url, subtypes):
    """Parse home subtype from loaded page by finding the value in the url string."""
    indexes = [i for i in range(len(subtypes[0])) if subtypes[0][i] in url]
    return subtypes[1][indexes[0]] if len(indexes) != 0 else 'unknown'


def parse_style(soup: BeautifulSoup):
    """Parse home style from loaded page by finding the relevant html tag."""
    div = soup.find('div', text='Property Style')
    return div.find_next_sibling('div').find_next_sibling('div').text if div is not None else None


def parse_living_area(soup: BeautifulSoup):
    """Parse home living area from loaded page by finding the relevant html tag."""
    div = soup.find('div', class_='listing-main-characteristics__item-dimensions')
    value = format_dimensions(div.find('span').find_next_sibling('span').text) if div is not None else None

    if value == parse_lot_dimensions(soup):
        div = soup.find('div', text='Building dimensions')
        value = format_dimensions(div.find_next_sibling('div').find_next_sibling('div').text) if div is not None else None

    return value


def parse_lot_dimensions(soup: BeautifulSoup):
    """Parse home lot dimensions from loaded page by finding the relevant html tag."""
    div = soup.find('div', class_='listing-main-characteristics__item listing-main-characteristics__item--lot-dimensions')
    return format_dimensions(div.find('span').find_next_sibling('span').text) if div is not None else None


def parse_icon_description(soup: BeautifulSoup, icon: str):
    """Parse icon description values from loaded page by finding the relevant html tag and text (bedroom, bathroom etc.)."""
    descriptions = soup.findAll('div', class_='listing-main-characteristics__label')

    for desc in descriptions:
        if icon in desc.text:
            return format(desc.find('span').text)
    return None


def parse_location(soup: BeautifulSoup):
    """Parse home location from loaded page by finding the relevant html tag."""
    div = soup.find('div', class_='listing-location__address')
    return format_location(div.find('a').text) if div is not None else None


def parse_listing_date(soup: BeautifulSoup):
    """Parse home listing date from loaded page by finding the value in the picture links."""
    photo_link = 'for_sale/'
    metas = soup.findAll(name='meta')
    for meta in metas[1:]:
        if photo_link in meta['content']:
            date = meta['content']
            date = date.split(photo_link)[1].split('/')
            return date[0]
    return None


def parse_year_of_construction(soup: BeautifulSoup):
    """Parse home year of construction from loaded page by finding the relevant html tag."""
    div = soup.find('div', text='Year of construction')
    return format(div.find_next_sibling('div').find_next_sibling('div').text) if div is not None else None


def parse_municipal_eval(soup: BeautifulSoup):
    """Parse home municipal assessment from loaded page by finding the relevant html tag."""
    div = soup.find('div', text='Municipal Assessment')
    return format(div.find_next_sibling('div').find_next_sibling('div').text) if div is not None else None


def parse_price(soup: BeautifulSoup):
    """Parse home selling price from loaded page by finding the price html tag."""
    div = soup.find('div', class_='listing-price__amount')
    return format(div.next_element) if div is not None else None


def scrape_listing(url: str, subtypes: list, output_filename: str):
    """load and scrape single listing page from the provided url.

    Args:
        url (str): DuProprio url of the listing to scrape values from.
        subtypes (list): list of possible home subtypes.
        output_filename (str): name of the .csv output file.
    """    
    page = requests.get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        data = [
            parse_subtype(url, subtypes),
            parse_style(soup),
            parse_living_area(soup),
            parse_lot_dimensions(soup),
            parse_icon_description(soup, 'bedroom'),
            parse_icon_description(soup, 'bathroom'),
            parse_icon_description(soup, 'level'),
            parse_location(soup),
            parse_listing_date(soup),
            parse_year_of_construction(soup),
            parse_municipal_eval(soup),
            parse_price(soup)
        ]

        append_to_csv(output_filename, dict(zip(config.data_columns, data)))


def scrape_listings(subtypes: list, urls_filename: str, output_filename: str):
    """load and scrape pages from the provided file of listing urls. 

    Args:
        subtypes (list): list of possible property subtypes. 
        urls_filename (str): name of the file containing the listing urls. 
        output_filename (str): name of the .csv file where data will be stored. 
    """
    for url in open(urls_filename, 'r'):
        scrape_listing(url[:-1], subtypes, output_filename)
