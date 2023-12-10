# 03장. 유용한 라이브러리: 판다스와 넘파이

## 판다스(Pandas)

판다스(Pandas)는 파이썬 프로그래밍 언어를 위한 데이터 조작과 분석을 위한 라이브러리입니다. 주로 데이터프레임(DataFrame)과 시리즈(Series)라는 두 가지 주요 자료 구조를 제공하여 효과적으로 데이터를 다룰 수 있게 도와줍니다.  
 - 사람이 읽기 쉬운 형태의 자료구조를 제공한다.
 - 데이터프레임(DataFrame): 행과 열로 이루어진 테이블 형태의 자료 구조를 제공합니다. 이를 통해 엑셀과 유사한 형태의 데이터를 다룰 수 있습니다.
 - 시리즈(Series): 하나의 열(column)을 나타내는 자료 구조로, 1차원 배열과 비슷합니다. 데이터프레임은 여러 개의 시리즈로 이루어져 있습니다.
    - 하나 이상의 자료형을 원소로 가질 수 있다.
    - 테이블 형식의 작업(SQL 같은 쿼리나 조인) 가능
    - 2차원 이하 배열의 데이터만 가능
    - SQL, 엑셀 파일, CSV 파일, 데이터베이스에서 데이터를 읽어들일 수 있고, 데이터를 파일 형식으로 만들거나 데이터베이스에 올릴 수 있다.

<br/>

### 판다스(Pandas) 사용법

 - `판다스 기초 사용 예제`
    - 판다스 자료형
        - object: 텍스트와 같은 문자 형태
        - int64: 소수점이 없는 숫자
        - float64: 소수점이 있는 숫자
        - bool: 불리언 타입(True/False)
        - datetime64: 날짜/시간을 다루는 자료형
```python
import pandas as pd

# csv 파일 불러오기
file_url = 'URL 주소'
sample = pd.read_csv(file_url)

# 데이터 프레임 기본 함수 살펴보기
sample.head() # 앞부분의 데이터 정보 출력
sample.tail() # 뒷부분의 데이터 정보 출력
sample.info() # 데이터에 대한 요약 정보 출력
sample.describe() # 데이터 통계 정보 출력

# 데이터 프레임 직접 만들기
sample_dict = {
    'name': ['John', 'Ann', 'Kevin'],
    'age': [23, 22, 21]
}
pd.DataFrame(sample_dict)

# 데이터 프레임 columns와 index 만들기 (index는 보통 정의하지 않는다. 0 ~ n으로 기본적으로 정의된다.)
sample_array = [
    ['John', 23],
    ['Ann', 22],
    ['Kevin', 21]
]
pd.DataFrame(sample_array, columns = ['name', 'age'], index = ['a', 'b', 'c'])

# 컬럼 목록 출력
sample_df.columns
```

<br/>

 - `판다스 인덱싱`
    - 컬럼 인덱싱 수행시 [] 안에는 단 하나의 값만 넣을 수 있다. 때문에, 여러 컬럼을 인덱싱할 때는 [] 기호를 사용해서 여러 컬럼을 묶어서 한 번에 넣도록 한다.
```python
# 컬럼 인덱싱
sample_df['name']
sample_df[['name', 'age']]

# 행(인덱스 이름) 기준 인덱싱
sample_df.loc['a'] # a 인덱스
sample_df.loc[['a', 'b', 'c']] # a, b, c 인덱스
sample_df.loc['a':'c'] # a ~ c 인덱스

# 행(위치) 기준 인덱싱
sample_df.iloc[0]
sample_df.iloc[[0, 1, 2]]
sample_df.iloc[0:3]

# 행과 컬럼 동시에 인덱싱: iloc[행, 컬럼]
sample_df.iloc[0:3, 0:2] # 0~2 행, 0~1열(컬럼)
```

<br/>

 - `컬럼 혹은 행 제거`
    - 열을 삭제하기 위해서는 drop() 함수를 이용하며, 매개변수에 axis를 1로 지정해주어야 한다.
    - 두 개 이상의 컬럼을 제거하기 위해서도 리스트 형식으로 컬럼들을 묶어주어야 한다.
```python
# 컬럼(열) 제거
sample_df.drop('age', axis=1)
sample_df.drop(['name', 'age'], axis=1) # 2개 이상 제거시 리스트로 묶는다.

# 행 제거
sample_df.drop('a')
sample_df.drop(['a', 'b', 'c'])
```

<br/>

 - `기타 계산 함수`
    - 데이터프레임에서는 count(), sum() 등 간단하게 변수별 합, 평균, 표준편차 등을 계산할 수 있다.
    - 판다스에서는 groupby() 함수로 특정 변수를 기준으로 그룹을 만들어 계산할 수 있다.
    - unique() 함수를 이용해 해당 열(컬럼)에 고유한 값들을 확인할 수 있다.
```python
# 컬럼별 계산
sample_df.count()  # 데이터 갯수
sample_df.sum()    # 합
sample_df.mean()   # 평균
sample_df.median() # 중윗값
sample_df.var()    # 분산
sample_df.std()    # 표준편차
sample_df.aggregate(['sum', 'mean']) # 합과 평균 함꼐 보기

# 그룹별 계산: groupby()
iris.groupby('class').mean() # 꽃 종류를 그룹으로 평균값
iris.groupby('class').agg(['count', 'mean']) # 꽃 종류를 그룹으로 데이터 갯수와 평균

# 변수 내 고윳값 확인: unique()
iris['class'].unique()  # 고유값 정보 목록
iris['class'].nunique() # 고유값 갯수
iris['class'].value_counts() # 고유값 별로 몇 건의 데이터가 있는지 확인
```

<br/>

 - `데이터프레임 합치기`
    - 데이터를 결합하는 방법으로 크게 내부 조인(INNER JOIN), 전체 조인(FULL JOIN), 왼쪽 조인(LEFT JOIN), 오른쪽 조인(RIGHT JOIN)이 있다.
    - merge() 함수는 기본적으로 내부 조인을 수행한다. 공통된 key만 결합되고, 나머지 데이터는 버려진다.
    - concat() 함수 괄호 안에 리스트 형태로 결합할 데이터들을 넣어주면, 행 기준으로 결합된다. merge()나 join()과 다르게 데이터 이름 뒤에 붙여서 쓰지 않고, 판다스(pd) 뒤에 붙여서 사용한다. concat()은 기본적으로 마지막 행 아래에 결합시킨다. axis 매개변수를 1로 두어 열 기준으로 결합하도록 한다.
```python
# 내부 조인
left.merge(right)
left.merge(right, on = {'키 변수'}) # 키 지정

# 전체 조인
left.merge(right, how = 'outer')

# 왼쪽 조인
left.merge(right, how = 'left')

# concat() 함수로 결합
pd.concat([left, right]) # left 밑에 right 행이 추가된다.
pd.concat([left, right], axis=1) # 열 기준 결합
```

## 넘파이(NumPy)

넘파이(NumPy)는 파이썬에서 대규모 다차원 배열과 행렬을 다루기 위한 핵심 라이브러리입니다. 넘파이는 빠른 연산 속도와 효율적인 메모리 사용을 제공하여 수치 계산 및 데이터 분석과 같은 과학적, 공학적 작업에 매우 유용합니다.  
 - 컴퓨터가 계산하기 좋은 형태의 자료구조를 제공한다.
    - 같은 자료형만 원소로 가질 수 있다.
    - 행렬 및 벡터 연산 기반
    - 3차원 이상의 배열도 가능

<br/>


### 넘파이(NumPy) 사용법

 - `넘파이 기초 사용 예제`

```python
import numpy as np

# 1차원 배열
np.array([1, 2, 3])

# 2차원 배열
np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# DataFrame > ndarray
sample_np = np.array(sample_df)

# ndarray > DataFrame
pd.DataFrame(sample_np, columns = sample.df.columns)
```

<br/>

 - `인덱싱`
```python
sample_np[0] # 0행 출력
sample_np[0, 0] # 0행의 0번째 데이터 출력
sample_np[0:3, 0:2] # 0~2행, 0~1번째 데이터
sample_np[:, 2] # 모든행, 2번째 데이터
```

<br/>

 - `배열의 연산`
```python
# 산술 연산
np_a = np.array([[1, 3], [0, -2]])
np_a + 10 # 모든 데이터에 10이 더해진다.
np_a * 2 # 모든 데이터에 2가 곱해진다.

# 배열끼리 연산
np_b = np.array([[1, 0], [0, 1]])

np_a + np_b # 같은 자리에 있는 원소들끼리 덧셈
np_a - np_b # 같은 자리에 있는 원소들끼리 뺄셈
np_a * np_b # 같은 자리에 있는 원소들끼리 곱셈
np_a @ np_b # 수학 과정에서의 행렬 곱셈으로 곱셈
```

<br/>

 - `기타 함수`
```python
# 임의의 숫자 얻기: randint()
np.random.randint(11) # 0 ~ 10 사이의 임의의 숫자
np.random.randint(10, 31) # 10 ~ 30 사이의 임의의 숫자
np.random.randint(10, 31, 5) # 10 ~ 30 사이의 임의의 숫자 5개 array로 반환

# 주어진 목록에서 임의의 값 선택: random.choice()
np.random.choice(['red', 'green', 'white', 'black', 'blue'], size = 3) # 선택된 값이 또 선택될 수 있다.
np.random.choice(['red', 'green', 'white', 'black', 'blue'], size = 3, replace=False) # 선택된 값은 제외된다. (중복 X) 

# 일련의 숫자 만들기: arange()
np.arange(1, 11) # 1 ~ 10까지의 숫자 ndarray
np.arange(1, 11, 2) # [1, 3, 5, 7, 9]
```
