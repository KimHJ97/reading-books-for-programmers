# 05장. 로지스틱 회귀: 타이타닉 생존자 예측하기

## 로지스틱 회귀

로지스틱 회귀 분석은 알고리즘의 근간을 선형 회귀 분석에 두고 있어 선형 회귀 분석과 상당히 유사하지만 다루는 문제가 다르다.  
선형 회귀 분석은 연속된 변수를 예측하는 반면, 로지스틱 회귀 분석은 Yes/No 처럼 두 가지로 나뉘는 분류 문제를 다룬다.  

실제 이진분류가 필요한 상황이 많아 두 가지 범주를 구분하는 간단한 예측에 유용하며 딥러닝에서도 기본 지식이다.  
 
 - 장점
    - 선형 회귀 분석만큼 구현하기 용이하다.
    - 계수(기울기)를 사용해 각 변수의 중요성을 쉽게 파악할 수 있다.
 - 단점
    - 선형 회귀 분석을 근간으로 하고 있어 선형 관계가 아닌 데이터에 대한 예측력이 떨어진다.
 - 사용처
    - Yes/No, True/False와 같은 두 가지 범주로 나뉜 값을 예측하는 데 사용
    - 분류 문제에 있어서 기준선으로 자주 활용된다.

 - `학습 순서`
```
1. 문제 정의
2. 라이브러리 및 데이터 불러오기
3. 데이터 확인하기
4. 전처리: 범주 변수 변환하기(더미변수와 원-핫 인코딩)
5. 모델링 및 예측하기
6. 예측 모델 평가하기
7. 이해하기
```

<br/>

### 문제 정의

이름, 성별, 나이, 티켓 번호 등 같은 정보가 실제로 생존에 어떤 영향을 미치는지 확인한다.  

 - 미션: 타이타닉 승객 정보 데이터셋을 이용해 생존 여부 예측
 - 알고리즘: 로지스틱 회귀
 - 데이터셋: 타이타닉에 승객의 정보를 담은 데이터셋. 각 승객 정보(이름, 성별, 나이, 티켓 번호 등)를 활용하여 생존 여부를 예측
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

판다스로 URL을 통해 csv 파일의 데이터를 로드한다.

 - `CSV 데이터 로드`
```python
import pandas as pd

file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/titanic.csv'
data = pd.read_csv(file_url)
```

<br/>

### 데이터 확인하기

불러온 데이터를 확인한다.  

 - `데이터 확인`
    - 독립 변수(8개)
        - Pclass: 티켓 클래스
        - Name: 승객 이름
        - Sex: 성별
        - Age: 나이
        - SibSp: 함께 탑승한 형제 및 배우자의 수
        - Parch: 함께 탑승한 부모 및 자녀의 수
        - Ticket: 티켓 번호
        - Embarked: 승선한 항구(C:Cherbourg, Q:Queenstown, S:Southampton)
    - 종속 변수(1개)
        - Survived: 생존 유무(1:생존, 0:사망)
```python
import matplotlib.pyplot as plt
import seaborn as sns

data.head() # 상위 5줄 출력
data.info() # 컬럼 정보 출력
data.describe() # 통계 정보 출력
data.corr() # 상관 관계 출력

# 상관 관계를 그래프로 확인
sns.heatmap(data.corr())
plt.show() # 그래프 출력

sns.heatmap(data.corr(), cmap='coolwarm') # 히트맵 생성
plt.show() # 그래프 출력

sns.heatmap(data.corr(), cmap='coolwarm', vmin=-1, vmax=1) # -1 ~ 1 범위 조정
sns.heatmap(data.corr(), cmap='coolwarm', vmin=-1, vmax=1, annot=True) # 수치 값 출력
```

<br/>

### 전처리: 범주형 변수 변환하기(더미 변수와 원-핫 인코딩)

타이타닉 데이터셋에는 자료형이 object인 변수(문자)가 4개가 있다.  
기본적으로 머신러닝 알고리즘에서는 문자열로 된 데이터를 이해하지 못한다. 대부분 object 형을 처리해주는 알고리즘은 내부적으로 object 컬럼들을 숫자 데이터로 변환하는 기능을 제공한다.  

 - `범주형 변수 변환하기`
    - nunique() 함수로 고유값 개수를 확인할 수 있다.
```python
data['Name'].nunique() # 889
data['Sex'].nunique() # 2
data['Ticket'].nunique() # 680
data['Embarked'].nunique() # 3

# Name과 Ticket을 데이터셋에서 제외
# 이름에 따라 사망 여부가 갈린다고 추론하기 어렵다.
# Ticket은 티켓 번호로 중요할 수도 있지만, Pclass(티켓 클래스)가 있어서 필요없다.
data = data.drop(['Name', 'Ticket'], axis=1)
data.head()

# 문자 형태의 변수들을 원-핫 인코딩
data = pd.get_dummies(data, columns = ['Sex', 'Embarked'], drop_first = True)
```

<br/>

### 모델링 및 예측하기


 - `모델링 및 예측하기`
    - model.fit(독립변수, 종속변수)
    - 데이터 모델 안에
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# 모델링 하기전에 독립변수와 종속변수, 훈련셋과 시험셋을 나눈다.
X = data.drop('Survived', axis = 1) # 데이터셋에서 종속변수 제거 후 저장
y = data['Survived'] # 데이터셋에서 종속변수만 저장
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 100) # 학습셋, 시험셋 분리

# 모델링 및 예측
model = LogisticRegression() # 로지스틱 회귀 모델 생성
model.fit(X_train, y_train) # 모델 학습

pred = model.predict(X_test) # 예측
```

<br/>

### 예측 모델 평가하기

model.predict() 함수로 테스트 데이터셋을 넣어주면 예측 결과가 반환된다.  

 - `예측하기`
```python
pred = model.predict(X_test)
```

<br/>

### 예측 모델 평가하기

이번 데이터 목표값은 0과 1로 나누어진 이진분류로 RMSE 평가는 적합하지 않다.  
다양한 이진분류 평가 지표로는 정확도, 오차 행렬, 정밀도, 재현율, F1 Score, 민감도, 특이도, AUC 등이 있다.  

 - `정확도`
    - 정확도는 예측값과 실제값을 비교하여 얼마나 맞추었는지를 확인한다.
    - 로지스틱 회귀 분석 모델 계수를 확인하면, Parch를 제외하고 모두 음수가 된다.
        - Pclass는 음의 계수를 가지고 있기 때문에 Pclass가 높을수록 생존 가능성이 낮다. Pclass는 낮은 숫자일수록 비행기의 퍼스트 클래스처럼 더 비싼 티켓이다.
        - Age는 낮을수록, 성별은 여성이 생존 가능성이 높다.
```python
from sklearn.metrics import accuracy_score

accuracy_score(y_test, pred) # 실제값과 예측값으로 정확도 계산

model.coef_ # 로지스틱 회귀 분석 모델의 계수 확인
pd.Series(model.coef_[0], index = X.columns)
```

<br/>

### 이해하기: 피처 엔지니어링

피처 엔지니어링이란 기존 데이터를 손보아 더 나은 변수를 만드는 기법이다. 더미 변수를 만드는 일도 일종의 피처 엔지니어링이다.  

피처 엔지니어링은 머신러닝에 있어서 매우 중요한 역할을 한다. 적합한 알고리즘을 선택하고 하이퍼파라미터를 튜닝하는 일도 중요하지만 좋은 피처를 하나 더 마련하는 일만큼 강력한 무기는 없다. 여기서 피처는 독립 변수의 다른 표현이다.  

선형 모델에서는 다중공선성 문제를 주의해야 한다. 다중공선성은 독립변수 사이에 상관관계가 높을 때 발생하는 문제이다.  
예를 들어, 두 독립변수 A, B는 모두 목표 변수를 양의 방향으로 이끄는 계수를 가지고 있을 때 A와 B의 상관관계가 매우 높다면 y가 증가한 이유가 A 때문인지 B 때문인지 명확하지 않다.  
다중공선성 문제는 상관관계가 높은 변수 중 하나를 제거하거나, 둘을 모두 포괄시키는 새로운 변수를 만들거나, PCA와 같은 방법으로 차원 축소를 수행해 해결할 수 있다.  

Parch와 SibSp가 그나마 강한 상관 관계를 보여 이 둘을 새로운 변수로 만든다.  

 - `피처 엔지니어링`
```python
data['family'] = data['SibSp'] + data['Parch'] # SibSp와 Parch 변수 합치기
data.drop(['SibSp', 'Parch'], axis=1, inplace=True) # SibSp와 Parch 변수 삭제
data.head() # 5행 출력

# 피처 엔지니어링된 데이터로 모델링부터 평가 다시 진행
X = data.drop('Survived', axis = 1)
y = data['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 100) # 학습셋, 시험셋 준비

model = LogisticRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)
accuracy_score(y_test, pred)
```

<br/>

### 이해하기: 로지스틱 회귀

0과 1로 구성된 이진분류 문제에 선형 회귀 분석이 아닌 로지스틱 회귀 분석을 사용하였다.  
만약, 선형 회귀 분석을 사용하였다면 예상하는 형태가 아니게 된다.  

전반적으로 독립변수 x가 클 수록 y값이 1일 확률이 높아지는 형태지만,  
x값이 특정 범위가 넘어서면 크게는 1 이상으로 넘어가고, 작게는 0 아래로 내려가서 마이너스의 값을 예측한다.  
목표값은 0과 1로 예측값이 그 사이에 있어야 한다.  

이진분류 문제에서 목표값은 0과 1이므로 예측값이 해당 범위 안에서 나오기를 바라며, 로지스틱 회귀 분석은 이러한 문제를 해결해준다.  
곡선을 그리면서 한없이 1과 0에 가까워지는 형태로 로지스틱 회귀 분석에서의 예측값은 절대 1과 0 사이를 벗어나지 않게 된다.  

<br/>

### 학습 마무리

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 라이브러리 및 데이터 불러오기
file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/titanic.csv'
data = pd.read_csv(file_url)

# 데이터 확인
data.head() # 상위 5줄 출력
data.info() # 컬럼 정보 출력
data.describe() # 통계 정보 출력
data.corr() # 상관 관계 출력

sns.heatmap(data.corr(), cmap='coolwarm', vmin=-1, vmax=1, annot=True) # 상관 관계 그래프로 출력

# 모델링 하기전에 독립변수와 종속변수, 훈련셋과 시험셋을 나눈다.
X = data.drop('Survived', axis = 1) # 데이터셋에서 종속변수 제거 후 저장
y = data['Survived'] # 데이터셋에서 종속변수만 저장
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 100) # 학습셋, 시험셋 분리

# 모델링 및 예측
model = LogisticRegression() # 로지스틱 회귀 모델 생성
model.fit(X_train, y_train) # 모델 학습

pred = model.predict(X_test) # 예측

# 예측 모델 평가하기
accuracy_score(y_test, pred) # 실제값과 예측값으로 정확도 계산

model.coef_ # 로지스틱 회귀 분석 모델의 계수 확인
pd.Series(model.coef_[0], index = X.columns)


# 피처 엔지니어링
data['family'] = data['SibSp'] + data['Parch'] # SibSp와 Parch 변수 합치기
data.drop(['SibSp', 'Parch'], axis=1, inplace=True) # SibSp와 Parch 변수 삭제

# 피처 엔지니어링된 데이터로 모델링부터 평가 다시 진행
X = data.drop('Survived', axis = 1)
y = data['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 100) # 학습셋, 시험셋 준비

model = LogisticRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)
accuracy_score(y_test, pred)
```

<br/>

 - `핵심 용어`
    - 로지스틱 회귀: 선형 회귀 분석을 기반으로 한 모델로 연속형 종속변수가 아닌 이진분류 문제를 위한 알고리즘
    - 피처 엔지니어링: 기존 변수에서 더 나은 변수를 도출해내는 작업
    - 상관 관계: 두 변수 간의 연관성을 나타내는 것으로, 상관 관계가 높으면 절댓값이 1에 가깝다.
    - PCA: 주성분 분석
    - 다중공선성 문제: 변수 간의 강한 상관관계가 있을 떄 발생하는 문제. 선형 모델은 독립변수 간의 독립성을 전제로 하기 때문에 다중공선성 문제를 해결해 주는 것이 좋다.
    - 더미 변수와 원-핫 인코딩: 범주 형태의 변수를 숫자로 표현하는 방법. 변수에 속해 잇는 고윳값에 대한 새로운 변수들을 만들어 1과 0으로 표현한다.
