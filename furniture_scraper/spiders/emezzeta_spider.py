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

    start_urls = ['https://namjestaj-mima.hr/proizvodi/?searchcode=basic&searchid=3&with_qty=0&discount=1&only_available=0&categories=4398&price=0&price-e=26999&search_q=&to_page=2']

    custom_settings = { 'FEEDS': {'mima_result.json': {'format': 'json', 'overwrite': True}}}

    def parse(self, response):
        for kutne in response.css('div#items_catalog .cp'):
            if kutne.css('div.cp-old-price'):
                yield{'kutne_mima': kutne.css('h2.cp-title::text').get(),
                      'old_price': kutne.css('div.cp-old-price::text').get(),
                      'discount_price': kutne.css('div.cp-discount-price::text').get()
                     }


class LesninaSpider(scrapy.Spider):
    name = 'lesnina'

    start_urls = ['https://www.xxxlesnina.hr/api/graphql?operationName=search&variables=%7B%22cid%22%3Anull%2C%22encodedFhLink%22%3A%22null%22%2C%22filters%22%3A%22%5B%7B%5C%22id%5C%22%3A%5C%22categories%5C%22%2C%5C%22type%5C%22%3A%5C%22categoryFilter%5C%22%2C%5C%22values%5C%22%3A%5B%5C%22C1%5C%22%2C%5C%22C1C1%5C%22%2C%5C%22C1C1C1%5C%22%5D%7D%2C%7B%5C%22id%5C%22%3A%5C%22v_atrm_uklju_eno_u_cijenu%5C%22%2C%5C%22type%5C%22%3A%5C%22multiSelectFilter%5C%22%2C%5C%22elementId%5C%22%3A%5C%22funkcija_kreveta%5C%22%2C%5C%22values%5C%22%3A%5B%5C%22funkcija_kreveta%5C%22%5D%7D%2C%7B%5C%22id%5C%22%3A%5C%22v_eyecatcher%5C%22%2C%5C%22type%5C%22%3A%5C%22multiSelectFilter%5C%22%2C%5C%22elementId%5C%22%3A%5C%22bestprice-sale%5C%22%2C%5C%22values%5C%22%3A%5B%5C%22bestprice%5C%22%2C%5C%22sale%5C%22%5D%7D%5D%22%2C%22pagination%22%3A%22%7B%5C%22page%5C%22%3A1%2C%5C%22numberOfResults%5C%22%3A60%7D%22%2C%22sortBy%22%3A%22%5C%22popular%5C%22%22%2C%22searchTerm%22%3A%22%5C%22%5C%22%22%2C%22type%22%3Anull%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22b6f527bf074c162f0fe9dd316c2d9144a159f15ac6a8d323e8ffc4da98914152%22%7D%7D']


    custom_settings = { 'FEEDS': {'lesnina_result.json': {'format': 'json', 'overwrite': True}}}

    def parse(self, response):
        data = response.json()
        search_res = data['data']['search']['searchResults']
        for i in range(len(search_res)):
            if search_res[i]['priceData']['oldPrice']:
                yield{'kutne_lesnina': search_res[i]['name'].strip(),
                      'old_price': search_res[i]['priceData']['oldPrice']['value'],
                      'discount_price': search_res[i]['priceData']['currentPrice']['value'],
                    }

# process = CrawlerProcess()
# process.crawl(MySpider1)
# process.crawl(MySpider2)
# process.start() # the script will block here until all crawling jobs are finished
