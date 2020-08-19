import scrapy
from scrapy.loader import ItemLoader
from douguo_spider.items import DouguoSpiderItem


class HomeSpider(scrapy.Spider):
    name = "home"

    def start_requests(self):
        urls = [
            'https://www.douguo.com/cookbook/1298538.html',
            'https://www.douguo.com/cookbook/1132250.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        res = response

        # l = ItemLoader(item = DouguoSpiderItem(), response = res)
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

        # l.add_value('title', res.css('h1.title::text').get())
        # l.add_value('img', res.css('#banner img::attr("src")').get())
        # l.add_value('author_img', res.css('a.author-img img::attr("src")').get())
        # l.add_value('author', res.css('.author-info a.nickname::text').get())

        # # 浏览量
        # l.add_value('pv', res.css('.vcnum span::text').get())
        # # 收藏量
        # l.add_value('stars', res.css('.collectnum::text').get())

        # # 简介
        # intro = ''.join(res.css('p.intro::text').getall())
        # intro = intro.replace('\r', '').replace('\n', '').strip()
        # l.add_value('intro', intro)

        # # 材料
        # materials = res.css('.metarial .scname a::text').getall()
        # materials_quantity = res.css('.metarial .scnum::text').getall()

        # l.add_value('materials', materials)
        # l.add_value('materials_quantity', materials_quantity)

        # # steps
        # steps = [
        #     item.replace('\r', '').replace('\n', '').strip()
        #     for item in res.css('.step .stepinfo::text').getall()
        #     if item.replace('\r', '').replace('\n', '').strip() != ''
        # ]

        # l.add_value('steps', steps)
        # l.add_value('tips', ''.join(res.css('.tips p::text').getall()))
        # cates = res.css('.fenlei a::text').getall()
        # l.add_value('category', cates)

        # return l.load_item()
        yield l