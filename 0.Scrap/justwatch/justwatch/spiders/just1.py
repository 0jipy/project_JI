from audioop import add
import imp
import time
from pytest import yield_fixture
import scrapy
from justwatch.items import JustwatchItem
##
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys

# from justwatch import justwatch




class Just1Spider(scrapy.Spider):
    name="just1"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        'justwatch.middlewares.JustwatchDownloaderMiddleware': 501,
        }
    }

    def start_requests(self):
        # path, 변수 선언
        path_chrome = 'C:/Users/jlune/carbon/project_JI/0.Scrap/justwatch/webdriver/chromedriver_win32_99/chromedriver.exe' 
        driver = webdriver.Chrome(path_chrome)
        driver.maximize_window()
        
        # sys.stdout = open('stdout.txt', 'wt')  #wb인지 w인지 wt 인지.

        a=2021 # 시작년도
        b=2023 # 끝년도
        input_urls = []

        for year in map(str, range(a, b)):
            add_netflix = 'https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/netflix?content_type=movie&release_year_from={}&release_year_until={}'.format(year, year)
            input_urls.append(add_netflix)
            driver.get(url=add_netflix)
            
            ## time 등 필요하면 밖으로 빼줘야. 
            start = time.time()
            # 검사용 counter 페이지 영화개수 세서 스크롤 끝 검출용
            counter = driver.find_element_by_class_name("total-titles").text

            #스크롤 처리용 #리팩토링 하면 좋을텐데.
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    time.sleep(3) # 로딩이 늦어 빠르게 브레이크 되지 않도록.
                    break
                last_height = new_height

            try:
                # ID가 myDynamicElement인 element가 로딩될 때 까지 10초 대기
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "filter-bar__reset-button"))
                )
                end = time.time()

                print(f'>>> {year}년 수집완료 ! /n> URL : {add_netflix}) <<<')
                print(f'>>> item 개수 : {counter} <<<')
                print(f'>>> 걸린시간: {end - start} sec <<<')
            except TimeoutException:
                # 실패 시에는 에러메시지로 Time Out 출력
                print('Time Out')
            # finally:
                # driver.quit()
            # driver.quit()
            print("끝")

            # 영화링크수집
            elem = driver.find_elements_by_css_selector('div.title-list-grid div.title-list-grid__item a.title-list-grid__item--link')
            linkUrls = []
            for e in elem:
                linkUrl = e.get_attribute('href')
                linkUrls.append(linkUrl)

            print("영화링크 수집 끝")
            print(linkUrls)
            # 반복문 구성때문에 드라이버는 언제끄나? 젠장.
            # driver.quit()  
            
            # parse로 스크랩요청
            for i in linkUrls:
                yield scrapy.Request(i, callback=self.parse)


    def parse(self, response):
        item = JustwatchItem()   
        item['title_kor'] = response.css("div.title-block > div > h1::text").get().strip()
        item['opening_date'] = response.css("div.title-block > div > span::text").get().replace("(","").replace(")","")
        #item['rating'] = response.css("div.title-info visible-xs visible-sm >div.jw-scoring-listing__rating > a::text").get()
        item['just_rating'] = response.css('div.detail-infos > div > div > div > a::text')[0].get()
        item['imdb_rating'] = response.css('div.detail-infos > div > div > div > a::text')[1].get()
        item['genre'] = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/span/text()').getall()     # 뽑아낸 값이 리스트형태로 뽑힘 str 형태로 바꿔야함 모르겠음..
        item['runtime'] = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[3]/div[2]/text()').get()
        item['director'] = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[4]/div[2]/span/a/text()').getall() # 뽑아낸 값이 리스트형태로 뽑힘 str 형태로 바꿔야함 모르겠음..
        item['actors'] = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[3]/div/div/a/text()').getall() # 뽑아낸 값이 리스트형태로 뽑힘 str 형태로 바꿔야함 모르겠음...
        try:
            item['synopsis'] = response.xpath('//*[@id="base"]/div[2]/div/div[2]/div[2]/div/div[1]/div[4]/p/span/text()').get()
        except:
            item['synopsis']=None
        #print("제목:",title_kor, "개봉일:",opening_date,"저스트와치 평점:", just_rating,"IMDB 평점:",imdb_rating, "장르:",genre, "재생시간:",runtime, "감독:",director,"출연자:", actors, "시놉시스:",synopsis)
        # print(actors_list)    # 함수값 안에서의 출연진 값이 print 값으로 표시됨
        print(len(item))

        yield item

        # # driver.quit()
        # print("영화링크 수집 끝!")

        # yield scrapy.Request(url=, callback=self.parse)
        



        