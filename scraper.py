import logging

import scrapy


logger = logging.getLogger()

URL_BASE = 'https://www.portalinmobiliario.com/venta/casa/'
URL_SUFFIX = '?ca=3&ts=1&mn=2&or=&sf=1&sp=0&at=0&pg=76'

URL_LAS_CONDES = URL_BASE + 'las-condes-metropolitana' + URL_SUFFIX
URL_NUNOA = URL_BASE + 'nunoa-metropolitana' + URL_SUFFIX
URL_PROVIDENCIA = URL_BASE + 'providencia-metropolitana' + URL_SUFFIX


class BuildingsSpider(scrapy.Spider):
    name = "buildings"
    start_urls = [URL_LAS_CONDES, URL_PROVIDENCIA, URL_NUNOA]

    def parse(self, response):
        town = response.css('.results-title').xpath('.//ol/li[5]/text()').get()
        for item in response.css('.propiedad'):
            item_data = item.css('.product-item-data')
            item_area = item_data.xpath('.//div/div[3]/p/span/@data-title').get()

            area_building = -1
            area_terrain = -1
            if item_area is not None:
                item_area = item_area.replace('m&sup2;', '').split('/')

                data_1 = item_area[0].strip().replace('.', '').split(' ')
                if len(item_area) > 1:
                    data_2 = item_area[1].strip().replace('.', '').split(' ')

                if data_1[1].lower() == 'construida':
                    area_building = data_1[0]
                if data_2[1].lower() == 'construida':
                    area_building = data_2[0]
                if data_1[1].lower() == 'terreno':
                    area_terrain = data_1[0]
                if data_2[1].lower() == 'terreno':
                    area_terrain = data_2[0]

            yield {
                'town': town,
                'id': item.xpath('.//@data-product-id').get(),
                'price': item_data.xpath('.//div/div[2]/p/span/@data-price').get(),
                'currency': item_data.xpath('.//div/div[2]/p/span/@data-price-currency').get(),
                'area_building': area_building,
                'area_terrain': area_terrain,
                'link': item_data.xpath('.//div/div[1]/h4/a/@href').get()
            }

        next_page = response.css('.pagination').css('.siguiente a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
