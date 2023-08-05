from scrapy import signals
from scrapy_exts.utils import get_single_name


class BaseSpiderMiddleware:
    """
    基础爬虫中间件, 含settings参数的构造方法
    """
    def __init__(self, settings=None):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        spider.logger.warn('SpiderMiddleware %s, Spider %s, process exception: %s' % (get_single_name(self), spider.name, exception))

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('SpiderMiddleware %s, Spider opened: %s' % (get_single_name(self), spider.name))


class BaseDownloaderMiddleware:
    """
    基础下载中间件, 含settings参数的构造方法
    """
    def __init__(self, settings=None):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        spider.logger.warn('DownloadMiddleware %s, Spider %s, process exception: %s' % (get_single_name(self), spider.name, exception))

    def spider_opened(self, spider):
        spider.logger.info('DownloadMiddleware: %s, Spider opened: %s' % (get_single_name(self), spider.name))
