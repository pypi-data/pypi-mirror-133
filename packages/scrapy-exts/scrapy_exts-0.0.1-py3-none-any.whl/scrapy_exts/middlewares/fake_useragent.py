from .base_middleware import BaseDownloaderMiddleware
import random


USER_AGENT = 'User-Agent'

class SimpleFakeUserAgentDownloadMiddleware(BaseDownloaderMiddleware):
    """
    简单随机UA下载中间件: 每一次请求均使用随机UA
    """

    def __init__(self, settings=None):
        super().__init__(settings)
        self.user_agent = settings.get('USER_AGENT')
        if not self.user_agent:
            from scrapy_exts.utils import UAS
            self.uas = UAS
            self.total = {
                'all': len(self.uas['randomize']),
                'chrome': len(self.uas['browsers']['chrome']),
                'opera': len(self.uas['browsers']['opera']),
                'firefox': len(self.uas['browsers']['firefox']),
                'ie': len(self.uas['browsers']['ie']),
                'safari': len(self.uas['browsers']['safari']),
            }


    def process_request(self, request, spider):
        if self.user_agent:
            request.headers.setdefault(USER_AGENT, self.user_agent[random.randint(0, len(self.user_agent) - 1)])
        else:
            user_agent_type = self.uas['randomize'][random.randint(0, self.total['all'] - 1)]
            request.headers.setdefault(USER_AGENT, self.uas['browsers'][user_agent_type][random.randint(0, self.total[user_agent_type] - 1)])