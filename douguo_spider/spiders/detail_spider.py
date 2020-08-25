import os
import json
import scrapy
from scrapy.loader import ItemLoader
from douguo_spider.items import DouguoSpiderItem

project_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../')

class HomeSpider(scrapy.Spider):
    name = 'detail'
    category = ''

    def start_requests(self):
        if self.category:
            with open(os.path.join(project_path, 'data/recipe_{}_basic.json'.format(self.category))) as f:
                list = json.load(f)
                for item in list:
                    yield scrapy.Request(url=item.get('url'), callback=self.parse)

    def parse(self, response):
        res = response

        l = {}
        l['title'] = res.css('h1.title::text').get()
        l['img'] = res.css('#banner img::attr("src")').get()
        l['author_img'] = res.css('a.author-img img::attr("src")').get()
        l['author'] = res.css('.author-info a.nickname::text').get()

        # 浏览量
        l['pv'] = res.css('.vcnum span::text').get()
        # 收藏量
        l['stars'] = res.css('.collectnum::text').get()

        # 简介
        intro = ''.join(res.css('p.intro::text').getall())
        intro = intro.replace('\r', '').replace('\n', '').strip()
        l['intro'] = intro

        # 材料
        l['materials'] = res.css('.metarial .scname a::text').getall()
        l['materials_quantity'] = res.css('.metarial .scnum::text').getall()

        # steps
        steps = [
            item.replace('\r', '').replace('\n', '').strip()
            for item in res.css('.step .stepinfo::text').getall()
            if item.replace('\r', '').replace('\n', '').strip() != ''
        ]

        l['steps'] = steps
        l['tips'] = ''.join(res.css('.tips p::text').getall())
        l['category'] = res.css('.fenlei a::text').getall()

        yield l