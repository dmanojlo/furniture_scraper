import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

class EmezzetaSpider(scrapy.Spider):
    name = 'emezzeta'

    start_urls = ['https://www.emmezeta.hr/dnevni-boravak/akcije-i-popusti.html?vrsta=Kutna+garnitura',
                  'https://www.emmezeta.hr/kuhinja/akcije-i-popusti.html',
                ]

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.jobId = kwargs.get('_job')
        print(self.jobId)

    custom_settings = { 'FEEDS': {'emezz_result.json': {'format': 'json', 'overwrite': True}}}

    def parse(self, response):
        if 'dnevni' in response.url:
            for desne in response.css('div.product-item-info'):
                if desne.css('span.clearance-icon::text') or desne.css('span.action-icon::text'):
                    yield{'kutne_garniture': desne.css('a.product-item-link::text').get().strip(),
                          'regular_price': desne.css('span.old-price .price::text').get(),
                          'discount_price': desne.css('span.price::text').get(),
                        }

                else:
                    yield{'kutne_garniture': desne.css('a.product-item-link::text').get().strip(),
                          'regular_price': desne.css('span.price::text').get(),
                          'discount_price': desne.css('span.loyalty-price .price::text').get(),
                        }

        if 'kuhinja' in response.url:
            for kitchen in response.css('div.product-item-info'):
                if kitchen.css('span.clearance-icon::text') or kitchen.css('span.action-icon::text'):
                    yield{'kuhinja': kitchen.css('a.product-item-link::text').get().strip(),
                          'regular_price': kitchen.css('span.old-price .price::text').get(),
                          'discount_price': kitchen.css('span.price::text').get(),
                        }

                else:
                    yield{'kuhinja': kitchen.css('a.product-item-link::text').get().strip(),
                          'regular_price': kitchen.css('span.price::text').get(),
                          'discount_price': kitchen.css('span.loyalty-price .price::text').get(),
                        }


class MimaSpider(scrapy.Spider):
    name = 'mima'

    start_urls = ['https://namjestaj-mima.hr/proizvodi/?with_qty=0&only_available=0&categories=4398&price=0&price-e=26999&searchcode=basic&searchid=3&discount=1&to_page=2']

    custom_settings = { 'FEEDS': {'mima_result.json': {'format': 'json', 'overwrite': True}}}

    def parse(self, response):
        for kutne in response.css('div.cp'):
            yield{'kutne_mima': kutne.css('h2.cp-title::text').get()}


# process = CrawlerProcess()
# process.crawl(MySpider1)
# process.crawl(MySpider2)
# process.start() # the script will block here until all crawling jobs are finished
