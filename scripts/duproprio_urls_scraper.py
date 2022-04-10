# --------------------------------------------------------------------------------------------------
# duproprio_urls_scraper.py
# Web scraping script to acquire sold listing urls from duproprio.com.
# # --------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
from config import url_end


def scrape_listings_page(filename: str, page: requests.Response) -> int:
    """Parse all house listings from a single duproprio listings preview page.

    Args:
        filename (str): .txt file where listing urls are stored line by line.
        page (requests.Response): Listings preview page.

    Returns:
        int: Number of listings parsed from the page.
    """
    soup = BeautifulSoup(page.content, 'html.parser')

    links = 0
    for a in soup.find_all('a', href=True, class_='search-results-listings-list__item-image-link'):
        with open(filename, 'a') as f:
            f.write(str(a['href']) + '\n')
        links += 1

    return links


def scrape_listing_urls(filename: str, url_base: str, start_page: int, end_page: int):
    """Parse all house listings from duproprio listings preview pages between specified start and end.

    Args:
        filename (str): .txt file where listing urls are stored line by line.
        url_base (str): The base url (before the page index) for the listing preview pages.
        start_page (int): Start page index of the listing preview pages.
        end_page (int): End page index of the listing preview pages.
    """
    for i in range(start_page, end_page):
        page = requests.get(url_base + str(i) + url_end)

        if page.status_code == 200:
            links = scrape_listings_page(filename, page)
            print('Parsed ' + str(links) + ' listing URLs from page ' + str(i))
