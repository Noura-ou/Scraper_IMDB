import scrapy


class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["imdb.com"]
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    def parse(self, response):

        # Extract the movie titles
        titles = response.css('td.titleColumn a::text').extract()
        yield {'titles': titles}
        


        





        # title = response.css('title').extract()
        # yield {'titletext': title}




