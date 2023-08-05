from scrapy_exts.pipelines import BasePipeline
from scrapy.exceptions import NotConfigured, NotSupported
import logging

class SimpleMongoPipeline(BasePipeline):
    """
    简易MongodbPipeline实现
    """
    def __init__(self, settings=None):
        super().__init__(settings)
        mongo_host = settings.get('MONGO_HOST') or 'localhost'
        mongo_port = settings.get('MONGO_PORT') or 27017
        mongo_username = settings.get('MONGO_USERNAME')
        mongo_password = settings.get('MONGO_PASSWORD')
        mongo_auth_source = settings.get('MONGO_AUTH_SOURCE', settings.get('MONGO_AUTHSOURCE'))
        mongo_db = settings.get('MONGO_DATABASE')
        mongo_collection = settings.get('MONGO_COLLECTION')
        self.logger = logging.getLogger("scrapy_exts.pipelines.SimpleMongoPipeline")

        try:
            from pymongo import MongoClient
        except:
            raise NotSupported

        try:
            self.mongo = MongoClient(
                host=mongo_host,
                port=int(mongo_port),
                username=mongo_username,
                password=mongo_password,
                authSource=mongo_auth_source,
            )
        except:
            self.logger.debug('[WARNING] Not found %s config in settings. Pipeline will not be started.' % 'mongo')
            raise NotConfigured

        if mongo_db:
            self.db = self.mongo.get_database(mongo_db)
            if mongo_collection:
                self.col = self.db.get_collection(mongo_collection)

    def process_item(self, item, spider):
        if self.col:
            self.col.save(item)
        return item
