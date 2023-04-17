import scrapy


class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["imdb.com"]
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    def parse(self, response):
        for movie in response.css('tr'):

            title = movie.css('td.titleColumn a::text').get()
            year = movie.css('span.secondaryInfo::text').get()

            if title and year:
                yield {
                    'title': title.strip(),
                    'year': year.strip('()')
                }
        
        # titles = response.css('td.titleColumn a::text').extract()
        # years = response.css('span.secondaryInfo::text').extract()
        # yield {'titles': titles , 'years': years}


    
