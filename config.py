# URL values
home_url_base = 'https://duproprio.com/en/search/list?search=true&type%5B0%5D=house&subtype%5B0%5D=1&subtype%5B1%5D=2&subtype%5B2%5D=4&subtype%5B3%5D=5&subtype%5B4%5D=6&subtype%5B5%5D=7&subtype%5B6%5D=9&subtype%5B7%5D=10&subtype%5B8%5D=11&subtype%5B9%5D=13&subtype%5B10%5D=15&subtype%5B11%5D=17&subtype%5B12%5D=19&subtype%5B13%5D=21&subtype%5B14%5D=97&subtype%5B15%5D=99&subtype%5B16%5D=100&is_sold=1&with_builders=1&parent=1&pageNumber='
condo_url_base = 'https://duproprio.com/en/search/list?search=true&subtype%5B0%5D=14&subtype%5B1%5D=12&subtype%5B2%5D=3&is_sold=1&with_builders=1&parent=1&pageNumber='
url_end = '&sort=-published_at'

# Data columns of values to parse in page
data_columns = ['subtype', 'style', 'living_area', 'lot_dimensions', 'bedrooms', 'bathrooms', 'levels',
                'location', 'listing_date', 'year_of_construction', 'municipal_eval', 'price']

# Subtypes html-tag/value pairs
home_subtypes = [['bungalow', 'semi-detached', 'hab-2-storey',
                 '1-12-storey', 'split-level', 'townhouse',
                  'country-home', 'mobile-home', 'acreage-hobby-farm-ranch',
                  'villa', 'raised-bungalow', '3-storey', 'manufactured-home',
                  '4-storey', 'hab-misc', 'bi-level', 'bi-generation'],
                 ['Bungalow', 'Semi-detached', '2 Storey',
                 '1 1/2 Storey', 'Split Level', 'Townhouse', 'Country Home',
                  'Mobile home', 'Acreage / Hobby Farm / Ranch', 'Villa',
                  'Raised Bungalow', '3 Storey', 'Manufactured home', '4 Storey',
                  'Misc.', 'Bi-Level', 'Bi-generation']]

condo_subtypes = [['hab-condominium', 'hab-loft',
                   'hab-penthouse'], ['Condominium', 'Loft', 'Penthouse']]
