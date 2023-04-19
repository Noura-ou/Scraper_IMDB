from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
ATLAS_KEY = os.getenv('ATLAS_KEY')

class ScrapImdbPipeline:
    def __init__(self):
        self.client = MongoClient(ATLAS_KEY)
        self.db = self.client.Db_scraped_IMDB
        self.collection = self.db.Db_film

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
    
    def find_longest_movie():
        db = MongoClient(ATLAS_KEY).Db_scraped_IMDB
        longest_movie = db.Db_film.find_one(sort=[('durée', pymongo.DESCENDING)])
        return longest_movie
    
    def count_movies_with_actor(actor_name):
        db = MongoClient(ATLAS_KEY).Db_scraped_IMDB
        count = db.Db_film.count_documents({'acteurs': {'$in': [actor_name]}})
        return count



class CsvPipeline(object):
    def __init__(self):
        self.file = None
        self.exporter = None

    def open_spider(self, spider):
        self.file = open('output.csv', 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
