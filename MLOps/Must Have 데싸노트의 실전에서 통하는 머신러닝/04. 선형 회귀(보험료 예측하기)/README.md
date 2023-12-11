# 04장. 선형 회귀: 보험료 예측하기

## 선형 회귀

선형 회귀는 가장 치고적인 머신러닝 모델로 여러 가지 데이터를 활용하여 연속형 변수인 목표 변수를 예측해 내는 것이 목적이다.  
선형 회귀 모델에서는 예측할 종속변수만 연속형 변수면 족하다.  

복잡한 알고리즘에 비해서 예측력이 떨어지지만 데이터의 특성이 복잡하지 않을 때 쉽고 빠른 예측이 가능하여 많이 사용된다.  
또, 다른 모델과의 성능을 비교하는 베이스라인으로 사용하기도 한다.  
 - 장점
    - 모델이 간단하기 때문에 구현과 해석이 쉽다.
    - 같은 이유로 모델링하는 데 오랜 시간이 걸리지 않는다.
 - 단점
    - 최신 알고리즘에 비해 예측력이 떨어진다.
    - 독립변수와 예측변수의 선형 관계를 전제로 하기 대문에, 이러한 전제에서 벗어나는 데이터에서는 좋은 예측을 보여주기 어렵다.
 - 사용처
    - 연속된 변수를 예측하는 데 사용된다.
    - 예를 들어, BMI, 매출액, 전력 사용량 등

 - `학습 순서`
```
1. 문제 정의
2. 라이브러리 및 데이터 불러오기
3. 데이터 확인하기
4. 전처리: 학습셋과 실험셋 나누기
5. 데이터 모델링
6. 모델을 활용해 예측하기
7. 예측 모델 평가하기
8. 이해하기: 선형회귀
```

<br/>

### 문제 정의

연령, 성별, BMI 등의 정보를 활용하여 보험료를 예측한다.  

 - 미션: 보험 데이터셋을 이용하여 보험사에서 청구할 보험료 예측
 - 알고리즘: 선형 회귀
 - 데이터셋: 보험과 관련된 데이터로 보험사에서 청구하는 병원 비용이 종속변수이며, 나이, 성별, BMI, 자녀 수, 흡연 여부를 독립변수로 사용한다.
 - 문제 유형: 회귀
 - 평가지표: RMSE(평균 제곱근 편차)
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

file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/insurance.csv'
data = pd.read_csv(file_url)
```

<br/>

### 데이터 확인하기

불러온 데이터를 확인한다.  

 - `데이터 확인`
```python
print(data)
data.head() # 상위 5줄 출력
data.info() # 컬럼 정보 출력
round(data.describe(), 2) # 소수점 2째자리까지만 표시해 통계 정보 출력
```

<br/>

### 전처리: 학습셋과 시험셋 나누기

데이터를 나누는 작업은 크게 2가지 차원으로 진행된다.  
첫번째는 종속변수와 독립변수 분리이다.  
두번째는 학습용 데이터셋인 학습셋과 평가용 시험셋을 나누는 작업이다.  

학습 데이터셋을 통해 모델링(학습)을 하고, 시험 데이터셋을 통해 만들어진 모델에 대해서 예측이 잘 되었는지 평가하도록 한다.  
즉, 모델에 대해서 검증하기 위한 데이터로 학습셋과 시험셋을 나눈다.  

일반적으로 학습셋과 시험셋의 비율은 7:3 혹은 8:2 정도 비율로 나눈다.  
데이터의 크기가 작다면, 학습셋의 비율을 높여서 최대한 학습셋을 많이 확보해야 한다.  

관례로 독립변수를 X, 종속변수를 y로 나눈다.  
또한, X는 대문자, y는 소문자로 쓰는데 X는 변수가 여러 개 있는 데이터프레임으로 대문자로 사용하고, y는 변수가 하나인 시리즈이기 때문에 소문자로 사용한다.  

 - `학습셋과 시험셋 나누기`
    - 싸이킷런의 train_test_split 모듈을 이용하여 데이터셋을 나눌 수 있다.
    - random_state 옵션은 데이터를 랜덤하게 샘플링해주며, 다시 실행해도 일관성있는 샘플링을 지원해준다.
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=100)
```

<br/>

### 모델링

모델링은 머신러닝 알고리즘으로 모델을 학습시키는 과정이며, 그 결과물이 머신러닝 모델이 된다.  
싸이킷런에서 선형 회귀 알고리즘은 sklearn.linear_model에서 제공한다.  

 - `모델링`
    - model.fit(독립변수, 종속변수)
    - 데이터 모델 안에
```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
```

<br/>

### 모델을 활용해 예측하기

model.predict() 함수로 테스트 데이터셋을 넣어주면 예측 결과가 반환된다.  

 - `예측하기`
```python
pred = model.predict(X_test)
```

<br/>

### 예측 모델 평가하기

모델을 평가하는 방법으로 '테이블로 평가하기', '그래프로 평가하기', '통계적인 방법으로 평가하기' 등이 있다.  

 - `테이블로 평가하기`
    - 예측한 값은 pred에 저장되어 있고, 실제 정보는 y_test에 저장되어 있다.
    - 예측값이 얼마나 정확한지는 pred와 y_test를 비교하는 것으로 확인할 수 있다.
```
comparison = pd.DataFrame({'actual': y_test, 'pred': pred})
comparison
```

<br/>

 - `그래프로 평가하기`
    - 테이블로 수많은 데이터를 눈으로 확인하기는 어려움이 있다. 때문에, 그래프를 통해 시각화하여 한눈에 파악한다.
    - 먼저, 그래프 크기를 정하고 scatterplot() 함수를 이용하여 산점도 그래프를 만든다.
    - 선에 가까울수록 잘 된 예측이고, 선을 기준으로 위에 있으면 예측값이 높게 나타난 것이고, 선을 기준으로 아래에 있으면 예측값이 낮게 나타난 것이다.
```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 10)) # 그래프 크기 정의
sns.scatterplot(x = 'actual', y = 'pred', data = comparison)
```

<br/>

 - `통계적인 방법으로 평가하기: RMSE`
    - 연속형 변수를 예측하고 평가할 때 RMSE(평균 제곱근 편차)를 이용해 평가하는 방법이 많이 사용된다.
    - RMSE는 실제값과 예측값 사이의 오차를 각각 합산하는 개념이다.
        - MAE: 평균 절대 오차. 실제값과 예측값 사이의 오차에 절대값을 씌운 뒤 이에 대한 평균을 계산
        - MSE: 평균 제곱 오차. 실제값과 예측값 사이의 오차를 제곱한 뒤 이에 대한 평균을 계산
        - RMSE: 루트 평균 제곱 오차. MSE에 루트를 씌운 값으로 가장 일반적으로 사용됨
```python
from sklearn.metrics import mean_squared_error
mean_squared_error(y_test, pred) ** 0.5 # RMSE 계산 실행
mean_squared_error(y_test, pred, squared = False)

model.score(X_train, y_train)
```

<br/>

### 이해하기: 선형 회귀

선형 회귀는 독립변수와 종속변수 간에 선형 관계가 있음을 가정하여 최적의 선을 그려서 예측하는 방법이다.  
머신러닝에서는 손실 함수를 최소화하는 선을 찾아서 모델을 만들어낸다.  
여기서 손실 함수란 예측값과 실제값의 차이, 즉 오차를 평가하는 방법을 말한다.  

<br/>

### 학습 마무리

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 라이브러리 및 데이터 불러오기
file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/insurance.csv'
data = pd.read_csv(file_url)

# 데이터 확인
print(data)
data.head() # 상위 5줄 출력
data.info() # 컬럼 정보 출력
round(data.describe(), 2) # 소수점 2째자리까지만 표시해 통계 정보 출력

# 데이터 전처리: 학습셋과 시험셋 나누기
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=100)

# 모델링
model = LinearRegression()
model.fit(X_train, y_train)

# 예측하기
pred = model.predict(X_test)

# 예측 모델 평가하기
comparison = pd.DataFrame({'actual': y_test, 'pred': pred}) # 테이블로 평가

plt.figure(figsize=(10, 10)) # 그래프 크기 정의
sns.scatterplot(x = 'actual', y = 'pred', data = comparison) # 그래프로 평가

mean_squared_error(y_test, pred) ** 0.5 # RMSE 계산 실행
mean_squared_error(y_test, pred, squared = False)

model.score(X_train, y_train)

```
