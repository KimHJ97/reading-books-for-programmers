# 2. 'practice/참고자료' 폴더의 엑셀 파일 목록에서 제목과 내용을 합쳐서 워드클라우드 제작

# !pip install python-pptx == 0.6.21
# !pip install wordcloud == 1.8.1

from pptx import Presentation # PopwerPoint 라이브러리
from wordcloud import WordCloud
import os
import pandas as pd

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
