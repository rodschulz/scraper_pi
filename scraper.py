import logging

import scrapy

logger = logging.getLogger()

URL_LAS_CONDES = 'https://www.portalinmobiliario.com/venta/casa/las-condes-metropolitana'
URL_PROVIDENCIA = 'https://www.portalinmobiliario.com/venta/casa/providencia-metropolitana'
URL_LA_REINA = 'https://www.portalinmobiliario.com/venta/casa/la-reina-metropolitana'
URL_NUNOA = 'https://www.portalinmobiliario.com/venta/casa/nunoa-metropolitana'

#TODO
# - UT link formats different (old urls) => https://www.portalinmobiliario.com/MLC-517628020-casa-en-venta-de-4-dormitorios-en-las-condes-_JM#position=1&type=item&tracking_id=e2af56e6-6952-44fb-a843-df1f5f0d94c3
# - UT for missing 'attrs'
# - UT for missing id
# - UT for missing spec items (sup total, sup util, dorms, baños)


class BuildingsSpider(scrapy.Spider):
    name = "buildings"
    start_urls = [
        URL_LAS_CONDES,
        # URL_PROVIDENCIA,
        # URL_LA_REINA,
        # URL_NUNOA,
    ]

    custom_settings = {
        'RETRY_TIMES': '2',
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 404],
        'FEED_FORMAT': 'json',
    }

    def parse(self, response):
        items = response.css('.results-item')
        for item in items:
            is_project = item.css('.item__image-label::text').get() is not None
            currency = item.css('.price__symbol::text').get()
            price = float(item.css('.price__fraction::text').get().replace('.', ''))
            attrs = item.css('.item__attrs::text').extract()[0].replace('\xa0', ' ')
            brief = '|'.join(item.css('.main-title::text').getall())
            link = item.css('.item__info-link::attr(href)').get()
            tmp = link.split('/')
            town = tmp[5]
            item_id = tmp[6].split('-')[0]

            # yield {
            #     'is_project': is_project,
            #     'town': town,
            #     'id': item_id,
            #     'price': price,
            #     'currency': currency,
            #     'link': link,
            #     'brief': brief,
            #     'attrs': attrs,
            #     'area_building': -1,
            #     'area_terrain': -1,
            #     'bedrooms': -1,
            #     'bathrooms': -1
            # }
            metadata = {
                'is_project': is_project,
                'town': town,
                'id': item_id,
                'price': price,
                'currency': currency,
                'link': link,
                'brief': brief,
                'attrs': attrs,
                'area_building': -1,
                'area_terrain': -1,
                'bedrooms': -1,
                'bathrooms': -1
            }

            yield response.follow(link, callback=self.parse_details, meta=metadata)

            break

        # parse next page of results
        # next_page = response.css('.andes-pagination__button--next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        print('==========================')
        print(response.css('.specs-list'))
        print('==========================')
        yield response.meta