# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstparsItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    follower_username = scrapy.Field()
    follower_full_name = scrapy.Field()
    follower_photo = scrapy.Field()
    #follow_by если true - то это кто подписан на пользователя, false - на кого подписан
    follow_by = scrapy.Field()
