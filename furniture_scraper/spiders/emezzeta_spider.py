import scrapy

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

    custom_settings = { 'FEEDS': {'result.json': {'format': 'json', 'overwrite': True}}}

    def parse(self, response):
        if 'dnevni' in response.url:
            print('dnevni je zakon')
        for desne in response.css('div.product-item-info'):
            if 'desna' in desne.css('a.product-item-link::text').get().strip():
                if 'Rasprodaja' == desne.css('span.clearance-icon::text').get():
                    yield{'kutne_garniture': desne.css('a.product-item-link::text').get().strip(),
                          'regular_price': desne.css('span.old-price .price::text').get(),
                          'discount_price': desne.css('span.price::text').get(),
                        }

                else:
                    yield{'kutne_garniture': desne.css('a.product-item-link::text').get().strip(),
                          'regular_price': desne.css('span.price::text').get(),
                          'discount_price': desne.css('span.loyalty-price .price::text').get(),
                        }
