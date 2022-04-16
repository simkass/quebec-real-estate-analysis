from scripts.duproprio_urls_scraper import scrape_listing_urls
from scripts.dupropio_listings_scraper import scrape_listings
import config

if __name__ == '__main__':
    # Scrape Family Home Listings (9158 pages on Duproprio, 2021 starts at 174)
    scrape_listing_urls('data/raw/home_listings_urls.txt', config.home_url_base, 174, 9158)
    scrape_listings(config.home_subtypes, 'data/raw/home_listings_urls.txt', 'data/raw/home_raw_listings.csv')

    # Scrape Condo Listings (2705 pages on Duproprio, 2021 starts at 74)
    scrape_listing_urls('../data/raw/condo_listings_urls.txt', config.condo_url_base, 74, 2705)
    scrape_listings(config.home_subtypes, 'data/raw/condo_listings_urls.txt', 'data/raw/condo_raw_listings.csv')
