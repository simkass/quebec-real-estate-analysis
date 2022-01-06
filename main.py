from quebec_real_estate.duproprio_web_scraper import parse_listing_urls, parse_listings

def main():
    # parse_listing_urls('data/raw/listings_URLs.txt', start_page=10438)
    parse_listings('data/raw/listings_URLs.txt', 'data/raw/raw_listings.csv')

if __name__ == '__main__':
    main()