# 05장. 개인화된 자료 자동화(MS Office&사진&영상)

## 개인화된 자료 자동화가 필요한 상황

MS Office(PPT, Excel) 등 많은 소프트웨어를 활용해 내부 인원들이 볼 수 있도록 공유하거나, 고객 및 협력사에 보내는 자료 등을 만든다.  
이떄, 주간업무 보고서, Daily 시황보고서, 대량의 상장/명함/수료증 그리고 지역별로 보내야 하는 홍보 영상 등 반복적으로 제작하는 경우가 있다.  

파이썬을 활용해 개인화된 자료 제작에 드는 시간을 줄일 수 있다.  

<br/>

## 사전 내용

 - `MS Office 자동화 관련 라이브러리 설치`
```py
# 엑셀: openpyxl
!pip install openpyxl == 3.0.10

# 파워포인트: python-pptx
!pip install python-pptx = 0.6.21

# 워드: python-docx
!pip install python-docs == 0.8.11

```

<br/>

## 엑셀 라이브러리(openpyxl)

 - `엑셀 자동화 라이브러리 기본 문법`
    - 공식 문서: https://openpyxl.readthedocs.io/en/stable/
    - 워크북 만들기: wb = openpyxl.Workbook()
    - 시트 만들기: wb.create_sheet('SheetName', 0)
    - 시트 삭제: wb.remove_sheet(wb['SheetName'])
    - 엑셀 파일 로드: wb = openpyxl.load_workbook('FileName')
    - 시트 접근: ws = wb['SheetName']
    - 셀 접근
        - ws['B1'] = '값'
        - ws(row = 값, column = 값).value = '값'
```py
# 엑셀 파일 생성 후 시트 만들기
wb = openpyxl.Workbook()

wb.create_sheet('sheet_name1', 0)
wb.create_sheet('sheet_name2', 0)
wb.create_sheet('sheet_name3', 0)
wb.create_sheet('sheet_name4', 0)

wb.save('basic/test.xlsx')

# 시트 삭제 후 종료
wb.remove_sheet(wb['sheet_name4'])

wb.save('basic/test.xlsx')
wb.close()

# 엑셀 파일 로드
wb = openpyxl.load_workbook('basic/text.xlsx')

# 셀의 값 입력
ws = wb['sheet_name1'] # 시트 접근
ws['B1'] = 'Hello' # 시트의 B1 셀의 접근

ws = wb['sheet_name1'] # 시트 접근
ws.cell(row = 1, column = 2).value = 'Hello' # 1행 2열 셀의 접근

ws.append(['Hello', 'World!']) # 현재 활성화된 행의 바로 아래 행에 데이터 삽입
```

<br/>

 - `여러 엑셀 파일을 한 파일로 합치기`
```py
import os
import pandas as pd

try:
    # 'basic' 폴더의 엑셀 파일 목록 추출
    files = os.listdir('basic')
    excel_files = []
    for fileName in files:
        if '.xls' in fileName:
            excel_files.append(fileName)

    # padans로 데이터프레임 변수를 만들고, 'basic' 폴더의 엑셀 파일 목록의 데이터를 추가
    excel = pd.DataFrame()
    for excelFileName excel_files:
        df = pd.read_excel('basic/' + excelFileName)
        excel = excel.append(df, ignore_index = True)
    
    excel.to_excel('basic/total.xlsx') # 합쳐진 데이터프레임을 엑셀 파일로 저장
except Exception as ex:
    print('error' + str(ex))

```

<br/>

 - `여러 엑셀 파일을 시트로 분할 저장하기`
    - with as 문법은 파일을 열고 특정 코드를 모두 실행한 다음 파일을 닫아주는 역할을 한다.
    - with as 문을 사용하면 close() 메서드를 생략할 수 있다.
```py
import pandas as pd

try:
    # 'basic' 폴더의 엑셀 파일 목록 추출
    files = os.listdir('basic')
    excel_files = []
    for fileName in files:
        if '.xls' in fileName:
            excel_files.append(fileName)

    saveFileName = 'basic/totla_sheet.xlsx'
    saveDir = os.path.join('', saveFileName)
    with pd.ExcelWriter(saveDir) as writer:
        for fileName in excel_files:
            df = pd.read_excel('basic/' + fileName) # 엑셀 파일 목록의 엑셀 하나를 읽어 데이터프레임 변수에 저장
            df.to_excel(writer, sheet_name = file_name.replace('.xlsx', '')) # 하나의 엑셀 시트로 해당 데이터프레임을 저장

except Exception as ex:
    print('error' + str(ex))
```

<br/>

## 파워포인트 자동화 라이브러리(python-pptx)

 - `파워포인트 자동화 라이브러리 기본 문법`
    - 공식 문서: https://python-pptx.readthedocs.io/en/latest/index.html
```py
from pptx import Presentation
from pptx.util import Inches

# PPT 파일 만들기
prs = Presentation()
prs.save('basic/test.pptx')

# 슬라이드 생성
title_slide_layout = prs.slide_layouts[0] # 첫 번째 양식으로 슬라이드 객체 변수 생성
slide = prs.slides.add_slide(title_slide_layout) # PPT에 슬라이드 추가
prs.save('basic/test.pptx')

# 슬라이드 양식 갯수 확인
print(len(prs.slide_layouts))

# 슬라이드에 내용 입력
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = 'Hello, World!'
subtitle.text = 'python-pptx was here!'
prs.save('basic/text.pptx')

# 슬라이드에 이미지 첨부
img_path = 'images/test.png'
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

top = Inches(0) # 이미지의 시작 위치(y)
left = Inches(0) # 이미지의 시작 위치(x)
height = Inches(10) # 이미지의 세로 너비
width = Inches(10 / 1.33) # 이미지의 가로 너비
slide.shapes.add_picture(img_path, left, top, height, width)
prs.save('basic/img_add.pptx')

# 슬라이드에 영상 첨부
video_path = 'videos/test.mp4'
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

top = Inches(0) # 이미지의 시작 위치(y)
left = Inches(0) # 이미지의 시작 위치(x)
height = Inches(10) # 이미지의 세로 너비
width = Inches(10 / 1.33) # 이미지의 가로 너비
slide.shapes.add_movie(video_path, left, top, height, width)
prs.save('basic/video_add.pptx')
```

<br/>

## MS Word 자동화 라이브러리(python-docs)

 - `MS Word 자동화 라이브러리 기본 문법`
    - 공식 문서: https://python-docx.readthedocs.io/en/latest/index.html
```py
from docs import Document
from docx.shared import Inches

# 문서 저장
document = Document()
document.save('basic/text.docx')

# 현재 위치 이후에 새로운 단락(텍스트) 추가
paragraph = document.add_paragraph('Welcome to python-docs')
document.save('basic/text.docx')

# 현재 위치 전에 새로운 단락(텍스트) 추가
before_paragraph = document.insert_paragraph_before('Before Paragraph')
document.save('basic/text.docx')

# 제목 텍스트 추가
document.add_heading('Heading Text')
document.add_heading('Heading Text', level = 2)
document.add_heading('Heading Text', level = 3)
document.save('basic/text.docx')

# 새로운 페이지 만들기
document.add_page_break()
document.add_heading('new_page')
document.save('basic/text.docx')

# 표(테이블) 추가
table = document.add_table(rows = 2, cols = 2)
cell = table.cell(0, 1) # 특정 셀 접근
cell.text = 'Hello'

row = table.rows[1] # 특정 행 접근
row.cells[0].text = 'Hello'
row.cells[1].text = 'World!'

print(len(table.rows)) # 행 갯수(row_count)
print(len(table.columns)) # 열 갯수(col_count)

document.save('basic/text.docx')

# 이미지 추가
document.add_picture('images/test.png')
document.add_picture('images/test.png', width = Inches(5.5)) # 이미지 크기 조정
document.save('basic/text.docx')
```

<br/>

## 개인화된 자료 자동화 실습

 - `엑셀 목록을 하나의 엑셀 파일의 시트로 통합 후 워드클라우드와 제품별 PPT 정리`
    - 통합 엑셀 만들기
        - 비어 있는 엑셀 만들기 (product_info.xlsx)
        - 해당 제품의 이름으로 Sheet 만들기
        - 엑셀 파일을 하나씩 불러오기
        - 불러온 엑셀 파일의 내용물을 통합 엑셀의 시트에 하나씩 집어넣기
        - 통합 엑셀 저장하기
    - 상품별 PPT 만들기
        - 비어 있는 PPT 만들기 (product_wordcloud.ppt)
        - 엑셀 파일을 하나씩 불러오기
        - 불러온 엑셀 파일의 제목과 내용을 합쳐서 워드클라우드로 만들기
        - 제작한 사진을 PPT에 첨부하고, 제목과 내용을 적어 하나의 파일로 저장하기
    - pd.ExcelWriter() 메서드는 엑셀 파일에 데이터를 입력하는 기능을 하며, 세부 시트에 각 파일에 있는 데이터를 입력한다.
```py
import openpyxl # Excel 라이브러리
from openpyxl import load_workbook # Excel 라이브러리
import os
from pptx import Presetation # PPT 라이브러리
import sys
from wordcloud import WordCloud
from pptx.util import Inches
import pandas as pd

##### 1. 각각의 엑셀데이터를 하나의 엑셀을 만들어 시트로 이동

# 1-1. 비어있는 엑셀 만들기
wb = openpyxl.Workbook()
wb.create_sheet('car', 0)
wb.create_sheet('semiconductor', 0)
wb.create_sheet('metaverse', 0)
wb.create_sheet('battery', 0)
wb.save('product_info.xlsx')

# 1-2. 'practice/참고자료' 폴더의 Excel 파일 목록 담기
path = "practice/참고자료/"

file_list = os.listdir(path)
file_list_xls = []
for file in file_list:
    if ".xlsx" in file:
        file_list_xls.append(file)

# 1-3. Excel 파일 목록의 데이터프레임 출력
for file in file_list_xls:
    df = pd.read_excel(f"practice/참고자료/{file}")
    print(df)

# 1-4. 불러온 엑셀 파일의 내용을 product_info.xls 시트에 한 개씩 넣고 저장하기
path_dir = "practice/참고자료/"
files = os.listdir(path_dir)
file_list_xls = []
for file in files:
    if '.xls' in file:
        file_list_xls.append(file)

file_nm = "product_info.xlsx"
with pd.ExcelWriter(file_nm) as writer:
    for file_name in file_list_xls:
        df = pd.read_excel("practice/참고자료/" + file_name) # Excel 파일의 데이터프레임 조회
        df.to_excel(writer, sheet_name = file_name.replace('.xlsx', '')) # 'product_info.xlsx' 파일에 Excel 파일의 이름으로 시트를 만들어 저장한다.


##### 2. 'practice/참고자료' 폴더의 엑셀 파일 목록에서 제목과 내용을 합쳐서 워드클라우드 제작
prs = Presentation() # 파워포인트 객체 선언

# 2-1. file_list_xls에 Excel 파일 목록 담기
path = "practice/참고자료"
file_list = os.listdir(path)
file_list_xls = []
for file in file_list:
    if ".xlsx" in file:
        file_list_xls.append(file)

# 2-2. Excel 파일 목록의 데이터프레임 출력
for file in file_list_xls:
    df = pd.read_excel(f"practice/참고자료/{file}")
    print(df)

# 2-3. Excel 파일 목록의 제목과 내용을 합쳐서 워드클라우드로 제작
for file in file_list_xls:
    df = pd.read_excel(f"practice/참고자료/{file}")
    df["제목&내용"] = df["제목"] + df["내용"]

    str_unit_sum = ''
    for a in range(df.shape[0]):
        str_unit = df.loc[a, "제목&내용"]
        str_unit_sum = str_unit_sum + str_unit
    
    wc = WordCloud(font_path = "practice/MBJUA_ttf.ttf")
    wc.generate(str(str_unit_sum))
    product_name = file.replace(".xlsx", "")
    wc.to_file(f'practice/{product_name}_wordcloud_1.png')


##### 3. 'product_info.xlsx' 엑셀 파일의 시트별 파워포인트 제작
wb = load_workbook('product_info.xlsx')
sheet_names = wb.sheetnames

for sheet in sheet_names:
    prs = Presentation()

    # PPT 슬라이드 생성(텍스트용)
    title_slide_layout = prs.slide_layouts[0] # title_slide_layout 변수에 첫 번째 양식 추가
    slide = prs.slides.add_slide(title_slide_layout) # 슬라이드 추가(첫 번쨰 양식)

    # PPT 내용 입력
    title = slide.shapes.title # 타이틀 텍스트 입력
    subtitle = slide.placeholders[1] # 텍스트 상자 줄 2번째 상자에 입력
    title.text = sheet
    subtitle.text = "뉴스기사 제목+내용 텍스트 기반 워드클라우드"

    # PPT 슬라이드 생성(사진용)
    img_path = f'practice/{sheet}_wordcloud_1.png'
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # PPT 이미지 첨부
    top = Inches(0) # 이미지의 시작 위치(y)
    left = Inches(0) # 이미지의 시작 위치(x)
    height = Inches(10) # 이미지의 세로 너비
    width = Inches(10 / 1.33) # 이미지의 가로 너비
    pic = slide.shapes.add_picture(img_path, left, top, height, width)
    prs.save(f'practice/{sheet}.pptx')

```