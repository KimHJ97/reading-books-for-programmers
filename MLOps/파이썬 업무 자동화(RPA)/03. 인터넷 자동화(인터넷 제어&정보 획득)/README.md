# 03장. 인터넷 자동화(인터넷 제어&정보 획득)

## 인터넷 자동화가 필요한 상황

매일 아침 8시 30분에 판매실적을 점검하고 관리하는 상황이 있다고 가정한다.  
그러기 위해서는 7시 30분에 회사에 도착해서 인트라넷에 접속하고 전날 실적을 내려받고, 내려받은 자료 시트를 취합하여 서식에 하나하나 옮겨 담아야 한다.  
또 이렇게 만들어진 자료는 각 임원/팀장들에게 메일로 전송한다.  

이러한 경우 파이썬과 Selenium으로 인터넷에서 가져오는 정보를 활용하거나 사내 인트라넷을 제어하는 동작을 설계하여 자동화할 수 있다.  
 - 인터넷 제어
    - 단순 클릭이나 타이핑 등 작업으로 인터넷 브라우저를 제어
    - 회사 이메일 정리, 단순 클릭을 통한 근태 등록, 판매실적 보고서 다운로드 등
 - 인터넷 정보 획득
    - 인터넷에 있는 여러 정보를 획득
    - 판매 데이터나 시황 분석, 타사 서비스 활용 등 데이터에 기반한 사고가 필요할 때 정보 획득
    - Selenium을 활용해 인터넷에서 필요한 정보를 그대로 긁어와서 텍스트를 추출한다.
    - 각 공식 사이트에서 제공하는 API를 활용해 대량의 데이터를 한 번에 가져온다.

<br/>

## 인터넷 자동화 사전 라이브러리 설치

Selenium은 웹 애플리케이션 자동화 및 테스트 수행을 돕는 프레임워크로 다양한 프로그래밍 언어(파이썬, 자바, C#, PHP, 루비 등)를 지원하며, 테스트 도메인 특화 언어인 Selenese를 제공한다.  
인터넷 제어를 위해 Selenium을 활용하며, WebDriver 라이브러리를 함께 이용한다. 해당 라이브러리를 통해 브라우저나 인트라넷을 제어할 수 있는 환경을 갖추고, 파이썬 코딩으로 인터넷을 구동시킬 수 있다.  
 - Selenium 공식 문서
    - https://www.selenium.dev/documentation/

<br/>

 - `Selenium 라이브러리 설치`
```py
!pip install selenium == 4.1.5
import selenium
selenium.__version__
```

 - `Word Cloud 라이브러리 설치`
    - Word Cloud(워드 클라우드)를 활용해 텍스트 정보를 요약하는 데 사용할 수 있다.
    - 만약, Jupyter Notebook에서 Word Cloud 설치 에러가 발생한 경우 Anaconda Prompt에서 wordcloud를 삭제하고 다시 설치한다.
        - [Widnows + S] > Anaconda Prompt > pip uninstall wordcloud
        - conda install -c conda-forge wordcloud=1.8.1
```py
!pip install wordcloud == 1.8.1
import wordcloud
wordcloud.__version__
```

 - `WebDriver 라이브러리 가져오기`
    - 파이썬으로 브라우저를 구동하기 위해서는 WebDriver 라이브러리를 이용한다.
```py
!pip install selenium webdriver_manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 설치
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
```

<br/>

## Selenium 기본 지식

 - `Selenium 설치 및 라이브러리 가져오기`
```py
!pip install selenium == 4.1.5
```

 - `웹 브라우저 드라이버 설치`
    - 설치된 Selenium 라이브러리를 정상적으로 작동시키기 위한 코드를 실행한다. (크롬 브라우저가 기본 브라우저로 설정되어야 한다.)
```py
# 크람 드라이버 자동 설치 (selenium 4.0 버전 이후)
!pip install selenium webdriver_manager

# pc 버전 코드
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 설치
```

 - `인터넷 열기 & HTML 코드 받아오기`
```py
# 인터넷 열기
driver = webdriver.Chrome(service = service) # 드라이브 열기
driver.get("https://www.naver.com")

# HTML 코드 받아오기
driver.page_source
```

 - `요소 찾기`
    - Selenium은 webdriver에서 제공하는 locator를 이용해 요소를 찾아낸다.
        - https://www.selenium.dev/documentation/webdriver/elements/locators/
        - class name: 클래스명에 검색 값이 포함된 요소를 찾는다.
        - id: ID 속성이 검색 값과 일치하는 요소를 찾는다.
        - tag name: 태그명이 검색 값과 일치하는 요소를 찾는다.
        - xpath: XPath 식이 일치하는 요소를 찾는다.
    - 참고
        - XPath(XML Path Language)는 W3C의 표준으로 확장 생성 언어 문서의 구조를 통해 경로 위에 지정한 구문을 사용하여 항목을 배치하고 처리하는 방법을 기술하는 언어이다.
```py
# class_name
# driver.find_element(By.CLASS_NAME, "클래스 이름")
class_sel = driver.find_element(By.CLASS_NAME, "gb_7d.gb_f.gb_lg.gb_cg")

# id
# driver.find_element(By.ID, "id")
id_sel = driver.find_element(By.ID, "gb")

# tag_name
driver.find_element(By.TAG_NAME, "태그 이름")

# xpath
# driver.find_element(By.XPATH, "xpath 식")
xpath_sel = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div")
```

 - `동작 넣기`
    - 요소를 찾고, 원하는 동작을 수행하도록 한다. (클릭, 타이핑, 정보 획득 등)
    - __변수에 요소 데이터 넣기__
        - element.send_keys('데이터')
        - 검색어를 입력하는 위치를 확인한다.
        - 해당 위치를 나타내는 코드를 확인하여 변수에 담는다.
        - 해당 변수에 원하는 데이터를 집어넣는다.
    - __요소 클릭__
        - element.click()
        - driver.execute_script("arguments[0].click", element)
    - __요소 출력__
        - element.text: 요소의 텍스트만을 가져온다.
        - element.get_attribute('innerHTML'): 요소의 HTML 코드 전부를 가져온다.
```py
# 변수에 요소 데이터 넣기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome(service = service) # 드라이브 열기
driver.get('https://www.google.com/?h1=') # 구글 접속
input_sel = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")

input_sel.send_keys("Hello World")

# 요소 클릭
click_sel = driver.find_element(ByXPATH, "/html/body/div[1]/div[3]/form/div[1]/div[3]/center/input[2]")
click_sel.click()

# 요소 출력
html_sel = driver.find_element(By.CLASS_NAME, "o3j99.n1xJcf.Ne6nSd")
print(html_sel.text) # 요소의 텍스트를 출력
html_sel.get_attribute('innerHTML') # 요소의 하위 HTML 코드를 모두 출력
```

 - `연속 동작`
    - 인터넷을 제어해서 어떤 동작을 자동화시키거나 반복적으로 특정 정보를 확보하려면 특정 루틴을 코드로 만들고 반복할 수 있게 해야 한다.
    - 우리가 사용하는 인터넷 환경은 위치/장소/시간마다 조금씩 속도가 다르다. 때문에, 코드를 반복적으로 구동할 때는 코드 실행을 기다리는 시간을 어느 정도 넣어 주어야 한다.
    - 그렇지 않으면 A 사이트에 도착하기 전에 검색어를 입력하고 검색을 누를 수 있다. 또, 화면이 나오지 않았는데 특정 탭을 클릭할 수 있다.
    - 이런 요인들은 중간에 오류가 생겨서 멈출 수 있기 떄문에, 연속 동작을 이해해야 한다.
    - time.time(): 현재 시간을 반환
    - sleep(시간): 시간(초)를 대기
    - driver.implicitly_wait(time_to_wait = 시간): 최대 시간(초)를 대기
```py
# 기다림 없이 진행
import time
import math
start = time.time() # 시작 시간 저장
driver = webdriver.Chrome(service = service)
driver.get('https://www.google.com/?h1=')

element = driver.find_element(By.CLASS_NAME, 'RNmpXc')
driver.execute_script('arguments[0].click();', element)
end = time.time() # 종료 시간 저장
print(f"{end-start:.5f} sec")

# 시간 기다리기 (지정 시간)
import time
import math
start = time.time() # 시작 시간 저장
driver.get('https://www.google.com/?h1=')
time.sleep(5) # 5초 뒤 시작

element = driver.find_element(By.CLASS_NAME, 'RNmpXc')
driver.execute_script('arguments[0].click();', element)
end = time.time() # 종료 시간 저장
print(f"{end-start:.5f} sec")

# 시간 기다리기 (로딩이 끝날 때까지 기다리기)
import time
import math
start = time.time() # 시작 시간 저장
driver.implicitly_wait(time_to_wait = 5) # 최대 5초까지 대기
driver.get('https://www.google.com/?h1=')

element = driver.find_element(By.CLASS_NAME, 'RNmpXc')
driver.execute_script('arguments[0].click();', element)
end = time.time() # 종료 시간 저장
print(f"{end-start:.5f} sec")
```

<br/>

## 인터넷 자동화 실습

pandas 라이브러리: https://pandas.pydata.org/docs  
word-cloud 라이브러리: https://amueller.github.io/word_cloud/  

 - `반도체 기사 정리 자동화`
    - 1. 인터넷에 있는 특정 단어('반도체')와 관련된 기사의 제목을 가져온다.
    - 2. 가져온 기사를 엑셀 한 시트로 만든다.
    - 3. 가져온 기사 제목을 모아서 워드클라우드로 제작한다.
```py
# 인터넷 제어를 위한 Selenium 라이브러리 설치
!pip install selenium == 4.1.5
!pip install selenium webdriver_Manager
!pip install wordcloud == 1.8.1

# 1. 인터넷 열기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
service = Service(executable_path = ChromeDriverManager().install()) # 크롬 드라이버 설치
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service = service) # 드라이브 열기

# 2. 웹사이트 접속 후 뉴스 기사 검색
driver.get('https://www.naver.com')

greenbox = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/div/input")
greenbox.send_keys("반도체")
driver.find_element(By.CLASS_NAME, "ico_search_submit").click()

# 3. URL을 활용해 2번 항목을 건너뛸 수 있다. 
driver.get("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EB%B0%98%EB%8F%84%EC%B2%B4")

# 4. 검색 결과 가져오기
first_sel = driver.find_element(By.CLASS_NAME, "list_news") # 클래스명이 list_news인 요소를 가져와 first_sel에 저장
second_sel = first_sel.find_elements(By.TAG_NAME, "li") # first_sel 요소에 li 태그 목록을 가져와 second_sel에 저장
news_title_lists = [] # second_sel에서 기사 내용을 하나씩 가져와 news_title_lists에 담는다.
for a in second_sel:
    news_title_lists.append(a.text.replace("\n", ""))

# 5. 가져온 기사를 엑셀 한 시트로 만든다. (pands 라이브러리 이용)
import pandas as pd
df = pd.DataFrame(news_title_lists) # news_title_lists에 있는 데이터를 pandas 데이터프레임으로 저장
df.to_excel('test.xlsx')

# 6. 가져온 기사 제목을 워드클라우드로 제작한다. (word-cloud 라이브러리 이용)
import WordCloud
from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS) # 불(Bool) 용어 지정(조사 등)
wc = WordCloud(font_path = 'BMJUA_ttf.ttf', stopwords = stopwords) # wc 변수에 wordcloud 객체 지정
wc.generate(str(news_title_lists))
wc.to_file('wordcloud_bm.png')
```

<br/>


## 유용한 블로그

 - https://velog.io/@lcs3947/selenium-driver-%EA%B4%80%EB%A6%AC-%EB%B0%8F-%EC%9C%A0%EC%9A%A9%ED%95%9C-%EA%B8%B0%EB%8A%A5
