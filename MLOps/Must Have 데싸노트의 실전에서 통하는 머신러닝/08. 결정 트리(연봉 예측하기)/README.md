# 08장. 결정 트리: 연봉 예측하기

## 결정 트리

결정 트리는 관측값과 목표값을 연결시켜주는 예측 모델로 나무 모양으로 데이터를 분류하며, 수많은 트리 기반 모델의 기본 모델이 되는 중요 모델이다.  
트리 기반의 모델은 선형 모델과는 전혀 다른 특징을 가지는데, 선형 모델이 각 변수에 대한 기울기값들을 최적화하여 모델을 만들어나갔다면, 트리 모델에서는 각 변수의 특정 지점을 기준으로 데이터를 분류해가며 예측 모델을 만든다.  
예를 들어, 남자/여자로 나눠 각 목표값 평균치를 나누거나, 나이를 30세 이상/미만인 두 부류로 나누어 평균치를 계산하는 방식으로 데이터를 무수하게 쪼개어 나가고, 각 그룹에 대한 예측치를 만들어낸다.  
 
 - 장점
    - 데이터에 대한 가정이 없는 모델이다.
    - 아웃라이어에 영향을 거의 받지 않는다.
    - 트리 그래프를 통해서 직관적으로 이해하고 설명할 수 있다. 시각화에 굉장히 탁월하다.
 - 단점
    - 트리가 무한정 깊어지면 오버피팅 문제를 야기할 수 있다.
    - 발전된 트리 기반 모델들에 비하면 예측력이 상당히 떨어진다.
 - 사용처
    - 종속 변수가 연속형 데이터와 범주형 데이터 모두에 사용할 수 있다.
    - 모델링 결과를 시각화할 목적으로 가장 유용하다.
    - 아웃라이어가 문제될 정도로 많을 떄 선형 모델보다 좋은 대안이 될 수 있다.

<br/>

### 문제 정의

나이, 교육 수준, 혼인 상태, 직업, 인종 성별 등 항목에 따른 연봉 데이터셋을 통해 결정 트리 알고리즘을 활용해 연봉 등급을 나눈다.  

 - 미션: 연봉 데이터셋을 이용해 연봉을 예측
 - 알고리즘: 결정 트리
 - 데이터셋: 종속 변수는 class, 독립 변수는 학력, 교육 연수, 혼인 상태, 직업 등이 있다.
 - 문제 유형: 분류
 - 평가지표: 정확도
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
        - age: 연령
        - workclass: 고용 형태
        - education-num: 교육 연수
        - marital-status: 혼인 상태
        - occupation: 직업
        - relationship: 가족 관계
        - race: 인종
        - sex: 성별
        - capital-gain: 자산 증가
        - capital-loss: 자산 감소
        - hours-per-week: 주당 노동 시간
        - native-country: 본국
    - 종속 변수(1개)
        - class: 연봉 구분 (50K 이하와 50K 초과 두 가지만 존재)
        
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/salary.csv'
data = pd.read_csv(file_url)

data.head()
data['class'].unique() # 목표 변수의 고윳값 확인
data.info() # 변수 특징 출력
data.describe() # 통계 정보 출력
```

<br/>

### 전처리: 범주형 데이터

가장 먼저 처리할 변수는 종속 변수인 class이다.  
차후 해석에 혼선이 없도록 50K 이하를 0, 초과를 1로 변경한다.  

이후에 독립변수의 범주형 데이터를 다룬다.  
처음으로, 어떤 변수가 object 형인지 확인하고 처리한다.


```python
# 1. 종속 변수 class 전처리
data['class'] = data['class'].map({'<=50K': 0, '>50K': 1})

# 2. 독립 변수 전처리
for i in data.columns:
    print(i, data[i].dtype) # 컬럼명과 데이터 타입 출력

obj_list = []
for i in data.columns:
    if data[i].dtype == 'object':
        obj_list.append(i)

# 전처리할 변수 선별하기
for i in obj_list:
    print(i, data[i].nunique()) # 변수 이름과 고유값 개수 확인

for i in obj_list:
    if data[i].nunique() >= 10: # 변수의 고유값이 10보다 크거나 같으면
        print(i, data[i].nunique()) # education, occupation, native-countrty

# education 변수 처리 -> education과 education-num 숫자와 매핑되어 있다.
data['education'].value_counts() # 고유값 출현 빈도 확인

for i in np.sort(data['education-num'].unique()):
    print(i, data[data['education-num'] == i]['education'].unique())

data.drop('education', axis=1, inplace=True) # education 제거

# occupation 변수 처리 -> 이미 비슷한 직업군끼리 묶인 상태, 직업 간의 서열은 없음, 더미 변수로 처리
data['occupation'].value_counts() # 고유값 출현 빈도 확인

# native-country 변수 처리
data['native-country'].value_counts() # 고유값 출현 빈도 확인

data.groupby('native-country').mean().sort_values('class') # 그룹별 평균 계산 후 class 기준으로 오름차순 정렬
country_group = data.groupby('native-country').mean()['class']
country_group = country_group.reset_index()
data = data.merge(country_group, on = 'native-country', how='left')

data.drop('native-country', axis=1, inplace=True)
data = data.rename(columns = {'class_x', 'class', 'class_y', 'native-country'})
```

<br/>

## 전처리: 결측치 처리 및 더미 변수 변환

```python
# 결측치 비율 확인
data.isna().mean()

# 임의의 값(-99)으로 결측치 채우기 (선형 모델에서는 데이터 왜곡을 불러올 수 있으니 주의)
data['native-country'] = data['native-country'].fillna(-99)

# workclass와 occupation 변수는 모두 범주형 변수로 평균치로 해결할 수 없다.
# 특정 텍스트를 채워주거나, dropna()로 해당 라인을 제거한다.
data['workclass'].value_counts() # 고유값별 출현 빈도 확인

# Private 비율이 압도적으로 해당 값으로 결측치를 채우기
data['workclass'] = data['workclass'].fillna('Private')

data['occupation'].value_counts() # 고유값별 출현 빈도 확인

# 특정 값이 압도적으로 많지 않아, 'Unknown' 텍스트로 결측치 채우기
data['occupation'] = data['occupation'].fillna('Unknown')

# 범주형 데이터를 더미 변수로 변환
data = pd.get_dummies(data, drop_first=True)
```

<br/>

### 모델링 및 예측/평가하기

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

x = data.drop('class', axis=1)
y = data['class']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.4, random_state = 100)

model = DecisionTreeClassifier() # 모델 객체 생성
model.fit(X_train, y_train)      # 학습
pred = model.predict(X_test)     # 예측

accuracy_score(y_test, pred)     # 정확도 계산: 0.81
```

<br/>

### 이해하기: 결정 트리

결정 트리는 특정 변수에 대한 특정 기준값으로 데이터를 계속 분류해가면서 유사한 그룹으로 묶어내어 예측값을 만드는 알고리즘이다.  

 - 분류 결정 트리
    - 주어진 입력 데이터를 여러 클래스 중 하나로 분류하는 것
    - 데이터의 특성(feature)을 기반으로 트리 형태의 구조를 만듭니다.
    - 각 노드(node)는 특정 특성(feature)에 대한 조건을 나타내며, 각 가지(branch)는 가능한 결과 클래스를 나타냅니다.
    - 트리의 맨 위에서부터 각 노드를 따라가며 조건을 만족하는 가지를 따라가면서 최종적으로 예측 클래스를 결정합니다.
 - 회귀 결정 트리
    - 주어진 입력 데이터에 대해 연속적인 출력 값을 예측하는 것
    - 분류 결정 트리와 유사하지만, 각 리프 노드(말단 노드)에서는 클래스가 아닌 실수값을 예측합니다.
    - 각 노드에서는 특정 특성(feature)과 그에 대한 분할 조건을 사용하여 데이터를 분리합니다.
    - 리프 노드에 도달하면 해당 리프 노드의 평균값 또는 가중 평균값을 사용하여 예측값을 계산합니다.

<br/>

### 매개변수 튜닝

결정 트리에서는 트리 깊이가 깊어질수록, 수없이 많은 노드를 분류하여 모델을 만들수록 오버피팅 발생 가능성이 높다.  
이 문제를 해결할 목적으로 결정 트리에서는 트리의 깊이를 제한하는 매개변수를 제공한다.  
기본값은 None으로 매개변수를 지정하지 않으면 최대한 깊은 수준으로 트리를 만들어낸다.  

```python
# None: 학습 점수: 0.97, 테스트 점수: 0.81
model = DecisionTreeClassifier()    # 모델 객체 생성
model.fit(X_train, y_train)         # 학습
train_pred = model.predict(X_train) # 훈련셋 예측
pred = model.predict(X_test)        # 예측
print('Train score:', accuracy_score(y_train, train_pred), 'Test score:', accuracy_score(y_test, pred)) # 훈련셋, 시험셋 정확도 평가

# 트리의 깊이 지정: 학습 점수: 0.85, 테스트 점수: 0.84
model = DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)
train_pred = model.predict(X_train)
pred = model.predict(X_test)
print('Train score:', accuracy_score(y_train, train_pred), 'Test score:', accuracy_score(y_test, pred))

# 트리의 깊이 지정: 학습 점수: 0.85, 테스트 점수: 0.85
model = DecisionTreeClassifier(max_depth=7)
model.fit(X_train, y_train)
train_pred = model.predict(X_train)
pred = model.predict(X_test)
print('Train score:', accuracy_score(y_train, train_pred), 'Test score:', accuracy_score(y_test, pred))
```

<br/>

### 트리 그래프

```python
from sklearn.tree import plot_tree
plt.figure(figsize=(30, 15))
plot_tree(model) # 트리 그래프 출력
plt.show()

# 크기 조절
plt.figure(figsize=(30, 15))
plot_tree(model, max_depth=3, fontsize=15) # 트리 그래프 출력
plt.show()

# 원래 변수 이름 지정
plt.figure(figsize=(30, 15))
plot_tree(model, max_depth=3, fontsize=15, feature_names=X_train.columns) # 변수 이름을 추가하여 그래프 출력
plt.show()
```


### 학습 마무리

<br/>

 - `핵심 용어`
    - 결정 트리: 트리 모델의 가장 기본 형태로 데이터의 특성을 고려하여 데이터를 분류해나가는 방식이다.
    - 지니 인덱스와 교체 엔트로피: 노드의 순도를 평가하는 방법. 노드의 순도가 높을수록 지니 및 엔트로피 값은 낮아진다.
    - 오버피팅: 모델이 학습셋에 지나치게 잘 맞도록 학습되어서 새로운 데이터에 대한 예측력이 떨어지는 현상
    - 언더피팅: 과소적합이라고도 하며, 모델이 충분히 학습되지 않아 훈련셋에 대해서도 좋은 예측력을 내지 못하는 상황

