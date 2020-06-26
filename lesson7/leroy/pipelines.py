# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class DataBasePipeline:

    
    def __init__(self):                             #Конструктор, где инициализируем подключение к СУБД
        client = MongoClient('', 7077)
        self.mongo_base = client.leroy_products


    def process_item(self, item, spider):           #Метод, куда прилетает сформированный item
        collection = self.mongo_base[spider.name]   #Выбираем коллекцию по имени паука
        collection.insert_one(item)                #Добавляем в базу данных
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
       if item['photos']:
           for img in item['photos']:
               try:
                   yield scrapy.Request(img,meta=item)
               except Exception as e:
                   print(e)

    def file_path(self, request, response=None, info=None, ):
        item = request.meta             #Получаем item из meta
        return 'img/'+ item['url'].split('/')[-2] + '/' + os.path.basename(urlparse(request.url).path)                      

    def item_completed(self, results, item, info):
        if results:
           item['photos']=[itm[1] for itm in results if itm[0]]
        return item
