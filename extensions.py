import logging

from twisted.internet import task

from scrapy import signals
from scrapy.exceptions import NotConfigured


class LogStats:
    """Log basic scraping stats periodically"""

    pagesprev = 0
    itemsprev = 0
    prev_values = {}

    def __init__(self, stats, interval=60.0):
        self.stats = stats
        self.interval = interval
        self.multiplier = 60 / self.interval
        self.task = None

        self.logger = logging.getLogger("scrapy.extensions.CustomLogStats")

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat("LOGSTATS_INTERVAL")
        if not interval:
            raise NotConfigured
        o = cls(crawler.stats, interval)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.pagesprev = 0
        self.itemsprev = 0

        self.prev_values = {
            stat.split("_")[0]: 0
            for stat in list(self.stats.get_stats().keys())
            if "scraped_count" in stat
        }

        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)

    def log(self, spider):
        pages = self.stats.get_value("response_received_count", 0)
        items = self.stats.get_value("item_scraped_count", 0)
        irate = (items - self.itemsprev) * self.multiplier
        prate = (pages - self.pagesprev) * self.multiplier
        self.pagesprev, self.itemsprev = pages, items

        additional_stats = []
        for stat, stat_value in self.stats.get_stats().items():
            if not "scraped_count" in stat:
                continue

            if stat == "item_scraped_count":
                continue

            stat_name = self.get_stat_name(stat)

            previous_value = self.prev_values.get(stat_name, 0)
            rate = (stat_value - previous_value) * self.multiplier

            additional_stats.append(
                f"scraped {stat_value} {stat_name}s (at {rate} {stat_name}s/min)"
            )

        base_msg = (
            f"Crawled {pages} pages (at {prate} pages/min), "
            f"scraped {items} items (at {irate} items/min)"
        )

        additional_msg = ", ".join(additional_stats)
        full_msg = f"{base_msg}, {additional_msg}" if additional_stats else base_msg

        self.logger.info(full_msg, extra={"spider": spider})

    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()

    def get_stat_name(self, stat: str) -> str:
        return stat.split("_scraped_count")[0]
