# 08장. 협업 자동화

## 팀을 위한 프로그램 제작 (PyInstaller 활용)

.py 혹은 .ipynb 파일을 다른 사람의 컴퓨터에서도 활용할 수 있도록 python 프로그램을 .exe 파일로 변환해주어야 한다.  

 - `PyInstaller`
    - 공식 문서: https://pyinstaller.org/en/stable/
```
1. 완성된 프로그램을 .py 파일로 변환
 - 주피터 노트북으로 코드를 작성한 경우 .ipynb 파일로 생성이 된다.
 - 주피터 노트북 > File > Download as > Python(.py) 을 눌러 .py 파일로 변환한다.

2. pyinstaller를 활용하여 .exe 파일 만들기
 - PyInstaller를 설치하고, 만든 .py 파일을 PyInstaller로 exe 파일로 변환한다.
!pip install pyinstaller
!pyinstaller 파일명.py
```

<br/>

## 팀과 함께 보는 데이터 공유 (구글 스프레드시트 활용)

 - `사전 내용`
    - 구글 스프레드시트를 파이썬과 연동하려면 구글 클라우드(Google Cloud)에서 구글 API를 받아야 한다.
    - 구글 클라우드 API 홈페이지: https://console.cloud.google.com/apis
```
1. 구글 API 발급
 - 구글 로그인 진행
 - 구글 클라우드의 API 및 서비스 페이지 접속
 - 프로젝트 생성
 - 서비스 계정 생성
 - 서비스 계정의 이메일 및 고유 ID 기록
 - 서비스 계정의 키 생성 후 보관
 - Google Sheets API 사용 설정
 - Google Drive API 사용 설정

2. 구글 드라이브에서 스프레드 시트 만들고 공유
 - 구글 스프레드시트 생성
 - 구글 스프레드시트를 구글 클라우드 서비스 계정의 이메일로 공유

3. 코드로 설정
 - 코드 실행
```

 - `코드 설정`
```py
# !pip install gspread == 5.4.0
# !pip install -upgrade oauth2client

import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Google Cloud API JSON 정보 파일 조회
file_list = os.listdir()
for file in file_list:
    if ".json" in file:
        output_name = file

# 스프레드 시트에서 가져온 데이터를 데이터프레임으로 변환
def gsheetdf(sheet):
    df = pd.DataFrame(columns = list(sheet.get_all_records()[0].keys()))
    for item in sheet.get_all_records():
        df.loc[len(df)] = item
    return df

# 구글 스프레드 시트를 파이썬과 연동시키기
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(output_name, scope)
spreadsheet_name = "스프레드시트 이름"
client = gspread.authorize(creds)
spreadsheet = client.open(spreadsheet_name)

sheet = spreadsheet.worksheet("시트1")
sheet.get_all_records() # 데이터 가져오기

df_sample_data = gsheetdf(sheet)
df_sample_data.head()

```

<br/>

## 구글 스프레드 시트 실습

 - `구글 설문지와 스프레드 시트 활용`
    - 특정 시트 불러오기
        - 이름으로 불러오기: spreadsheet.worksheet('시트명')
        - 순서로 불러오: spreadsheet.get_worksheet(0)
    - 시트에 있는 모든 데이터 가져오기: sheet_unit.get_all_records()
    - 셀 변경: sheet_unnit.update_acell('B1', '값')
    - 행 추가: sheet_unit.append_row(['값', '값', ..])
```py
# !pip install gspread == 5.4.0
# !pip install -upgrade oauth2client
# !pip install gspread_dataframe == 3.3.0

# 스프레드 시트에서 가져온 데이터를 데이터프레임으로 변환 함수
import os
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import gspread_dataframe as gd

def gsheetdf(sheet):
    df = pd.DataFrame(columns = list(sheet.get_all_records()[0].keys()))
    for item in sheet.get_all_records():
        df.loc[len(df)] = item
    return df

# 1. 구글 스프레드 시트 연동
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("JSON 파일", scope)
spreadsheet_name = "스프레드시트 이름"
client = gspread.authorize(creds)
spreadsheet = client.open(spreadsheet_name)

# 2. 해당 데이터를 원하는 형태로 가공
survey_sheet = spreadsheet.get_worksheet(0) # 응답지 시트 생성
df = gsheetdf(survey_sheet)
df.rename(columns = {'타임스탬프':'Time', '사번':'epnum', '일정':'class'}, inplace = True) # df 컬럼값 변경
df = df.drop_duplicates(['epnum'], keep = 'last') # 마지막만 남기기

# 클래스별 현황표 출력
result_df = df.pivot_table(index = 'class', values = 'epnum', aggfunc = 'count')
display(result_df)
result_df['class'] = result_df.index
result_df = result_df[['class', 'epnum']]
sheet_unit = spreadsheet.get_worksheet(1)

# 기존에 있던 데이터 모두 삭제
sheet_unit.clear()

# 만들어진 result_df를 원하는 시트에 넣기
gd.set_with_dataframe(sheet_unit, result_df)

```
