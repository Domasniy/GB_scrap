import scrapy
from scrapy.http import HtmlResponse
from leroy.items import LeroyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Compose
class LeroyruSpider(scrapy.Spider):
    name = 'leroyru'
    allowed_domains = ['leroymerlin.ru']
    search = []
    start_urls = ['https://leroymerlin.ru/search/?q=']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search[0]}']

    def parse(self, response):
        next_page = response.css('a[navy-arrow = "next"]')
        for link in next_page:
            yield response.follow(link, callback=self.parse)
        
        products_links = response.css('a.black-link.product-name-inner')
        for link in products_links:
            yield response.follow(link, callback=self.parse_product)
        
    
    def parse_product(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyItem(),response=response)      
        loader.add_css('name','h1.header-2::text')
        loader.add_value('url',response.url)
        loader.add_css('price','uc-pdp-price-view.primary-price meta[itemprop="price"]::attr(content)')
        loader.add_css('photos','picture[slot="pictures"] img::attr(data-origin)')
        options_keys = loader.get_css('dt.def-list__term::text', MapCompose(str.strip))
        options_val = loader.get_css('dd.def-list__definition::text', MapCompose(str.strip))
        loader.add_value('options',dict(zip(options_keys,options_val)))
        yield loader.load_item()
