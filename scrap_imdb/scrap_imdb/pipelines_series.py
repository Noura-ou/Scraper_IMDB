from scrapy.exporters import CsvItemExporter
from pymongo import MongoClient
from dotenv import load_dotenv
import pymongo
import os


load_dotenv()
ATLAS_KEY = os.getenv('ATLAS_KEY')



class ScrapSeriesPipeline:

    def __init__(self):
        ATLAS_KEY = os.getenv('ATLAS_KEY')
        client = MongoClient(ATLAS_KEY,socketTimeoutMS=5000)
        db = client.Db_scraped_IMDB
        self.collection = db.Db_series

    
    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item



class CsvPipelineSeries(object):
    def __init__(self):
        self.file = None
        self.exporter = None

    def open_spider(self, spider):
        self.file = open('series.csv', 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
