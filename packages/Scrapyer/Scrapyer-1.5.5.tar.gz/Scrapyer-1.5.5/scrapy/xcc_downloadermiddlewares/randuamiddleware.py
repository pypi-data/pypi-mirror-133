"""
browser :选择浏览器头
默认选择:chrome
其他选择:"opera"/"firefox"/"internetexplorer"/"safari"
或者任意ua:"random"
"""

from .fake_ua import choice_brower_model

class RandomUserAgent(object):
    DEFAULT_BROWSER = 'chrome'
    def __init__(self,uabrowser):
        self.browser = uabrowser #if self.uabrowser else self.DEFAULT_BROWSER
    @classmethod
    def from_crawler(cls, crawler):
        ub=crawler.settings.get('UABROWSER')
        return cls(uabrowser=ub)

    def process_request(self, request, spider):
        if not request.headers["User-Agent"] or 'scrapy' in request.headers["User-Agent"].decode().lower() :
            # 如果请求中没有设置ua,或者ua是scrapy
            request.headers["User-Agent"] = choice_brower_model(browser = self.browser)
