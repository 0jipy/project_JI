
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = '0.Scrap\justwatch\justwatch\drivers\chromedriver.exe'
WINDOW_SIZE = "1920,1080"
 
chrome_options = Options()
# chrome_options.add_argument( "--headless" )     # 크롬창이 열리지 않음
# chrome_options.add_argument( "--no-sandbox" )   # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
# chrome_options.add_argument( "--disable-gpu" )  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
# chrome_options.add_argument(f"--window-size={ WINDOW_SIZE }")  # 브라우저가 설정한 창크기로 실행됩니다.
chrome_options.add_argument('--start-maximized')  # 브라우저가 최대화된 상태로 실행됩니다.
chrome_options.add_argument('Content-Type=application/json; charset=utf-8')
 
driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options )
driver.get( 'https://news.naver.com' )
