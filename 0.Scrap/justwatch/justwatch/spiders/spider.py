# -* coding: utf-8 *-
from cProfile import run
import scrapy
from justwatch.items import JustwatchItem

class JustwatchSpider(scrapy.Spider):
    name = 'justwatch'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            'justwatch.middlewares.JustwatchDownloaderMiddleware': 543,   #보통 501쓰던데 셋팅에선 543. 뭘로써야 하지?
        }
    }

    # allowed_domains =['https://www.justwatch.com/kr'] #kr 주의 #도메인인데 /kr 적용되나
    # netf_2022 = 'https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/netflix?content_type=movie&release_year_from=2022'
    # start_urls = [netf_2022]

    # 원본남기기
    # def start_requests(self):
    #     # 나중에 변수처리 해줘야. 포매팅이라도 사용
    #     url = 'https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/netflix?content_type=movie&release_year_from=2022'
    #     yield scrapy.Request(url, callback=self.parse)

    # 스타드 수정본
    def start_requests(self):

        input_urls = []
        for year in map(str, range(2022, 2023)):   # 여기 수정해줘야
            add_netflix = 'https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/netflix?content_type=movie&release_year_from={}&release_year_until={}'.format(year, year)
            input_urls.append(add_netflix)
            print(year), print(add_netflix) #출력 로그용.
            yield scrapy.Request(url=add_netflix, callback=self.parse)

        # return super().start_requests(self)

        #     url = 'https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/netflix?content_type=movie&release_year_from=2022'


    # 어딘가에서 스크롤 내리고 크롤링하는 코드 개발해줘야.

    def parse(self, response):
        links = response.xpath('//*[@id="base"]/div[3]/div/div[2]/div[1]/div/div/a/@href').extract()
        links = list(map(response.urljoin, links))
        for link in links:
            yield scrapy.Request(link, callback=self.page_parse)

    def page_parse(self, response):
        item = JustwatchItem()
        
        # 일부수정. 스트립이나 getall 등. 자르고 합치고 조이고 기름칠.
        item['a_title_kor'] = response.css("div.title-block > div > h1::text").get().strip()
        item['b_opening_date'] = response.css("div.title-block > div > span::text").get().replace("(","").replace(")","").strip()
        # item['rating'] = response.css("div.title-info visible-xs visible-sm >div.jw-scoring-listing__rating > a::text").get()
        item['c_just_rating'] = response.css('div.detail-infos > div > div > div > a::text')[0].get().strip()
        item['imdb_rating'] = response.css('div.detail-infos > div > div > div > a::text')[1].get().strip()
        
        genre = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/span/text()').getall()     # 뽑아낸 값이 리스트형태로 뽑힘 str 형태로 바꿔야함 모르겠음..
        genre = ",".join(genre).replace(" ","")
        item['genre'] = genre
        runtime = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[3]/div[2]/text()').getall()
        runtime = ",".join(runtime).replace(" ","")
        item['runtime'] = runtime
        director = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[4]/div[2]/span/a/text()').getall() # 뽑아낸 값이 리스트형태로 뽑힘 str 형태로 바꿔야함 모르겠음..
        director = ",".join(director).replace(" ","")
        item['director'] = director
        actors = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div/div/a/text()').getall() # 뽑아낸 값이 리스트형태로 뽑힘 str 형태로 바꿔야함 모르겠음...
        actors = ",".join(actors).replace(" ","")
        item['actors'] = actors
        
        try:
            item['synopsis'] = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[4]/p/span/text()').get()
        except:
            item['synopsis']= None
        #print("제목:",title_kor, "개봉일:",opening_date,"저스트와치 평점:", just_rating,"IMDB 평점:",imdb_rating, "장르:",genre, "재생시간:",runtime, "감독:",director,"출연자:", actors, "시놉시스:",synopsis)
        # print(actors_list)    # 함수값 안에서의 출연진 값이 print 값으로 표시됨
        yield item



    
