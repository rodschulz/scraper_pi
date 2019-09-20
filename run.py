import logging

import scrapy


logging.config.fileConfig('log.ini', disable_existing_loggers=False)
logger = logging.getLogger()

URL_BASE = 'https://www.portalinmobiliario.com/venta/casa/'
URL_SUFFIX = '?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1'

URL_LAS_CONDES = URL_BASE + 'las-condes-metropolitana' + URL_SUFFIX
URL_NUNOA = URL_BASE + 'nunoa-metropolitana' + URL_SUFFIX
URL_PROVIDENCIA = URL_BASE + 'providencia-metropolitana' + URL_SUFFIX
URL_TEST = 'http://brickset.com/sets/year-2016'


class HousesSpider(scrapy.Spider):
    name = "houses_spider"
    start_urls = [URL_LAS_CONDES]

    def parse(self, response):
        print('================================================')
        for item in response.css('.product-item'):
            item_id = item.xpath('.//@data-product-id').get()
            print(item_id)

            # x = item.css('.product-item-summary')
            # print('x:', x)
            # z = x.xpath('.//p[1]')
            # print('z:', z)

            item_price = item.css('.product-price-value::attr(data-price)')
            price = item_price.extract()
            # discard projects, accept only existing buildings
            if len(price) > 1:
                continue
            print(price)

            # area = item.xpath('//div[1]')
            # print(area)
        print('================================================')
