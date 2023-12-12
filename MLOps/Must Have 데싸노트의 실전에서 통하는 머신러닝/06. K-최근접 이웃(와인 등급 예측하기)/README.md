# 06장. K-최근접 이웃(KNN): 와인 등급 예측하기

## K-최근접 이웃

K-최근접 이웃은 거리 기반 모델로 선형 관계를 전제로 하지는 않는다.  
각 데이터 간의 거리를 활용해서 새로운 데이터를 예측하는 모델이다.  
이때, 가까이에 있는 데이터를 고려하여 예측값이 결정된다.  

다중분류 문제에서 가장 간편히 적용할 수 있는 알고리즘으로 데이터가 크지 않고 예측이 까다롭지 않은 상황에서 KNN을 사용하면 신속하고 쉽게 예측 모델을 구현할 수 있다.
 
 - 장점
    - 수식에 대한 설명이 필요 없을 만큼 직관적이고 간단하다.
    - 선형 모델과 다르게 별도의 가정이 없다.
 - 단점
    - 데이터가 커질수록 상당히 느려질 수 있다.
    - 아웃라이어에 취약하다.
        - 아웃라이어(이상치): 평균치에서 크게 벗어나는 데이터를 의미한다. 예를들어, 축구 선수 평균 연봉이 2억일때 스타 플레이어 연봉이 150억 이상인 경우 이것을 아웃라이어라고 볼 수 있다.
 - 사용처
    - 분류에서 사용되며, 로지스틱 회귀로 해결할 수 없는 3개 이상의 목표 변수들도 분류할 수 있다.
    - 작은 데이터셋에 적합하다.

<br/>

### 문제 정의

이름, 성별, 나이, 티켓 번호 등 같은 정보가 실제로 생존에 어떤 영향을 미치는지 확인한다.  

 - 미션: 와인 정보가 들어 있는 데이터셋을 이용해 와인 등급 예측
 - 알고리즘: KNN
 - 데이터셋: 와인에 대한 데이터. 총 3가지 목표값으로 이루어진 범주형 변수로 다중 분류 문제에 해당한다.
 - 문제 유형: 분류
 - 평가지표: 정확도
 - 사용 라이브러리
    - numpy: 1.19.5
    - pandas: 1.3.5
    - seaborn: 0.11.2
    - matplotlib: 3.2.2
    - sklearn: 1.0.2

<br/>

### 라이브러리 및 데이터 불러오기

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/wine.csv'
data = pd.read_csv(file_url)
```

<br/>

### 데이터 확인하기

 - `데이터 확인`
    - 독립 변수(12개)
        - alcohol: 알코올(도수)
        - malic_acid: 알산(사과산)
        - ash: 증발/소각 후 남은 무기물
        - alcalinity_of_ash: 남은 무기물의 알칼리성
        - magnesium: 마그네슘
        - total_phenols: 전체 페놀
        - flavanoids: 폴라보노이드(색소)
        - nonflavanoid_phenols: 비색소 페놀
        - proanthocyanins: 프로안토시아닌
        - color_intensity: 색상 강도
        - hue: 색조
        - od280/od315_of_diluted_wines: 희석된 와인의 단백질 함량
        - proline: 프롤린
    - 종속 변수(1개)
        - class: 와인 등급
    - 해석
        - 전체 데이터 길이는 178로 상당히 작다.
        - Non-Null Count 값이 다른 변수가 있다.
            - alcohol은 178이 아닌 176으로 2개의 결측치가 있다.
            - nonflavanoid_phenols는 173이므로 5개의 결측치가 있다.
        - 통계를 확인하면, 몇몇 변수에서 75%와 max 값의 차이가 유독 두드러진 경우가 있다. 이러한 아웃라이어는 경우에 따라 모델링에 영향을 미칠 수 있다.
```python
data.head()
data.info()
data.describe() # 통계 정보 출력
```

<br/>

### 목표값에서 고윳값 확인하기

연속형 변수인지, 0과 1로 이루어진 이진 변수인지, 아니면 3개 이상으로 된 범주형 변수인지 등 목표값의 특성에 따라 적합한 알고리즘이 다르다.  
연속형 변수는 head() 함수로 출력해 한눈에 파악이 가능하지만, 새로운 데이터를 다루고 있고, 목표 변수가 어떤 값들로 구성되어 있는지 알지 못하는 경우에는 unique() 함수로 고유값을 얻을 수 있다.  

```python
data['class'].unique() # 목표 변수의 고유값 출력
data['class'].nunique() # 고유값 갯수 출력
data['class'].value_counts() # 각 고유값에 해당하는 갯수 출력

sns.barplot(x = data['class'].value_counts().index, y = data['class'].value_counts()) # 막대 그래프 생성 및 출력
sns.countplot(data['class'])
```

<br/>

### 전처리: 결측치 처리하기

info()와 describe() 함수를 호출해 일부 변수에 결측치가 있다는 것을 확인하였다.  
그 외에도 isna() 함수로 직접적으로 결측치 유무를 확인할 수 있다.  

 - `결측치 처리`
    - 결측치 행 제거를 원하는 경우 dropna() 함수를 이용할 수 있다.
    - 결측 변수 자체를 제거하기 위해서는 drop() 함수를 이용할 수 있다.
    - 결측치에 값을 채워넣기 위해서는 fillna() 함수를 이용할 수 있다.
```python
# 결측치 확인
data.isna() # 결측치 확인
data.isna().sum() # 결측치 갯수
data.isna().mean() # 결측치 비율


# 결측치 처리
data.dropna() # 결측치 제거
data.dropna(subset=['alcohol']) # 지정된 변수의 결측치 행만 제거

data.drop(['alcohol', 'nonflavanoid_phenols'], axis=1) # 해당 컬럼을 제거

data.fillna(-99) # -99로 결측치 채워넣기
data.fillna(data.mean()) # 평균값으로 결측치 채워넣기
```

<br/>

 - `결측치 처리 방식 선택하기`
    - 평균 등을 이용하여 결측치를 채우면, 아무리 비슷한 값을 채운다고 해도 실제값과 일치할 가능성이 매우 낮기 때문에 오히려 오차의 원인이 될 수 있다. (데이터에 노이즈가 더해진 효과)
    - dropna()로 결측치 행 제거 방법은 경우에 따라서 너무 과도하게 많은 데이터가 삭제될 수도 있다.
    - 예제에서는 전체 178개 데이터밖에 없으므로 7개의 결측치 행도 아쉬운 상황이다. 때문에, 평균값 등으로 결측치를 채워주는 방식을 이용한다.
```python
data.fillna(data.median(), inplace = True)
data.isna().mean() # 결측치 확인
```

<br/>

### 스케일링

스케일링은 데이터의 스케일을 맞추는 작업이다.  
쉽게, 각 컬럼들마다 값들의 범위가 너무나도 다를 때 스케일링을 할 수 있다.  
K-최근접 이웃은 거리 기반의 알고리즘으로 스케일 문제가 안 좋은 결과를 초래할 수 있다.  
예를 들어, 알코올은 11.03 ~ 14.75 값의 범위에 해당하고, 마그네슘은 70 ~ 162 값의 범위에 해당한다.  
이때, 스케일링으로 인위적으로 각 컬럼이 비슷한 범위를 가지도록 만드는 작업이다.  
 - 표준화 스케일링: 평균이 0이 되고, 표준편차가 1이 되도록 데이터를 고르게 분포시키는데 사용
 - 로버스트 스케일링: 데이터에 아웃라이어가 존재하고, 그 영향력을 그대로 유지하고 싶을 떄 사용
 - 최소-최대 스케일링: 데이터 분포의 특성을 최대한 그대로 유지하고 싶을 때 사용
 - 정규화 스케일링: 행 기준의 스케일링이 필요할 때 사용하나, 실제로 거의 사용하지 않음
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
```

<br/>

 - `표준화 스케일링`
    - 표준화 스케일링은 데이터를 표준화된 정규분포로 만들어주는 방법이다. 모든 컬럼에서 평균과 표준편차가 각각 0과 1이 되며, min과 max 값은 컬럼마다 각기 다르지만, 차이를 줄여 데이터가 더 동등한 수준에서 연산되도록 할 수 있다.
    - 스케일링도 모델링 코드와 비슷한 방식으로 사용할 수 있다.
    - fit() 함수로 데이터를 학습시킨다. 이 단계에서 스케일링에 필요한 정보(평균, 표준편차)가 학습된다.
    - 학습이 되었으면, transform()으로 연산을 해준다. 이 단계에서 학습에서 얻은 정보로 계산하게 된다.
```python
# 표준화 스케일링
st_scaler = StandardScaler()
st_scaler.fit(data)
st_scaled = st_scaler.transform(data)

# 사람이 보기 좋은 형태로 변환
pd.DataFrame(st_scaled)
st_scaled = pd.DataFrame(st_scaled, columns = data.columns)

round(st_scaled.describe(), 2)
```

<br/>

 - `로버스트 스케일링`
    - 로버스트 스케일링은 평균과표준편차 대신 사분위값을 이용하여 계산된다.
```python
rb_scaler = RobustScaler()
rb_scaled = rb_scaler.fit_transform(data)
rb_scaled = pd.DataFrame(rb_scaled, columns = data.columns)
round(rb_scaled.describe(), 2)
```

<br/>

 - `최소-최대 스케일링`
    - 최소-최대 스케일링의 특징은 모든 컬럼에서 최댓값이 1, 최솟값이 0인 형태로 변환된다는 것이다.
    - 각 값에서 최솟값을 빼주고, 최댓값과 최솟값의 차이만큼으로 나누어주면 최소-최대 스케일링 결괏값이 나온다.
```python
mm_scaler = MinMaxScaler()
mm_scaled = mm_scaler.fit_transform(data)
mm_scaled = pd.DataFrame(mm_scaled, columns = data.columns)
round(mm_scaled.describe(), 2)
```

<br/>

 - `스케일링 방식 선택하기`
    - 우선 아웃라이어의 유무에 따라 판단하는데, 아웃라이어의 영향이 큰 데이터이고 이를 피하고 싶다면 로버스트 스케일링이 적합하다.
        - 표준화 스케일링은 평균과 표준편차를 이용하고 최소-최대 스케일링은 최대/최솟값을 이용하여, 이들 모두 아웃라이어가 있을 떄 민감하게 반응한다.
    - 떄에 따라서 데이터의 기준 분포를 최대한 유지하여 스케일링하는 게 필요할 수 있다. 이러한 경우 최소-최대 스케일링이 적합하다.
        - 표준화 스케일링은 모든 데이터를 표준정규분포 형태, 즉 좌우 대칭의 종 모양으로 변경하여, 여기에 적용하면 아웃라이어의 영향을 받으면서도 기존의 데이터 분포에 대한 특징을 상실하게 된다.
        - 반면 최소-최대 스케일링은 최댓값 1과 최솟값 0의 범위에서 기존 데이터의 분포를 최대한 그대로 옮겨담아 낸다.
    - 표준화 스케일링은 기존 데이터가 정규분포를 따르고 있고 아웃라이어가 없는 상황에서 무난하게 사용된다.
```
★ 스케일링별 특징
 - 표준화 스케일링
데이터에 아웃라이어가 존재할 때 아웃라이어의 영향을 받는다.
평균 0, 분산 1이 되게끔 분포시키기 때문에,
데이터의 기존 분포 형태가 사라지고 정규분포를 따르는 결과물을 가져온다.

 - 로버스트 스케일링
데이터에 아웃라이어가 존재할 때 아웃라이어의 영향을 받지 않는다.
변화된 데이터의 범위는 표준화 스케일링이나 최소-최대 스케일링보다 넓게 나타난다.

 - 최소-최대 스케일링
데이터에 아웃라이어가 존재할 때 아웃라이어의 영향을 받는다.
두 스케일러와 비교했을 때 데이터의 기존 분포를 가장 있는 그대로 담아내며 스케일만 변화시킨다.
데이터의 범위는 0~1로 나타난다.
```

<br/>

 - `스케일링 주의사항`
    - 스케일링 대상에서 종속변수를 제외해야 한다.
        - class라는 컬럼을 예측해야 하기 때문에 이 변수는 그대로 남겨두어야 한다.
    - 스케일링 전에 훈련셋과 시험셋을 나누어야 한다.
        - 훈련셋에서 fit()으로 스케일링을 위한 값을 학습시키고, 이 값을 활용하여 훈련셋과 시험셋을 변환해야 한다.
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(data.drop('class', axis=1), data['class'], test_size=0.2, random_state=100)

mm_scaler = MinMaxScaler() # 최대-최소 스케일러 객체 생성
mm_scaler.fit(X_train) # 학습
X_train_scaled = mm_scaler.transform(X_train) # 학습셋 트랜스폼
X_test_scaled = mm_scaler.transform(X_test) # 시험셋 트랜슬폼

```

<br/>

### 모델링 및 예측/평가하기

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

knn = KNeighborsClassifier()
knn.fit(X_train_scaled, y_train)
pred = knn.predict(X_test_scaled)
accuracy_score(y_test, pred) # 정확도 확인 (0.88)
```

<br/>

### 하이퍼파라미터 튜닝하기

KNN 알고리즘에는 n_neighbors라는 아주 중요한 매개변수가 하나 있다.  
해당 변수는 예측에 가까운 이웃을 몇 개나 고려할지를 정한다.  
KNeighborsClassifier() 함수에 별도로 지정하지 않으면 5가 들어간다.

 - `하이퍼파라미터 튜닝`
    - n_neighbors: 예측에 참고할 이웃 수
    - weights: 예측에 사용되는 가중치 함수 (uniform, distance, 사용자 정의 함수)
    - metric: 거리 측정 기준
    - n_jobs: 실행할 병렬 작업수
```python
knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(X_train_scaled, y_train)
pred = knn.predict(X_test_scaled)
accuracy_score(y_test, pred) # 정확도 확인 (0.91)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_scaled, y_train)
pred = knn.predict(X_test_scaled)
accuracy_score(y_test, pred) # 정확도 확인 (0.88)

# 반복 확인
scores = []
for i in range(1, 21)
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train_scaled, y_train)
    pred = knn.predict(X_test_scaled)
    acc = accuracy_score(y_test, pred) # 정확도 계산
    scores.append(acc) # 정확도 저장

# 그래프로 출력
sns.lineplot(x=range(1, 21), y=scores) # 13이 합리적
```

<br/>

### 이해하기: K-최근접 이웃

KNN 알고리즘은 새로운 데이터를 예측할 때, 거리를 기반으로 하여 인접한 데이터와 같은 종류로 분류해내는 기법이다.

 - 동점일 떄 처리
    - 2개 이웃을 고려할 때 세모와 원이 1개씩으로 동점일 때 최종 예측값은 랜덤으로 결정된다. 동점 상황에서 랜덤으로 결정되어도 대세에는 큰 지장이 없는 경우가 대부분이지만, 해결 방안이 몇 가지 있다.
    - 첫 번쨰, 고려할 이웃의 수를 항상 홀수로 유지한다.
    - 두 번째, 가중치를 준다. KNN에 weights 라는 매개변수를 이용하여 동점일 때 그 거리가 더 가까운쪽으로 결정하도록 설정할 수 있다.

<br/>

### 학습 마무리

```python
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 라이브러리 및 데이터 불러오기
file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/wine.csv'
data = pd.read_csv(file_url)


# 데이터 확인
data.head()
data.info()
data.describe() # 통계 정보 출력


# 목표값에 고유값 확인
data['class'].unique() # 목표 변수의 고유값 출력
data['class'].nunique() # 고유값 갯수 출력
data['class'].value_counts() # 각 고유값에 해당하는 갯수 출력

sns.barplot(x = data['class'].value_counts().index, y = data['class'].value_counts()) # 막대 그래프 생성 및 출력
sns.countplot(data['class'])


# 결측치 처리
data.fillna(data.median(), inplace = True)
data.isna().mean() # 결측치 확인


# 스케일링
X_train, X_test, y_train, y_test = train_test_split(data.drop('class', axis=1), data['class'], test_size=0.2, random_state=100)
mm_scaler = MinMaxScaler() # 최대-최소 스케일러 객체 생성
mm_scaler.fit(X_train) # 학습
X_train_scaled = mm_scaler.transform(X_train) # 학습셋 트랜스폼
X_test_scaled = mm_scaler.transform(X_test) # 시험셋 트랜슬폼


# 모델링 및 예측하기
knn = KNeighborsClassifier(n_neighbors=13)
knn.fit(X_train_scaled, y_train)
pred = knn.predict(X_test_scaled)
accuracy_score(y_test, pred) # 정확도 확인 (0.97)
```

<br/>

 - `핵심 용어`
    - K-최근접 이웃: 거리 기반으로 데이터를 분류하는 알고리즘
    - 아웃라이어: 평균치에서 크게 벗어나는 데이터
    - 스케일링: 독립변수의 범위를 동일한 수준으로 만드는 데 사용하는 방법
        - 표준화 스케일링: 평균이 0이 되고, 표준편차가 1이 되도록 데이터를 고르게 분포시키는데 사용
        - 로버스트 스케일링: 데이터에 아웃라이어가 존재하고, 그 영향력을 그대로 유지하고 싶을 때 사용
        - 최소-최대 스케일링: 데이터 분포의 특성을 최대한 그대로 유지하고 싶을 때 사용
        - 정규화 스케일링: 행 기준의 스케일링이 필요할 때 사용하나, 실제로 거의 사용하지 않음
    - 결측치: 데이터가 비어있는 값으로, Null, NaN, NA 등으로 표현

