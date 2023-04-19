import scrapy
from ..items import ScrapImdbSeriesItem


class SpiderSeries250Spider(scrapy.Spider):
    name = "spider_series_250"
    allowed_domains = ["www.imdb.com"]
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250', headers={
            'User-Agent': self.user_agent
        })


    def parse(self, response):        
        links = response.css('td.titleColumn a::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_series)
        

    def parse_series(self, response):
        items = ScrapImdbSeriesItem()
        titre_original = response.xpath("//h1//span[@class='sc-afe43def-1 fDTGTb']/text()").get().strip('()')


        items['titre_original'] = titre_original
        yield items
