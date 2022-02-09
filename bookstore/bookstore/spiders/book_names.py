from turtle import title
import scrapy
from bookstore.items import BookstoreItem

class BookNamesSpider(scrapy.Spider):
    name = 'book_names'
    allowed_domains = ['books.toscrape.com']
    start_urls = [f'http://books.toscrape.com/catalogue/page-{i}.html' for i in range(1,51)]
    id_book = 0


    def start_requests(self):
        """on veut faire des requests"""
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response):
        """on veut récupérer qqch en particulier dans les requests"""
        titles = response.xpath('//a/@title').getall()
        prices = response.xpath('//p[@class="price_color"]/text()').getall()
        
        for title, price in zip(titles, prices):
            price_clean = float(price.replace("£",""))
            self.id_book+=1
            yield BookstoreItem(index=self.id_book, name=title, price=price_clean)

