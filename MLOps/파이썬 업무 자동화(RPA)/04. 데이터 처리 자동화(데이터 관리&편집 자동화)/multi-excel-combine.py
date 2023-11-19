# 1. 필요한 라이브러리 설치하기
import pandas as pd
import os # 파일 저장시 원하는 시스템 경로나 파일명을 지정하기 위한 라이브러리

# 2. 취합할 엑셀 파일의 자료 가져오기
# ex) 제품_나라이름_제품카테고리.xlsx -> product_taiwan_semiconductor.xlsx
basic_folder = 'new_data2'
file_list = os.listdir(f"./{basic_folder}")
file_list_xls = []
for fileName in file_list:
    if '.xlsx' in fileName:
        file_list_xls.append(fileName)

# 3. 각 엑셀 파일을 원하는 구조로 편집한 후 취합하여 통합 파일 만들기
data_unit_sum = pd.DataFrame()
for fileName in file_list_xls:
    df = pd.read_excel(f"./{basic_folder}" + fileName) # 엑셀 파일을 데이터프레임(df) 변수에 담는다.
    df['나라'] = fileName.split("_")[1] # 파일명의 나라가 데이터프레임에 마지막 열에 추가된다. ("조사제품", "제목", "내용", "나라" 순서)
    data_unit = df[['나라', '조사제품', '제목', '내용']] # 데이터프레임의 순서를 변경한다. ("나라", "조사제품", "제목", "내용" 순서)
    data_unit_sum = pd.concat([data_unit_sum, data_unit], axis = 0) # data_unit_sum 데이터프레임에 만들어진 데이터유닛을 합친다.
data_unit_sum.to_excel('combined_excel.xlsx')

# 4. 만들어진 파일(합쳐진 파일)을 기반으로 제품별로 구분하여 분할 저장하기
product_list = data_unit_sum['조사제품'].value_counts() # 값별로 갯수를 조회 (SQL로 치면 GROUP BY + COUNT 함수)
for d in dict(product_list):
    xls_name = data_unit_sum[data_unit_sum['조사제품'] == d]
    xls_name.to_excel(f"{d}.xlsx")
