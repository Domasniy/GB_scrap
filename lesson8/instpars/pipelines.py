# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstparsPipeline:

    def __init__(self):                             #Конструктор, где инициализируем подключение к СУБД
        client = MongoClient('3.10.213.78', 7077)
        self.mongo_base = client.instagram


    def process_item(self, item, spider):           #Метод, куда прилетает сформированный item
        collection = self.mongo_base[spider.name]   #Выбираем коллекцию по имени паука
        collection.insert_one(item)                #Добавляем в базу данных
        return item