from proxypool.db import RedisClient
from proxypool.proxy_spider import Crawler
from proxypool.setting import *
import sys

class Getter():
    def __init__(self):
        self.redis=RedisClient()
        self.crawler=Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        :return:
        """
        if self.redis.count()>=POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print("获取器开始执行")
        if not self.is_over_threshold():
            for calback_label in range(self.crawler.__CrawlFuncCount__):
                calback=self.crawler.__CrawlFunc__[calback_label]
                # 获取代理
                proxies=self.get_proxies(calback)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)