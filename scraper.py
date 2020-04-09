import logging

import scrapy


logger = logging.getLogger()

URL_BASE = 'https://www.portalinmobiliario.com/venta/casa/'
URL_SUFFIX = '?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=1'
URL_LAS_CONDES = URL_BASE + 'las-condes-metropolitana' + URL_SUFFIX
URL_NUNOA = URL_BASE + 'nunoa-metropolitana' + URL_SUFFIX
URL_PROVIDENCIA = URL_BASE + 'providencia-metropolitana' + URL_SUFFIX


class BuildingsSpider(scrapy.Spider):
    name = "buildings"
    start_urls = [
        URL_LAS_CONDES,
        # URL_PROVIDENCIA,
        # URL_NUNOA
    ]

    custom_settings = {
        'RETRY_TIMES': '2',
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 404],
        'FEED_FORMAT': 'json',
        'HTTPPROXY_ENABLED': False
    }

    def parse(self, response):
        items = response.css('.results-item')
        for item in items:
            is_project = False
            currency = item.css('.price__symbol::text').get()
            price = float(item.css('.price__fraction::text').get().replace('.', ''))
            attrs = item.css('.item__attrs::text').extract()[0].replace('\xa0', ' ')
            brief = '|'.join(item.css('.main-title::text').getall())
            link = item.css('.item__info-link::attr(href)').get()
            tmp = link.split('/')
            town = tmp[5]
            item_id = tmp[6].split('-')[0]
            break

        yield {
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

        # next_page = response.css('.pagination').css(
        #     '.siguiente a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
