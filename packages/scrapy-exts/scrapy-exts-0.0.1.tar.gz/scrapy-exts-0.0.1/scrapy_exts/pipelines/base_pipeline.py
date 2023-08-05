from scrapy import signals
from scrapy_exts.utils import get_single_name


class BasePipeline:
    """
    基础管道, 含settings参数的构造方法
    """
    def __init__(self, settings=None):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_item(self, item, spider):
        return item

    def spider_opened(self, spider):
        spider.logger.info('Pipeline: %s, Spider opened: %s' % (get_single_name(self), spider.name))
