from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from mpeiscraper import settings
from mpeiscraper.spiders.Mpei import MpeiSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_settings['FEED_EXPORT_ENCODING'] = 'utf-8'
    crawler_settings['FEEDS'] = {"items.json": {"format": "json"}}

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(MpeiSpider)
    process.start()
