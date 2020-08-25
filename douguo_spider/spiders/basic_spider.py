import os
import json
import scrapy
import urllib

project_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../')
count = 0

class TypesSpider(scrapy.Spider):
    name = 'basic'
    domain = 'https://www.douguo.com'
    category = ''

    def start_requests(self):
        if self.category:
            url = self.domain + '/caipu/' + self.category
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for info in response.css('ul.cook-list li.clearfix').getall():
            res = scrapy.Selector(text=info)
            recipe = {}
            recipe['name'] = res.css('a.cookname::text').get()
            recipe['url'] = self.domain + res.css('a.cookname::attr("href")').get()
            recipe['author'] = res.css('a.headicon img::attr("alt")').get()
            recipe['score'] = res.css('.score span+span::text').get()
            recipe['img'] = res.css('.cook-img img::attr("src")').get()
            recipe['author_img'] = res.css('a.headicon img::attr("src")').get()
            recipe['ingredient'] = res.css('p.major::text').get()
            yield recipe

        next_page = response.css('a.anext::attr("href")').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
