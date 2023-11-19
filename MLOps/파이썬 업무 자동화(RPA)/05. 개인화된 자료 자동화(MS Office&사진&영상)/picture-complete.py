import os
import pandas as pd
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# 1. 명함을 저장할 디렉토리 생성
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory.' + directory)

createFolder('명함(onecode)')


# 2. 명함기본샘플 이미지에 회사 로고 삽입하기
# 흰색 샘플 배경 이미지에 회사 로고 삽입하기
img_logo = Image.open('Logo.jpg')
img_resize = img_logo.resize((140, 140)) # 회사 로고 사이즈 조정

img_basic = Image.open('명함기본샘플(90mm-50mm).jpg')
img_basic.paste(im = img_resize, box = (5, 24))
img_basic.save('명함(onecode)/명함기본샘플(90mm-50mm)_logo.jpg')


# 3. 엑셀 파일을 읽고 해당 데이터로 이미지에 글자 삽입하기 [명함 1,000개]
# 회사 로고 이미지에 텍스트 삽입하기
df = pd.read_excel('명함제작용data.xls')
width = int(90 * 96 / 25.4)
height = int(50 * 96 / 25.4)

for a in range(len(df)):
    # 명함 제작에 들어가는 텍스트 정하기(내용, 크기)
    df_unit = df.loc[a]
    fnt1 = ImageFont.truetype("SCDream3.otf", 20, encoding = "UTF-8")
    row1 = df_unit[0] # 회사명

    fnt2 = ImageFont.truetype("SCDream3.otf", 10, encoding = "UTF-8")
    row2 = df_unit[1] # 회사 주소

    fnt3 = ImageFont.truetype("SCDream3.otf", 15, encoding = "UTF-8")
    row3 = df_unit[2] + " " + df_unit[3] # 이름 + 직위

    fnt4567 = ImageFont.truetype("SCDream3.otf", 10, encoding = "UTF-8")
    row4 = df_unit[4] # 팀이름
    row5 = 'H.P:' + df_unit[5] + '/Tel:' + df_unit[6] # 전화번호, 사무실번호
    row6 = '/Email:' + df_unit[8] # 이메일
    row7 = df_unit[9] # 회사 웹사이트 주소
    text_list = [
        [row1, fnt1],
        [row2, fnt2],
        [row3, fnt3],
        [row4, fnt4567],
        [row5, fnt4567],
        [row6, fnt4567],
        [row7, fnt4567]
    ]

    # 명함 제작에 들어가는 텍스트 입력하기
    a = 0
    img = img_basic.copy()
    draw = ImageDraw.Draw(img)
    for unit in text_list:
        a = a + 25
        draw.text((150, a), unit[0], font = unit[1], fill = "black")
    
    img.save(f"명함(onecode)/{row3}.jpg") # 이름+직위 별로 명함 파일 만들기
    img.close()
