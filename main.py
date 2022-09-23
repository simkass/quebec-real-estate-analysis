# --------------------------------------------------------------------------------------------------
# main.py
# Main program that runs the scraping scripts.
# --------------------------------------------------------------------------------------------------
# Author: Simon Kassab
# --------------------------------------------------------------------------------------------------

from scripts.duproprio_urls_scraper import scrape_listing_urls
from scripts.dupropio_listings_scraper import scrape_listings
import config

if __name__ == '__main__':
    # Scrape Family Home Listings (9158 pages on Duproprio, 2021 starts at 174)
    scrape_listing_urls('data/raw/home-listings-urls.txt', config.home_url_base, 174, 9158)
    scrape_listings(config.home_subtypes, 'data/raw/home-listings-urls.txt', 'data/raw/home-listings.csv', 99069)

    # Scrape Condo Listings (2705 pages on Duproprio, 2021 starts at 74)
    scrape_listing_urls('data/raw/condo-listings-urls.txt', config.condo_url_base, 74, 2705)
    scrape_listings(config.home_subtypes, 'data/raw/condo-listings-urls.txt', 'data/raw/condo-listings.csv', 29114)