import os
import json
import scrapy

project_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../')
count = 0

class TypesSpider(scrapy.Spider):
    name = "types"
    domain = 'https://www.douguo.com/'

    def start_requests(self):

        with open(os.path.join(project_path, 'data/recipe_types.json')) as f:
            list = json.loads(f.read())
            urls = [self.domain + 'caipu/' + i for i in list[14:22]] # 按地区分类

        self.start_urls = urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        type = response.url.split('/')[4]
        filename = 'recipe_%s_urls.csv' % type
        filepath = os.path.join(project_path, 'data/' + filename)
        global count

        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write('name,url,author,score,img,author_img,ingredient\n')

        with open(filepath, 'a') as f:
            for i in self.parse_page(response):
                count += 1
                f.write('%s,%s,%s,%s,%s,%s,%s\n' % (
                    i.get('name'), i.get('url'), i.get('author'), i.get('score'),
                    i.get('img'), i.get('author_img'), i.get('ingredient')
                ))

        self.log('------------ Saved %s Count: %d' % (type, count))

        next_page = response.css('a.anext::attr("href")').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_page(self, response):
        recipes = []

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
            recipes.append(recipe)

        return recipes
