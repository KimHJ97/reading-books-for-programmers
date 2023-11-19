# 04장. 데이터 처리 자동화(데이터 관리&편집 자동화)

## 데이터 자동화가 필요한 상황

일을 하다 보면 종종 엑셀 데이터 관리, 편집하는 작업을 반복해야 할 경우가 있다. 가령 여러 팀이 보낸 자료를 취합하는 일이나 여러 결과 데이터를 통계하여 하나의 파일로 만드는 작업이 있다.  

<br/>

## pandas 설치 및 기본 문법

pandas는 데이터 조작 및 분석을 위한 Python 프로그래밍 언어용으로 작성된 소프트웨어 라이브러리이다.  
데이터프레임처럼 열과 행으로 이루어진 데이터를 처리할 수 있으며, 특히 숫자 테이블과 시계열을 조작하기 위한 데이터 구조와 연산을 제공한다.  

pandas에서는 행과 열로 이루어진 표 형식의 데이터 구조를 DataFrame(데이터프레임) 이라고 한다.  

 - `사전 준비`
    - pandans 라이브러리 설치
```py
!pip install pandas == 1.4.3
import pandas as pd
```

<br/>

 - `pandas 기본 문법`
    - 인덱스 확인: data.index
    - 열 이름 확인: data.columns
    - 행/열 구조 확인: data.shape
    - 최초 5개의 행 확인: data.head()
    - 마지막 5개의 행 확인: data.tail()
    - 값 변경: data["컬럼명"].replace("찾을값", "대체값")
    - 결측치: data["컬럼명"].isnull()
    - 결측치 대체: data["컬럼명"].fillna("대체값")
    - 데이터 프레임 복사: data2 = data.copy()
    - 기본 연산
        - 열 값의 평균치: data["컬럼명"].mean()
        - 열 값의 최솟값: data["컬럼명"].min()
        - 열 값의 최댓값: data["컬럼명"].max()
        - 열 값의 합계: data["컬럼명"].sum()
        - 기본 통계치: data["컬럼명"].describe()
    - 데이터 조회
        - 지정 열 데이터만 조회: data[["컬럼명", "컬럼명"]]
        - 지정 행 데이터만 조회: data.loc([[1, 2, 5]])
        - 지정 행/열 데이터만 조회: data.loc[[1,2,3], ["컬럼명", "컬럼명"]]
    - 데이터 삭제
        - 행 값 삭제는 drop() 메서드를 이용하며, 기존 변수에 다시 저장해주어야 저장된다.
        - 행 값 삭제: data = data.drop(행번호, axis = 'index')
        - 열 값 삭제: data = data.drop(컬럼명, axis = 'columns')
    - 데이터 일치 여부 확인
        - 값 일치 여부: data["컬럼명"] == "값"
        - 값이 일치만 데이터만 출력: data[data["컬럼명"] == "값"]
        - 특정 값이 포함된 데이터 검색: data[data["컬럼명"].str.contains("값")]

<br/>

 - `pandas Pivot table & concat`
    - 피벗 테이블과 concat 외에도 pandas 문법 중에 merge, join, groupby 등이 있다.
```py
# Pivot table
pd.pivot_table(data, index = "트레이너", values = "몸무게")

# pivot 테이블에 들어오는 값의 이름은 values라는 이름으로 사용된다.
pd.pivot_table(data, index = ["지점명", "트레이너"], values = "몸무게")

# index는 리스트 형태로 값을 넣을 수 있다.
pd.pivot_table(data, index = ["지점명", "트레이너"], values = "몸무게", aggfunc = ["sum", "mean"]) # 합계 & 평균

# Concat
data246 = data.loc[[2, 4, 6]] # 2, 4, 6 행번의 데이터 만들기
data389 = data.loc[[3, 8, 9]] # 3, 8, 9 행번의 데이터 만들기
dpd.concat([data246, data389], axis = 0)
```

<br/>

## pandas 활용 예시

 - `행과 열 변경 작업`
```py
import pandas as pd

df = pd.read_excel("excel_sample.xlsx")
df1 = df.transpose()
df1 = df1.rename(columns = df1.iloc[0])
df1 = df1.drop(df1.index[0])
display(df1)
df1.to_excel("excel_sample_trans.xlsx")
df2 = df
df2.index = df2['Unnamed: 0'].values
df2.drop(['Unnamed: 0'], axis = 1, inplace = True)
display(df2)
```

<br/>

 - `2개의 데이터를 합치기`
```py
import pandas as pd

df = pd.DataFrame({
    'month': [1, 4, 7, 10],
    'year': [2012, 2014, 2013, 2014],
    'sale': [55, 40, 84, 31]
})
df2 = pd.DataFrame({
    'month': [3, 5, 11, 10],
    'year': [2015, 2016, 2017, 2018],
    'sale': [12, 20, 34, 41]
})

df = df.transpose()
display(df)

df2 = df2.transpose()
display(df2)

data = pd.concat([df, df2])
display(data)
```

<br/>

## 데이터 처리 자동화 실습

 - `엑셀 파일 취합하기`
    - 폴더 안에 있는 엑셀 파일 확인하기
    - 각각의 엑셀 파일을 열어서 상태 확인하기
    - 각 엑셀 파일의 구조를 편집하여 데이터 Unit으로 저장하기
    - 전체 엑셀 파일의 구조를 편집하여 하나의 데이터로 저장하기
    - 정리된 데이터 파일을 pivot을 사용ㅎ해서 제품별 정리된 내용을 분할하여 저장하기
```py
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
for d in dict(product_list): # dict(product_list): {'metaverse': 89, 'battery': 86, 'automobile': 81, ..}
    xls_name = data_unit_sum[data_unit_sum['조사제품'] == d]
    xls_name.to_excel(f"{d}.xlsx")

```
