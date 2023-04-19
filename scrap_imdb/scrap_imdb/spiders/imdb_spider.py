import scrapy
import time
from ..items import ScrapImdbItem

def convert_duration_to_minutes(duration):
    hours, minutes = duration.split('h ')
    minutes_only = minutes[:-1]
    total_minutes = int(hours) * 60 + int(minutes_only)
    return total_minutes


class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["imdb.com"]
    #start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4.1 Safari/605.1.15'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

#__________________________________________________________________________

    def parse(self, response):
        # extraire les liens vers les pages de chaque film
        
        links = response.css('td.titleColumn a::attr(href)').getall()
        titre = response.css('td.titleColumn a::text').get()
        for link in links:
            yield response.follow(link, callback=self.parse_movie)
            # time.sleep(2)
        
    

    def parse_movie(self, response):

        items = ScrapImdbItem()
        titre_original_element = response.xpath("//h1//span[@class='sc-afe43def-1 fDTGTb']/text()")
        if titre_original_element:
            titre_original = titre_original_element.get().strip('()')
        else:
            titre_original = "Titre inconnu"
        # durée = response.xpath('(//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li)[3]//text()').get().strip('()')

        durée_raw = response.xpath('(//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li)[3]//text()').get().strip('()')
        durée = convert_duration_to_minutes(durée_raw)

        date = response.xpath('(//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li)[1]//text()').get().strip('()')
        score = response.xpath('//a[@class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-textPrimary ipc-text-button sc-acdbf0f3-2 tBSnU"]//span[@class="ipc-btn__text"]//div[@class="sc-acdbf0f3-3 kpRihV"]//div[@class="sc-bde20123-2 gYgHoj"]//text()').get().strip('()')
        nbr_votants = response.xpath('(//a[@class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-textPrimary ipc-text-button sc-acdbf0f3-2 tBSnU"]//span[@class="ipc-btn__text"]//div[@class="sc-acdbf0f3-3 kpRihV"]//div[@class="sc-bde20123-3 bjjENQ"])//text()').get().strip('()')
        genre = response.xpath('(//div[@class="ipc-chip-list--baseAlt ipc-chip-list"]//div[@class="ipc-chip-list__scroller"])//text()').extract()
        desciption = response.xpath('(//p[@class="sc-5f699a2-3 lopbTB"]//span[@class="sc-5f699a2-2 cxqNYC"])//text()').extract()
        acteurs = response.xpath('(//li[@class="ipc-metadata-list__item ipc-metadata-list-item--link"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt"])//text()').extract()
        #(//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base"]//li[@class="ipc-metadata-list__item"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base"]//li[@class="ipc-inline-list__item"]//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"])//text()
        #pays = response.xpath('(//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base"]//li[@class="ipc-metadata-list__item"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base"]//li[@class="ipc-inline-list__item"]//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"])//text()').extract()

        items['titre_original'] = titre_original
        items['durée'] = durée
        items['date'] = date
        items['score'] = score
        items['nbr_votants'] = nbr_votants
        items['desciption'] = desciption
        items['genre'] = genre
        items['acteurs'] = acteurs

        yield items


#_______________________________

    # def parse(self, response):
    #     items = ScrapImdbItem()
    #     for movie in response.css('tr'):

    #         title = movie.css('td.titleColumn a::text').get()
    #         year = movie.css('span.secondaryInfo::text').get()  #response.xpath("//span[@class='text']/text()").extract()
    #         url = movie.css('td.titleColumn a')
 

    #         items['title'] = title
    #         items['year'] = year
    #         items['url'] = url
            
           
    #         yield items
        

    
