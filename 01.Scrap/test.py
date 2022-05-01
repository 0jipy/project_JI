import time
from pytest import yield_fixture
import scrapy
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

        # sys.stdout = open('stdout.txt', 'wd')


        # 경로 봐줘야 할 곳
        path_chrome = 'C:/Users/jlune/carbon/project_JI/0.Scrap/justwatch/webdriver/chromedriver_win32_99/chromedriver.exe'  #
        driver = webdriver.Chrome(path_chrome)
        driver.maximize_window()
        # 경로, 영환씨 말대로 규칙생각.
        url = 'https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/netflix?content_type=movie&release_year_from=2022'
        driver.get(url)
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
            print(f'> {year}년 수집완료 ! /n> URL : {add_netflix})')
            print(f'> item 개수 : {counter}')
            print(f'> 걸린시간: {end - start}')
        except TimeoutException:
            # 실패 시에는 에러메시지로 Time Out 출력
            print('Time Out')
        # finally:
        #     # driver.quit()
        driver.quit()
        print("끝")

        # yield scrapy.Request(url=url, callback=self.parse)

        