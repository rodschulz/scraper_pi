import logging
import numbers

import scrapy


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

_URL_LAS_CONDES = 'https://www.portalinmobiliario.com/venta/casa/las-condes-metropolitana'
_URL_PROVIDENCIA = 'https://www.portalinmobiliario.com/venta/casa/providencia-metropolitana'
_URL_LA_REINA = 'https://www.portalinmobiliario.com/venta/casa/la-reina-metropolitana'
_URL_NUNOA = 'https://www.portalinmobiliario.com/venta/casa/nunoa-metropolitana'

_SCRAP_TYPE = ['REG', 'PRO']

# TODO
# - UT link formats different (old urls) => https://www.portalinmobiliario.com/MLC-517628020-casa-en-venta-de-4-dormitorios-en-las-condes-_JM#position=1&type=item&tracking_id=e2af56e6-6952-44fb-a843-df1f5f0d94c3
# - UT for missing 'attrs'
# - UT for missing id
# - UT for missing spec items (sup total, sup util, dorms, baños)


class BuildingsSpider(scrapy.Spider):
    name = "buildings"
    start_urls = [
        # _URL_LAS_CONDES,
        # _URL_PROVIDENCIA,
        # _URL_LA_REINA,
        _URL_NUNOA,
    ]

    custom_settings = {
        'RETRY_TIMES': '2',
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 404],
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_ITEMS': 1,
        'CONCURRENT_REQUESTS': 1,
    }

    def parse(self, response):
        logger.info('scraping {}'.format(response.url))

        items = response.css('.results-item')
        if items is None:
            logger.warning('no items found')
            return

        scrap_id = 0
        for item in items:
            is_project = item.css('.item__image-label::text').get() is not None
            currency = item.css('.price__symbol::text').get()
            price = float(item.css('.price__fraction::text').get().replace('.', ''))
            attrs = item.css('.item__attrs::text').extract()[0].replace('\xa0', ' ')
            brief = '|'.join(item.css('.main-title::text').getall())
            link = item.css('.item__info-link::attr(href)').get().split('#')[0]
            town = response.strip('/').url.split('/')[-1]
            # item_id = tmp[6].split('-')[0]

            scrap_id += 1

            data = {
                'scrap_id': scrap_id,
                'is_project': is_project,
                'town': town,
                # 'id': item_id,
                'price': price,
                'currency': currency,
                'link': link,
                'brief': brief,
                'attrs': attrs,
                'terrain': -1,
                'building': -1,
                'bedrooms': -1,
                'bathrooms': -1,
            }

            logger.debug(' > scrap {:02}: {}...'.format(scrap_id, data['link'][34:34+min(70, len(data['link']))]))
            yield scrapy.Request(link, callback=BuildingsSpider.parse_details, cb_kwargs={'data': data})

            # if scrap_id == 10:
            #     break

        # parse next page of results
        # next_page = response.css('.andes-pagination__button--next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def parse_details(response, data):
        logger.debug('  ({})({}) scrap: {:03}'.format(response.status, _SCRAP_TYPE[data['is_project']], data['scrap_id']))

        if data['is_project']:
            valid, details = BuildingsSpider.details_project(response, data)
        else:
            valid, details = BuildingsSpider.details_regular(response, data)

        if valid:
            data.update(details)

        yield data

    @staticmethod
    def details_regular(response, data):


        # terrain = response. \
        #     xpath('//*[@id="root-app"]/div/div[1]/div[1]/section[1]/div/div/div/section/ul/li[1]/span/text()').get()
        # terrain = terrain.split(' ')[0]
        # if terrain.isdigit():
        #     terrain = int(terrain)
        #
        # building = response. \
        #     xpath('//*[@id="root-app"]/div/div[1]/div[1]/section[1]/div/div/div/section/ul/li[2]/span/text()').get()
        # building = building.split(' ')[0]
        # if building.isdigit():
        #     building = int(building)
        #
        # bedrooms = response. \
        #     xpath('//*[@id="root-app"]/div/div[1]/div[1]/section[1]/div/div/div/section/ul/li[3]/span/text()').get()
        # if bedrooms.isdigit():
        #     bedrooms = int(bedrooms)
        #
        # bathrooms = response. \
        #     xpath('//*[@id="root-app"]/div/div[1]/div[1]/section[1]/div/div/div/section/ul/li[4]/span/text()').get()
        # if bathrooms.isdigit():
        #     bathrooms = int(bathrooms)
        #
        # is_valid = isinstance(terrain, numbers.Number) \
        #            and isinstance(building, numbers.Number) \
        #            and isinstance(bedrooms, numbers.Number) \
        #            and isinstance(bathrooms, numbers.Number)
        # data = {
        #     'terrain': terrain,
        #     'building': building,
        #     'bedrooms': bedrooms,
        #     'bathrooms': bathrooms
        # }
        #
        # return is_valid, data

        return True, {'terrain': 10, 'building': 100}


    @staticmethod
    def details_project(response, data):
        # building = response. \
        #     xpath('//*[@id="root-app"]/div[2]/div[1]/div[1]/section[2]/div[1]/section/ul/li[1]/span/text()').get()
        # try:
        #     building = building.split(' ')[0]
        #     building = int(float(building))
        # except Exception:
        #     pass
        #
        # bedrooms = response. \
        #     xpath('//*[@id="root-app"]/div[2]/div[1]/div[1]/section[2]/div[1]/section/ul/li[2]/span/text()').get()
        # if bedrooms.isdigit():
        #     bedrooms = int(bedrooms)
        #
        # bathrooms = response. \
        #     xpath('//*[@id="root-app"]/div[2]/div[1]/div[1]/section[2]/div[1]/section/ul/li[3]/span/text()').get()
        # if bathrooms.isdigit():
        #     bathrooms = int(bathrooms)
        #
        # is_valid = isinstance(building, numbers.Number) \
        #            and isinstance(bedrooms, numbers.Number) \
        #            and isinstance(bathrooms, numbers.Number)
        # data = {
        #     'building': building,
        #     'bedrooms': bedrooms,
        #     'bathrooms': bathrooms
        # }
        #
        # return is_valid, data

        return True, {'terrain': 10, 'building': 100}
