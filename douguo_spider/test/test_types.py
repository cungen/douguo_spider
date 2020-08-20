import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from douguo_spider.spiders.types_spider import TypesSpider

if __name__ == "__main__":
    spider = TypesSpider()
    spider.start_requests()
    print(spider.start_urls)
