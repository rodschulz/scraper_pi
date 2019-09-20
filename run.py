import logging

import scrapy


logger = logging.getLogger()

URL_BASE = 'https://www.portalinmobiliario.com/venta/casa/'
URL_SUFFIX = '?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1'

URL_LAS_CONDES = URL_BASE + 'las-condes-metropolitana' + URL_SUFFIX
URL_NUNOA = URL_BASE + 'nunoa-metropolitana' + URL_SUFFIX
URL_PROVIDENCIA = URL_BASE + 'providencia-metropolitana' + URL_SUFFIX
URL_TEST = 'http://brickset.com/sets/year-2016'


class BuildingsSpider(scrapy.Spider):
    name = "buildings"
    start_urls = [URL_LAS_CONDES]

    def parse(self, response):
        logger.info('================================================')
        for item in response.css('.propiedad'):
            item_id = item.xpath('.//@data-product-id').get()

            item_data = item.css('.product-item-data')
            item_link = item_data.xpath('.//div/div[1]/h4/a/@href').get()
            item_price = item_data.xpath('.//div/div[2]/p/span/@data-price').get()
            item_currency = item_data.xpath('.//div/div[2]/p/span/@data-price-currency').get()

            item_area = item_data.xpath('.//div/div[3]/p/span/text()').get()
            item_area_built = item_area.split(' ')[0]
            item_area_terrain = item_area.split(' ')[2]

            logger.debug('[{id}] => {price} / {currency} / {area_built} / {area_terrain}'
                         .format(id=item_id, price=item_price, currency=item_currency,
                                 area_built=item_area_built, area_terrain=item_area_terrain))

        logger.info('================================================')
