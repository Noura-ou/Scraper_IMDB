import scrapy
from ..items import ScrapImdbItem


class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["imdb.com"]
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })


    def parse(self, response):
        # extraire les liens vers les pages de chaque film
        
        links = response.css('td.titleColumn a::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_movie)
        

    def parse_movie(self, response):

        items = ScrapImdbItem()
        titre_original = response.xpath("//h1//span[@class='sc-afe43def-1 fDTGTb']/text()").get().strip('()')
        durée = response.xpath('(//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li)[3]//text()').get().strip('()')
        date = response.xpath('(//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li)[1]//text()').get().strip('()')
        score = response.xpath('//a[@class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-textPrimary ipc-text-button sc-acdbf0f3-2 tBSnU"]//span[@class="ipc-btn__text"]//div[@class="sc-acdbf0f3-3 kpRihV"]//div[@class="sc-bde20123-2 gYgHoj"]//text()').get().strip('()')
        nbr_votants = response.xpath('(//a[@class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-textPrimary ipc-text-button sc-acdbf0f3-2 tBSnU"]//span[@class="ipc-btn__text"]//div[@class="sc-acdbf0f3-3 kpRihV"]//div[@class="sc-bde20123-3 bjjENQ"])//text()').get().strip('()')
        genre = response.xpath('(//div[@class="ipc-chip-list--baseAlt ipc-chip-list"]//div[@class="ipc-chip-list__scroller"])//text()').extract()
        desciption = response.xpath('(//p[@class="sc-5f699a2-3 lopbTB"]//span[@class="sc-5f699a2-2 cxqNYC"])//text()').extract()
        acteurs = response.xpath('(//li[@class="ipc-metadata-list__item ipc-metadata-list-item--link"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt"])[1]//text()').extract()
        pays = response.xpath('(//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base"]//li[@class="ipc-metadata-list__item"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base"]//li[@class="ipc-inline-list__item"]//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"])[1]//text()').extract()
        langue_d_origine = response.xpath('(//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base"]//li[@class="ipc-metadata-list__item"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base"]//li[@class="ipc-inline-list__item"]//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"])[4]//text()').extract()
        
        
        def convertir_time(durée):
            # extraire les heures et les minutes de la durée
            heure, minute = durée.split("h ")
            # convertir les heures et les minutes en entiers
            heure = int(heure)
            minute = int(minute.replace("m", ""))
            # calculer la durée en minutes
            duree_minutes = heure * 60 + minute
            return duree_minutes
        
     
        items['titre_original'] = titre_original
        items['date'] = date
        items['score'] = score
        items['nbr_votants'] = nbr_votants
        items['durée'] = convertir_time(durée)
        items['desciption'] = desciption
        items['genre'] = genre
        items['acteurs'] = acteurs
        items['pays'] = pays
        items['langue_d_origine'] = langue_d_origine

        yield items


        

    
