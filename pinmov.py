import logging.config
# import logging.getLogger
import numbers

import scrapy


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

_URL_LAS_CONDES = 'https://www.portalinmobiliario.com/venta/casa/las-condes-metropolitana'
_URL_PROVIDENCIA = 'https://www.portalinmobiliario.com/venta/casa/providencia-metropolitana'
_URL_LA_REINA = 'https://www.portalinmobiliario.com/venta/casa/la-reina-metropolitana'
_URL_NUNOA = 'https://www.portalinmobiliario.com/venta/casa/nunoa-metropolitana'

_SCRAP_TYPE = ['REG', 'PRO']


class ScrapUtils(object):
    """
    Utils class to ease the scrapping
    """
    @staticmethod
    def parse_area(surface):
        if surface is None or type(surface) is not str:
            return -1
        else:
            return int(surface.split(' ')[0])

    @staticmethod
    def parse_rooms(number):
        if number is None or type(number) is not str:
            return -1
        else:
            return int(number)


class BuildingsSpider(scrapy.Spider):
    name = "buildings"
    start_urls = [
        # _URL_LAS_CONDES,
        _URL_PROVIDENCIA,
        # _URL_LA_REINA,
        # _URL_NUNOA,
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
            scrap_id += 1

            try:
                is_project = item.css('.item__image-label::text').get() is not None
                currency = item.css('.price__symbol::text').get()
                price = float(item.css('.price__fraction::text').get().replace('.', ''))
                attrs = item.css('.item__attrs::text').extract()[0].replace('\xa0', ' ')
                brief = '|'.join(item.css('.main-title::text').getall())
                link = item.css('.item__info-link::attr(href)').get().split('#')[0]
                town = response.url.strip('/').split('/')[-1]

                tmp = link.split('/')
                if len(tmp) == 4:   # old url format
                    item_id = tmp[3].split('-')[1]
                else:               # new url format
                    item_id = tmp[6].split('-')[0]

                data = {
                    'scrap_id': scrap_id,
                    'is_project': is_project,
                    'town': town,
                    'id': item_id,
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

                logger.debug(' > scrap {:02}: {}...'.format(scrap_id, data['link'][34:34 + min(70, len(data['link']))]))
                yield scrapy.Request(link,
                                     callback=BuildingsSpider.parse_details,
                                     cb_kwargs={'data': data},
                                     meta={'dont_redirect': True,'handle_httpstatus_list': [302]}
                                     )

            except Exception as ex:
                logger.error('\n\tscrap_id:{:02}\n\turl: {}\n\tlink: {}'.format(
                            scrap_id, response.url, link))
                logger.error('Exception: {}'.format(str(ex)))

        # parse next page of results
        next_page = response.css('.andes-pagination__button--next a::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    @staticmethod
    def parse_details(response, data):
        logger.debug('  ({}) scrap: {:03}'.format(_SCRAP_TYPE[data['is_project']], data['scrap_id']))

        try:
            terrain = ScrapUtils.parse_area(response.xpath('//strong[contains(.,"total")]/following-sibling::span/text()').get())
            building = ScrapUtils.parse_area(response.xpath('//strong[contains(.,"útil")]/following-sibling::span/text()').get())
            bedrooms = ScrapUtils.parse_rooms(response.xpath('//strong[contains(.,"Dormitorios")]/following-sibling::span/text()').get())
            bathrooms = ScrapUtils.parse_rooms(response.xpath('//strong[contains(.,"Baños")]/following-sibling::span/text()').get())

            data.update({
                'terrain': terrain,
                'building': building,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms
            })

        except Exception as ex:
            logger.error('\n\tscrap_id:{:02}\n\ttype: {}\n\turl: {}'.format(
                data['scrap_id'], _SCRAP_TYPE[data['is_project']], response.url))
            logger.error('Exception: {}'.format(str(ex)))

        yield data
