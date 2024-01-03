import scrapy

class MySpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://q.10jqka.com.cn/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        