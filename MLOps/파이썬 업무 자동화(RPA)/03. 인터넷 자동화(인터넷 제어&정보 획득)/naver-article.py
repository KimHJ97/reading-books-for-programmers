# 코드를 실행하면 인터넷이 자동으로 열린 후 단어를 자동 검색하여 그 결과를 텍스트 데이터로 가져온다.
# 이후 워크클라우드와 엑셀을 한 번에 만들어낸다.
# 1. 인터넷 브라우저를 열고 키워드를 입력 후 검색(클릭)한다.
# 2. 검색 결과 화면에서 뉴스 링크로 이동하고, 리스트 변수에 담는다.
# 3. 만들어진 리스트 변수를 엑셀로 변환한다.

import time
st = 5

# 1-1. 인터넷 브라우저 열기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 설치
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service = service) # 드라이브 열기
time.sleep(st)

driver.get("https://www.naver.com")
time.sleep(st)

# 1-2. 원하는 키워드 검색
greenbox = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/div/input")
greenbox.send_keys("반도체")
driver.find_element(By.CLASS_NAME, "ico_search_submit").click()
time.sleep(st)

# 2-1. 키워드 검색 후 뉴스 링크 접속
driver.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EB%B0%98%EB%8F%84%EC%B2%B4")
time.sleep(st)

# 2-2. 뉴스 탭에 나오는 기사들을 최신순으로 배열하여 리스트 변수에 담는다.
first_sel = driver.find_element(By.CLASS_NAME, "list_news")
second_sel = first_sel.find_elements(By.TAG_NAME, "li")
news_title_lists = []
for a in second_sel:
    news_title_lists.append(a.text.replace("\n", ""))

print("------------------------------추출 텍스트------------------------------")
print(news_title_lists)
time.sleep(st)

# 3-1. 만들어진 리스트 변수를 엑셀로 변환
import pandas as pd
df = pd.DataFrame(news_title_lists) # news_title_lists에 있는 데이터를 pandas 데이터프레임으로 저장
df.to_excel('test.xlsx')
time.sleep(st)

# 3-2. 만들어진 리스트 변수의 본문들을 합쳐서 워드클라우드로 만든다.
import WordCloud
from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS) # 불(Bool) 용어 지정(조사 등)
wc = WordCloud(font_path = 'BMJUA_ttf.ttf', stopwords = stopwords) # wc 변수에 wordcloud 객체 지정
wc.generate(str(news_title_lists))
wc.to_file('wordcloud_bm.png')
