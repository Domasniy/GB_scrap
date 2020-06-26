# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# ● название;
# ● все фото;
# ● параметры товара в объявлении;
# ● ссылка;
# ● цена.


import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose

def price_float(value):
    try:
        value = float(value)
        return value
    except:
        return value


class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_float),output_processor=TakeFirst())
    photos = scrapy.Field()
    options = scrapy.Field(output_processor=TakeFirst())
