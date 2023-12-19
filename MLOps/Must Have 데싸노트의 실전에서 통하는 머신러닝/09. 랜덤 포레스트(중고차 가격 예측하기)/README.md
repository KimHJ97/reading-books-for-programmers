# 07장. 랜덤 포레스트: 중고차 가격 예측하기

## 랜덤 포레스트

랜덤 포레스트 모델은 결정 트리의 단점인 오버피팅 문제를 완화시켜주는 발전된 형태의 트리 모델이다.  
랜덤으로 생성된 무수히 많은 트리를 이용하여 예측을 하기 때문에 랜덤 포레스트라고 불린다.  
여러 모델을 활용하여 하나의 모델을 이루는 기법을 앙상블이라 부른다.  

앙상블 기법을 사용한 트리 기반 모델 중 가장 보편적인 방법이다.  
부스팅 모델에 비하면 예측력이나 속도에서 부족한 부분이 있고, 시각화에서는 결정 트리에 못미치나, 부스팅 모델을 이해하기 위해서는 꼭 알아야할 필수 알고리즘이다.  
 
 - 장점
    - 아웃 라이어에 거의 영향을 받지 않는다.
    - 선형/비선형 데이터에 상관없이 잘 동작한다.
 - 단점
    - 학습 속도가 상대적으로 느리다.
    - 수많은 트리를 동원하기 때문에 모델에 대한 해석이 어렵다.
 - 사용처
    - 종속변수가 연속형 데이터와 범주형 데이터인 경우 모두에서 사용할 수 있다.
    - 아웃라이어가 문제가 되는 경우 선형 모델보다 좋은 대안이 될 수 있다.
    - 오버피팅 문제로 결정 트리를 사용하기 어려울 때, 랜덤 포레스트를 사용할 수 있다.

<br/>

### 문제 정의

자동차 모델명, 연식, 마일리지, 성능 등 해외 중고차 거래 데이터셋을 이용해 중고차 가격을 예측한다.

 - 미션: 중고차 가격 예측
 - 알고리즘: 랜덤 포레스트
 - 데이터셋: 종속 변수는 판매 가격이며, 독립 변수로는 생산년도, 주행 거리, 변속기, 마일리지, 배기량 등이 있다.
 - 문제 유형: 회귀
 - 평가지표: RMSE
 - 사용 라이브러리
    - numpy: 1.19.5
    - pandas: 1.3.5
    - seaborn: 0.11.2
    - matplotlib: 3.2.2
    - sklearn: 1.0.2

<br/>

### 라이브러리 및 데이터 불러오기 & 데이터 확인

 - `데이터 확인`
    - 독립 변수(1개)
        - name: 이름
        - year: 생산년도
        - km_driven: 주행거리
        - fuel: 연료
        - seller_type: 판매자 유형
        - transmission: 변속기
        - owner: 차주 변경 내역
        - milleage: 마일리지
        - engine: 배기량
        - max_power: 최대 출력
        - torque: 토크
        - seats: 인승
    - 종속 변수(1개)
        - selling_price: 판매가
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/car.csv'
data = pd.read_csv(file_url)

data.head()
data.info() # 변수 특징 출력 -> 결측치 존재
round(data.describe(), 2) # 통계 정보 출력 -> 아웃 라이어 존재, selling_price의 max 값이 유독 높고, km_driven도 마찬가지
```

<br/>

### 전처리: 텍스트 데이터

문자형 데이터를 숫자형으로 바꾸어야 연산이 가능하다.  
첫 번째 작업으로는 단위 일치 및 숫자형으로 변환을 진행한다. 단위가 섞여 있으므로 단위를 통일하고, 그에 맞게 값을 계싼해주고 단위에 해당하는 텍스트를 제거해 숫자형으로 변경한다.  
두 번째 작업으로는 테스트 분류이다. 불필요하게 구체적인 내용의 텍스트는 버리고, 필요한 부분만 남긴다.  

우선 숫자형 데이터로 변경할 컬럼들을 다룬다. mileage, engine, max_power, torque 변수에는 숫자와 문자가 혼재되어 있다. 숫자와 문자를 분리시키고 숫자의 자료형을 float 형으로 지정한다.  
문자형 데이터 분리는 판다스 시리즈에서 제공하는 str.split()을 사용한다. 데이터프레임이 아닌 시리즈에만 있는 함수로 컬럼 하나씩 인덱싱해 처리해준다.  

```python
# engine 변수 전처리
data[['engine', 'engine_unit']] = data['engine'].str.split(expand=True)
data['engine'].head() # 엔진 변수 확인 -> dtype이 object이다.
data['engine'] = data['engine'].astype('float32') # 숫자형 변수로 변환

data['engine_unit'].unique() # 고유값 확인 -> CC라는 값만 존재 -> 제거
data.drop('engine_unit', axis=1, inplace=True)

# max_power 변수 전처리
data[['max_power', 'max_power_unit']] = data['max_power'].str.split(expand=True)
data['max_power'].head() # max_power 변수 확인 -> dtype이 object
data['max_power'] = data['max_power'].astype('float32') # 숫자형 변수로 변환 -> ValueError 발생 (bhp 문자가 존재)

data[data['max_power'] == 'bhp'] # max_power 변수에 bhp라는 문자가 있는지 확인


def isFloat(value): # 함수 정의
    try:
        num = float(value) # 값을 숫자로 변환
        return num # 변환된 값 리턴
    except ValueError:
        return np.NaN

data['max_power'] = data['max_power'].apply(isFloat) # 순회하면서 Float 값 변환

data['max_power_unit'].unique() # 고유값 확인 -> 문자열로 변수 제거
data.drop('max_power_unit', axis=1, inplace=True)

# mileage 변수 전처리
data[['mileage', 'mileage_unit']] = data['mileage'].str.split(expand=True)
data['mileage'] = data['mileage'].astype('float32') # 숫자형 변수로 변환

data['mileage_unit'].unique() # 고유값 확인 -> kmpl, km/kg, nan
data['fuel'].unique() # 고유값 확인 -> Diesel, Petrol, LPG, CNG

# mileage 변수를 각 연료별 가격으로 나누면 1달러당 주행거리가 된다.
def mile(x):
    if x['fuel'] == 'Petrol':
        return x['mileage'] / 80.43
    elif x['fuel'] == 'Diesel':
        return x['mileage'] / 73.56
    elif x['fuel'] == 'LPG':
        return x['mileage'] / 40.85
    else:
        return x['mileage'] / 44.23

# fuel과 mileage 두 변수를 사용하기 떄문에 함수에 data 전체를 파라미터로 넘긴다.
data['mileage'] = data.apply(mile, axis=1) # mile 함수로 마일리지 수정

data.drop('mileage_unit', axis=1, inplace=True) # 변수 제거

# torque 변수 전처리 -> 단위 앞부분 숫자만 추출해 숫자형으로 바꾼 후, Nm 단위로 스케일링한다.
data['torque'].head() # 값 확인

data['torque'] = data['torque'].str.upper()

def torque_unit(x):
    if 'NM' in str(x):
        return 'Nm'
    elif 'KGM' in str(x):
        return 'kgm'

data['torque_unit'] = data['torque'].apply(torque_unit)
data['torque_unit'].unique() # 고유값 확인 -> Nm, kgm, None

data['torque_unit'].isna() # torque_unit이 Null 값인지 확인
data[data['torque_unit'].isna()] # 얻은 결과를 data[] 안에 넣어 필터링
data[data['torque_unit'].isna()]['torque'].unique() # 필터링된 데이터에서 torque의 unique 값 확인

# Nm은 보통 100, 200 같은 백 단위, kgm은 10, 20 등 십 단위 -> 모두 Nm에 해당한다고 추론
data['torque_unit'].fillna('Nm', inplace=True)

def split_num(x):
    x = str(x) # 문자 형태로 변환
    for i,j in enumerate(x): # 인덱스를 포함한 순회
        if j not in '0123456789.': # j가 0123456789.에 속하지 않으면
            cut = i # 인덱스 순서를 cut에 저장
            break # 순회 중지
    return x[:cut] # cut 이전 자리까지 인덱싱하여 리턴

data['torque'] = data['torque'].apply(split_num)
data['torque'] = data['torque'].astype('float64') # 숫자 형태로 변환 -> ValueError

data['torque'] = data['torque'].replace('', np.NaN) # ''를 결측치로 대체
data['torque'] = data['torque'].astype('float64') # 숫자 형태로 변환

def torque_trans(x): # 단위 차이를 맞추기 위한 값 계산 함수
    if x['torque_unit'] == 'kgm':
        return x['torque'] * 9.8066
    else:
        return x['torque']

data['torque'] = data.apply(torque_trans, axis=1) # 단위별 값 맞추기
data.drop('torque_unit', axis=1, inplace=True) # 변수 제거

# name 변수 전처리 -> 브랜드/모델명이 담겨있다.
    # 수많은 모델을 담으면 좋지만, 더미 변수를 만들때 수 많은 컬럼이 추가되어 좋지 않다.
    # 모델 이름보다는 모델이 갖고 있는 engine, max_power, torque 등으로 구분할 수 있다.
    # 다만, 브랜드명은 가지고 가야한다. 동일 스팩이더라도 브랜드별로 가격이 다를 수 있다.
data['name'] = data['name'].str.split(expand=True)[0] # name 변수를 공백으로 나누고 첫 번쨰 부분만 가져오기
data['name'].unique() # 고유값 확인 -> 브랜드 이름이 아닌 다른 값이 분리될 수도 있으니 확인
data['name'] = data['name'].replace('Land', 'Land Rover') # 띄어쓰기로 브랜드명이 절삭되었음

```

<br/>

### 전처리: 결측치 처리와 더미 변수 변환

```python
data.isna().mean() # 변수별 결측치 평균 확인 -> 결측치 비율 2%인 값들이 있음
data.dropna(inplace=True) # 결측치 행 제거 -> 2% 수준으로 높지 않아 과감하게 해당 행 제거

# 남은 텍스트 컬럼을 더미 변수로 변환
    # name, fuel, seller_type, transmission, owner가 있다.
data = pd.get_dummies(data, columns = ['name', 'fuel', 'seller_type', 'transmission', 'owner'], drop_first=True)
```

<br/>

### 모델링 및 평가하기

```python
# 훈련셋과 시험셋 나누기
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data.drop('selling_price', axis=1), data['selling_price'], test_size=0.2, random_state=100)

# 랜덤 포레스트 모델 만들기
    # 랜덤 포레스트는 매번 다른 방식으로 나무를 생성하여 random_state를 지정하는 것이 좋다.
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(random_state=100) # 모델 객체 생성
model.fit(X_train, y_train)
train_pred = model.predict(X_train) # 훈련셋 예측
test_pred = model.predict(X_test) # 시험셋 예측

from sklearn.metrics import mean_squared_error
print("train_rmse:", mean_squared_error(y_train, train_pred) ** 0.5, "test_rmse:", mean_squared_error(y_test, test_pred) ** 0.5)
```

<br/>

### 이해하기: K-폴드 교차검증

교차검증의 목적은 모델의 예측력을 더 안정적으로 평가하기 위함이다.  
새로운 데이터를 얼마나 잘 예측하는지 확인하고자 훈련셋과 시험셋을 나누어 평가하고, 이러한 데이터 분할은 랜덤 샘플링으로 이루어져 어느정도 안정적인 보장을 받는다.  
하지만, 랜덤 샘플링으로 나누어졌더라도 우연에 의한 오차들이 예측력을 평가하는 데 작은 노이즈로 존재할 수 있다.  

K-폴드 교차검증은 데이터를 특정 개수(k개)로 쪼개어서 그중 하나씩을 선택하여 시험셋으로 사용하되, 이 과정을 K번만큼 반복하는 것이다.  
여러번 반복 모델링을 수행하여 얻어진 평갓값(오차)를 평균내어 최종 평갓값(RMSE)를 도출한다.  
이러한 과정을 직접 코딩할 수도 있지만, 이미 사이킷런에서 패키지(KFold)로 제공한다.  

```python
from sklearn.model_selection import KFold

# KFold는 인덱스 값을 이용하여 데이터를 분할한다.
# 중간에 빈값이 존재하면 에러가 발생하여 인덱스를 정리한다.
data.reset_inmdex(drop=True, inplace=True)

kf = KFold(n_splits=5) # KFold 객체 생성

X = data.drop('selling_price', axis=1)
y = data['selling_price']

for i, j in kf.split(X):
    print(i, j)

for train_index, test_index in kf.split(X):
    X_train, X_test = X.loc[train_index], X.loc[test_index]
    y_train, y_test = y[train_index], y[test_index]


train_rmse_total = []
test_rmse_total = []

for train_index, test_index in kf.split(X):
    X_train, X_test = X.loc[train_index], X.loc[test_index]
    y_train, y_test = y[train_index], y[test_index]

    model = RandomForestRegressor(random_state=100)
    model.fit(X_train, y_train)
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    train_rmse = mean_squared_error(y_train, train_pred) ** 0.5
    test_rmse = mean_squared_error(y_test, test_pred) ** 0.5

    train_rmse_total.append(train_rmse)
    test_rmse_total.append(test_rmse)

print("train_rmse:", sum(train_rmse_total)/5, "test_rmse:", sum(test_rmse_total)/5)
```

<br/>

### 이해하기: 랜덤 포레스트

랜덤 포레스트는 결정 트리의 집합체로 여러 트리를 활용하여 최종 모델을 만든다.  
다양한 트리의 의견을 반영하기 떄문에 오버피팅 위험을 낮출 수 있다.  
랜덤 포레스트가 여러 개의 트리를 만들 때는 데이터 전체를 사용하지 않고, 매번 다른 일부의 데이터를 사용하여 다른 트리를 만들어 낸다.  

랜덤 포레스트의 최종 예측값은 각 트리의 예측값들을 기반으로 만들어진다.  
회귀 문제는 연속형 변수를 예측하기 떄문에, 각 트리에서 만들어낸 예측값들의 평균값을 랜덤 포레스트의 최종 예측값으로 사용한다.  
분류 문제는 각 트리에서 예측한 값들 중 최다 투표값으로 랜덤 포레스트의 예측값이 결정된다.  

<br/>

### 하이퍼파라미터 튜닝

랜덤 포레스트는 수 많은 하이퍼파라미터를 가지고 있다.  

 - n_estimators
    - 랜덤 포레스트를 구성하는 결정 트리의 개수.
    - 기본값은 100으로 설정된다.
    - 너무 많거나 적은 수를 입력하면 성능이 떨어지므로 적정 수준의 값을 찾아서 넣어야 한다.
 - max_depth
    - 각 트리의 최대 깊이를 제한한다.
    - 숫자가 낮을수록 오버피팅을 피할 수 있으며, 또한 언더피팅의 위험도는 올라간다.
 - min_samples_split
    - 해당 노드를 나눌 것인지 말 것인지를 노드 데이터 수를 기준으로 판단한다.
    - 이 매개변수에 지정된 숫자보다 적은 수의 데이터가 노드에 있으면 더는 분류하지 않는다.
    - 숫자가 높을수록 분리되는 노드가 적어진다. 즉, 오버피팅을 피하지만 언더피팅의 위험이 있다.
    - 기본값은 2이다.
 - min_samples_leaf
    - 분리된 노드의 데이터에 최소 몇 개의 데이터가 있어야 할지를 결정하는 매개변수
    - 여기에 지정된 숫자보다 적은 수의 데이터가 분류된다면, 해당 분리는 이루어지지 않는다.
    - 숫자가 클수록 오버피팅을 피할 수 있지만 언더피팅의 위험이 있다.
    - 기본값은 1이다.
 - n_jobs
    - 병렬 처리에 사용되는 CPU 코어 수
    - 많은 코어를 사용할수록 속도가 빨라지며, -1을 입력하면 지원하는 모든 코어를 사용한다.
    - 기본값은 None으로 실제는 1개 코어를 사용한다.

```python
train_rmse_total = []
test_rmse_total = []

for train_index, test_index in kf.split(X):
    # X_train, X_test 정의
    X_train, X_test = X.iloc[train_index,:], X.iloc[test_index, :]
    y_train, y_test = y[train_index], y[test_index]

    # 하이퍼파라미터를 지정하여 모델 객체 생성
    model = RandomForestRegressor(n_estimators = 300, max_depth = 50, min_samples_split = 5, min_samples_leaf = 1, n_jobs=-1, random_state=100)
    model.fit(X_train, y_train)
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    # 훈련셋 rmse 계산
    train_rmse = mean_squared_error(y_train, train_pred) ** 0.5
    test_rmse = mean_squared_error(y_test, test_pred) ** 0.5

    train_rmse_total.append(train_rmse)
    test_rmse_total.append(test_rmse)

```

<br/>

### 학습 마무리

 - `핵심 용어`
    - 교차검증: 다양한 훈련셋/시험셋을 통하여 모델에 더 신뢰할 수 있는 평가를 하는 방법
    - 앙상블: 여러 모델을 만들고 각 예측값들을 투표/평균 등으로 통합하여 더 정확한 예측을 도모하는 방법

