# import scrapy
# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from scrapy.utils.project import get_project_settings
# from scrapy.settings import Settings
# from scrapy.crawler import CrawlerProcess
# from furniture_scraper.spiders.emezzeta_spider import EmezzetaSpider, MimaSpider
#
#
#
# process = CrawlerProcess(get_project_settings())
# process.crawl(EmezzetaSpider)
# process.crawl(MimaSpider)
# process.start() # the script will block here until all crawling jobs are finished
