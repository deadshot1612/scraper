from scraper import Scraper


uri_dict = {
    'Cafe in Tashkent': 'https://www.goldenpages.uz/rubrics/?Id=3478',
    'Pools in Tashkent':'https://www.goldenpages.uz/rubrics/?Id=1039',
    'Restaurants in Tashkent':'https://www.goldenpages.uz/rubrics/?Id=3473',
    'Fast Food in Tashkent':'https://www.goldenpages.uz/rubrics/?Id=3742',
    'Entertainment centers in Tashkent': 'https://www.goldenpages.uz/rubrics/?Id=3770',
    'Bars in Tashkent':'https://www.goldenpages.uz/rubrics/?Id=3776',
    'Shopping and entertainment centers, complexes in Tashkent':'https://www.goldenpages.uz/rubrics/?Id=101709'
    }

for name, uri in uri_dict.items():

    scraper = Scraper(uri=uri, name=name)

    scraper.get_data()