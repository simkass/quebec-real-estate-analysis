from scripts.duproprio_urls_scraper import scrape_listing_urls
from scripts.dupropio_listings_scraper import scrape_listings
import config

if __name__ == '__main__':
    # Scrape Family Home Listings (269 pages on Duproprio)
    scrape_listing_urls('../data/raw/home_listings_urls.txt', config.home_url_base, 1, 269)
    scrape_listings(config.home_subtypes, '../data/raw/home_listings_urls.txt', '../data/raw1/home_raw_listings.csv')

    # Scrape Condo Listings (122 pages on Duproprio)
    scrape_listing_urls('../data/raw/condo_listings_urls.txt', config.home_url_base, 1, 122)
    scrape_listings(config.home_subtypes, '../data/raw/condo_listings_urls.txt', '../data/raw1/condo_raw_listings.csv')
