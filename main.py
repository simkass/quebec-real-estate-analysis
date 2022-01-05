from quebec_real_estate.duproprio_web_scraper import parse_listing_urls

def main():
    parse_listing_urls('data/raw/listings_URLs.txt', start_page=10438)

if __name__ == '__main__':
    main()