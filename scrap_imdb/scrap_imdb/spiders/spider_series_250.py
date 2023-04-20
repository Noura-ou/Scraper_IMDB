import scrapy
from ..items import ScrapImdbSeriesItem


class SpiderSeries250Spider(scrapy.Spider):

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrap_imdb.pipelines_series.ScrapSeriesPipeline': 400,
            'scrap_imdb.pipelines_series.CsvPipelineSeries': 301,
        }
    }

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
        durée = response.xpath('(//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li)[4]//text()').get().strip('()')
        date = response.xpath('(//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"]/li)[2]//text()').get().strip('()')
        score = response.xpath('//a[@class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-textPrimary ipc-text-button sc-acdbf0f3-2 tBSnU"]//span[@class="ipc-btn__text"]//div[@class="sc-acdbf0f3-3 kpRihV"]//div[@class="sc-bde20123-2 gYgHoj"]//span[@class="sc-bde20123-1 iZlgcd"]//text()').get().strip('()')
        nbr_votants = response.xpath('(//a[@class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-textPrimary ipc-text-button sc-acdbf0f3-2 tBSnU"]//span[@class="ipc-btn__text"]//div[@class="sc-acdbf0f3-3 kpRihV"]//div[@class="sc-bde20123-3 bjjENQ"])//text()').get().strip('()')
        genre = response.xpath('(//div[@class="ipc-chip-list--baseAlt ipc-chip-list"]//div[@class="ipc-chip-list__scroller"])//text()').extract()
        desciption = response.xpath('(//p[@class="sc-5f699a2-3 lopbTB"]//span[@class="sc-5f699a2-2 cxqNYC"])//text()').extract()
        acteurs = response.xpath('(//li[@class="ipc-metadata-list__item ipc-metadata-list-item--link"]//div[@class="ipc-metadata-list-item__content-container"]//ul[@class="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt"])[1]//text()').extract()
        nbr_eposodes = response.xpath('(//div[@class="ipc-title ipc-title--base ipc-title--section-title ipc-title--on-textPrimary"]//a[@class="ipc-title-link-wrapper"]//h3[@class="ipc-title__text"]//span[@class="ipc-title__subtext"])[1]//text()').extract()
        nbr_saison = response.xpath('(//div[@class="sc-5e603484-0 jyNcfY episodes-browse-episodes"]//div[@class="sc-5e603484-4 bUTodD"]//div[@class="ipc-simple-select ipc-simple-select--base ipc-simple-select--on-accent2"]//label[@class="ipc-simple-select__label"])[1]//text()').extract()
        
        
        def convertir_time(durée):
            if 'h' in durée and 'm' in durée:
                heure, minute = durée.split("h ")
                heure = int(heure)
                minute = int(minute.replace("m", ""))
            elif 'h' in durée:
                heure = int(durée.replace("h", ""))
                minute = 0
            elif 'm' in durée:
                heure = 0
                minute = int(durée.replace("m", ""))
            else:
                raise ValueError()
            duree_minutes = heure * 60 + minute
            return duree_minutes
    
     
        items['titre_original'] = titre_original
        items['durée'] = convertir_time(durée)
        items['date'] = date
        items['score'] = score
        items['nbr_votants'] = nbr_votants
        items['desciption'] = desciption
        items['genre'] = genre
        items['acteurs'] = acteurs
        items['nbr_eposodes'] = nbr_eposodes
        items['nbr_saison'] = nbr_saison
        
        yield items
