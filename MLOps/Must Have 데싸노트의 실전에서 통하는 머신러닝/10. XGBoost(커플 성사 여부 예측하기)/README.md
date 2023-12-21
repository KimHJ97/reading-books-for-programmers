# 10장. XGBoost: 커플 성사 여부 예측하기

## XGBoost

랜덤 포레스트는 각 트리를 독립적으로 만드는 알고리즘이다. 반면 부스팅은 순차적으로 트리를 만들어 이전 트리로부터 더 나은 트리를 만들어내는 알고리즘이다.  
부스팅 알고리즘은 트리 모델을 기반으로 한 최신 알고리즘 중 하나로, 랜덤 포레스트보다 훨씬 빠른 속도와 더 좋은 예측 능력을 보여준다.  
대표적으로 XG부스트, 라이트GBM, 캣부스트 등이 있으며, XGBoost가 가장 먼저 개발되고, 가장 널리 활용된다.  

 
 - 장점
    - 예측 속도가 상당히 빠르며, 예측력 또한 좋다.
    - 변수 종류가 많고 데이터가 클수록 상대적으로 뛰어난 성능을 보여준다.
 - 단점
    - 복잡한 모델인 만큼, 해석에 어려움이 있다.
    - 더 나은 성능을 위한 하이퍼파라미터 튜닝이 까다롭다.
 - 사용처
    - 종속변수가 연속형 데이터인 경우든 범주형 데이터인 경우든 모두 사용할 수 있다.
    - 이미지나 자연어가 아닌 표로 정리된 데이터의 경우, 거의 모든 상황에 활용할 수 있다.

<br/>

### 문제 정의

참가자의 정보와 개인 취향이 담겨있는 스피드데이팅 데이터셋을 분석해 어떤 사람들끼리 커플 성사가 잘 되는지 예측한다.

 - 미션: 커플 성사 여부 예측
 - 알고리즘: XG부스트
 - 데이터셋: 독립변수로는 상대방과 내 정보, 개인의 취향, 상대방에 대한 평가 등이 있으며, 종속 변수로 매칭 성사 여부가 있다.
 - 문제 유형: 분류
 - 평가지표: 정확도, 혼동 행렬, 분류 리포트
 - 사용 라이브러리
    - numpy: 1.19.5
    - pandas: 1.3.5
    - seaborn: 0.11.2
    - matplotlib: 3.2.2
    - sklearn: 1.0.2
    - xgboost: 0.90

<br/>

### 라이브러리 및 데이터 불러오기 & 데이터 확인

 - `데이터 확인`
    - 독립 변수(38개)
        - has_null: Null값이 있는지 여부
        - age: 본인 나이
        - age_o: 상대방 나이
        - race: 본인 인종
        - race_o: 상대방 인종
        - importance_same_race: 인종을 중요하게 여기는지 여부
        - importance_same_religion: 종교를 중요하게 여기는지 여부
        - attractive_o: 매력적인
        - sincere_o: 성실한
        - intelligence_o: 지적
        - funny_o: 재미난
        - ambitous_o: 야심찬
        - shared_interests_o: 공통 관심사
        - intellicence_important: 관심사 연관도
        - expected_happy_with_sd_people: 만날 사람과의 기대치
        - expected_num_interested_in_me: 만날 사람이 나에게 보일 기대치
        - like: 파트너가 마음에 들었는지 여부
        - guess_prob_liked: 파트너가 나를 마음에 들어했을지에 대한 예상
        - met: 파트너를 이벤트 이전에 만난 적이 있는지 여부
    - 종속 변수(1개)
        - match: 매칭 성사 여부
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/dating.csv'
data = pd.read_csv(file_url)

data.head()
data.info() # 변수 특징 출력
round(data.describe(), 2) # 통계 정보 출력
```

<br/>

### 전처리: 결측치 처리

대부분의 변수에서 결측치가 보이지만, 대체로 5% 미만이다.  
결측치에 대해서 데이터에 등장하지 않을 법한 임의의 숫자(-99)로 채워넣는 것으로 해당 사람은 해당 항목에 응답하지 않음을 나타낼 수 있다.  
단, 피처 엔지니어링에서 중요도 * 점수로 계산을 하기 때문에 중요도와 관련된 변수들은 결측치를 제거하는 방향으로 처리한다.  

```python
# 결측치 비율 확인
data.isna().mean()

# 결측치 제거
data = data.dropna(subset=['pref_o_attractive', 'pref_o_sincere', 'pref_o_intelligence', 'pref_o_funny', 'pref_o_ambitious', 'pref_o_shared_interests','attractive_important', 'sincere_important', 'intellicence_important', 'funny_important', 'ambtition_important', 'shared_interests_important'])

# 나머지 변수들의 결측치는 -99로 채움
data = data.fillna(-99)
```

<br/>

### 전처리: 피처 엔지니어링

우선, 상대방 나이와 본인 나이를 통해 나이차이가 얼마나 나는지를 계산한다.  
이때, 결측치(-99)에 해당하는 값이 있을 수 있다. 남자, 여자 둘중 하나라도 -99라면, 알 수 없음의 의미로 나이차에 -99로 저장한다.  

```python
def age_gap(x):
    if x['age'] == -99:
        return -99
    elif x['age_o'] == -99:
        return -99
    elif x['gender'] == 'female':
        return x['age_o'] - x['age']
    else:
        return x['age'] - x['age_o']

data['age_gap'] = data.apply(age_gap, axis=1) # age_gap에 나이차 저장
data['age_gap_abs'] = abs(data['age_gap']) # age_gap_abs에 나이차를 절댓값으로 저장
```

<br/>

다음은 인종 데이터 관련 피처 엔지니어링을 진행한다.  
본인과 상대방의 인종이 같으면 1, 다르면 -1으로 처리하며, 결측치는 -99를 반환하도록 한다.  

```python
def same_race(x):
    if x['race'] == -99:
        return -99
    elif x['race_o'] == -99:
        return -99
    elif x['race'] == x['race_o']:
        return 1
    else:
        return -1     

data['same_race'] = data.apply(same_race, axis=1)
```

<br/>

인종 관련 변수로는 importance_same_race도 있다.  
동일 인종 여부가 얼마나 중요한지를 의미하기 때문에, same_race 변수와 이 변수를 곱하여 새 변수를 만든다.  
해당 계산 결과는 동일 인종이면 양수, 아니면 음수가 되며 중요할수록 절대값이 크다.  

```python
def same_race_point(x):
    if x['same_race'] == -99:
        return -99
    else:
        return x['same_race'] * x['importance_same_race']

data['same_race_point'] = data.apply(same_race_point, axis=1)
```

<br/>

마지막으로 attractive와 sincere 등에 대한 평가/중요도 변수들을 다룬다.  
간단하게 평가 점수 * 중요도로 계산하여 새로운 변수를 만든다.  

매개변수는 3개로 data는 데이터프레임을, importance와 score는 각각 중요도와 평가 변수를 받는다.  


```python
def rating(data, importance, score):
    if data[importance] == -99:
        return -99
    elif data[score] == -99:
        return -99
    else:
        return data[importance] * data[score]

data.columns[8:14] # 컬럼의 8자리부터 14 이전 자리까지 출력

partner_imp = data.columns[8:14]      # 상대방의 중요도
partner_rate_me = data.columns[14:20] # 본인에 대한 상대방의 평가
my_imp = data.columns[20:26]          # 본인의 중요도
my_rate_partner = data.columns[26:32] # 상대방에 대한 본인의 평가

# 계산된 값을 받아줄 새 변수 컬럼명 정의: 새변수명 = 중요도 변수명 * 평가변수명
new_label_partner = ['attractive_p', 'sincere_partner_p', 'intelligence_p', 'funny_p', 'ambition_p', 'shared_interests_p']
new_label_me = ['attractive_m', 'sincere_partner_m', 'intelligence_m', 'funny_m', 'ambition_m', 'shared_interests_m']

for i,j,k in zip(new_label_me, my_imp, my_rate_partner):
    data[i] = data.apply(lambda x: rating(x, j, k), axis=1)
```

<br/>

마지막으로 object타입 변수들을 숫자 형태가 되게끔 더미 변수로 변경해준다.  
gender, race, race_o 단 3개 변수만이 object 타입이다.  

```python
data = pd.get_dummies(data, columns=['gender','race','race_o'], drop_first=True)
```

<br/>

### 모델링 및 평가

모델링에 사용할 훈련셋과 시험셋을 분리하고, XGBoost 알고리즘으로 모델을 학습한다.  
n_estimators, max_depth, random_state 총 3가지하이퍼 파라미터에 임의의 값을 설정한다.  

```python
# 훈련셋과 시험셋 분리
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data.drop('match',axis=1), data['match'], test_size=0.2, random_state=100)

# XGBoost 모델 학습
import xgboost as xgb

model = xgb.XGBClassifier(n_estimators = 500, max_depth = 5, random_state=100)
model.fit(X_train, y_train)
pred= model.predict(X_test) # 예측

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
accuracy_score(y_test, pred) # 정확도: 86%
```

<br/>

정확도는 약 86%가 나오며, 수치상 좋아보일 수 있지만 데이터 특성을 고려하면 그렇지 못하다.  
confusion_matrix()를 사용해 정보를 더 구체적으로 살펴본다.  

실제값이 0인데 0으로 예측한 경우가 1291건으로 가장 많다. 매칭된 경우를 제대로 예측한 경우도 114건으로 무난한 수준이다.  
혼동 행렬에서 1종 오류, 즉 실제값은 0인데 1로 예측한 경우가 68건, 반대로 2종 오류는 약 147건으로 상당히 많다.  
모델 간의 비교/평가를 진행할 떄는 오류 유형에 따른 평가를 해야 한다. 사이킷런에서 제공하는 classification_report() 함수를 이용하면 이와 관련된 평가 수치를 일목요연하게 확인할 수 있다.  

```python
print(confusion_matrix(y_test, pred)) # [[1297 68] [ 147 114]]

print(classification_report(y_test, pred))
```

<br/>

### 이해하기: 경사하강법

경사하강법은 머신 러닝이 학습시킬 때 최소의 오차를 찾는 방법이다. 오차 함수에 대한 경사도(미분계수)를 기준으로 매개변수를 반복적으로 이동해가며 최소 오차를 찾는다.  

아래 과정을 반복하면서 함수의 최솟값에 수렴하게 됩니다. 그러나 학습률이 너무 크면 발산할 수 있고, 너무 작으면 수렴이 느려질 수 있습니다. 따라서 적절한 학습률을 선택하는 것이 중요합니다.  
 - 현재 위치에서 기울기 계산: 최적화하려는 함수의 현재 위치에서의 기울기(경사)를 계산합니다. 이는 함수의 미분을 통해 얻을 수 있습니다.
 - 이동 방향 결정: 기울기가 가리키는 방향은 함수가 가장 빠르게 증가하는 방향입니다. 하지만 우리는 최솟값을 찾아야 하므로, 기울기의 반대 방향으로 이동하려고 합니다.
 - 이동 거리 결정: 얼마나 멀리 이동할지 결정합니다. 이것을 학습률(learning rate)이라고 하며, 사용자가 설정해야 하는 하이퍼파라미터입니다.
 - 위치 업데이트: 결정된 방향과 거리에 따라 현재 위치를 업데이트합니다. 이를 반복하면서 최적화 과정을 진행합니다.

<br/>

### 하이퍼파라미터 튜닝: 그리드 서치

하이퍼파라미터 튜닝으로 임의의 값들을 하나씩 넣어보며 더 나은 결과를 찾을 수 있다.  
하지만, 이러한 방식은 하나하나 확인하며 모델링 과정을 기다리고 재시도하는 단순 작업을 반복해야 한다.  
그리드 서치를 이용하면 한 번 시도로 수백 가지 하이퍼 파라미터값을 시도해볼 수 있다.  

그리드 서치에 입력할 하이퍼파라미터 후보들을 입력하면, 각 조합에 대해 모두 모델링해보고 최적의 결과가 나오는 하이퍼파라미터 조합을 알려준다.  

 - learning_rate: 경사하강법에서 매개변수를 얼만큼씩 이동해가면서 최소 오차를 찾을지, 그 보폭의 크기를 결정하는 하이퍼하라미터이다. 기본적으로 보폭은 미분계수에 의해 결정되지만, learning_rate를 크게 하면 더 큰 보폭을, 작게 하면 작은 보폭으로 움직인다.
 - max_depth: 각 트리의 깊이를 제한한다.
 - subsample: 모델을 학습시킬 때 일부 데이터만 사용하여 각 트리를 만든다. 0.5를 쓰면 데이터의 절반씩만 랜덤 추출하여 트리를 만든다. 이 또한 오버피팅을 방지하는 데 도움이 된다.
 - n_estimators: 전체 나무의 갯수를 정한다.
```python
from sklearn.model_selection import GridSearchCV

parameters = {
              'learning_rate': [0.01, 0.1, 0.3],
              'max_depth': [5,7,10],
              'subsample': [0.5,0.7,1],                 
              'n_estimators': [300, 500, 1000]
                }

model = xgb.XGBClassifier()

# n_jobs: 사용할 코어 수
# scoring: 모델링할 떄 어떤 기준으로 최적의 모델을 평가할지 정의 (F1-점수 기준)
# cv: 교차 검증에 사용할 K-폴드값
gs_model = GridSearchCV(model, parameters, n_jobs=-1, scoring='f1', cv = 5)
gs_model.fit(X_train, y_train) # 학습
gs_model.best_params_ # 최적의 하이퍼파라미터 출력: {'learning_rate': 0.3, 'max_depth': 5, 'n_estimators': 1000, 'subsample': 0.5}

# 그리드 서치를 이용해 새로운 데이터를 예측: 자동으로 최적의 하이퍼파라미터 조합으로 반영된다.
pred = gs_model.predict(X_test) # 예측
accuracy_score(y_test, pred) # 정확도 계산: 0.86
print(classification_report(y_test, pred))

# 결과
# 정확도는 미세하게 올라갔고, F1-점수는 0.02 상승했다.
# 일반적으로 하이퍼파라미터 튜닝으로 엄청난 개선을 얻기는 쉽지 않다.
# 예측에는 피처 엔지니어링과 모델 알고리즘 선정이 큰 영향을 미친다.
```

<br/>

### 중요 변수 확인

선형 회귀와 로지스틱 회귀에서는 계수로, 결정 트리에서는 노드의 순서로 변수의 영향력을 확인했다.  
부스팅 모델은 이전 모델들보다 훨씬 복잡한 알고리즘으로 단순하게 변수의 영향력을 파악하기는 어렵지만, XGBoost에 내장된 함수는 변수의 중요도까지 계산해준다.  
단, 그리드 서치로 학습된 모델에서는 이 기능을 사용할 수 없다. 그리드 서치로 최적의 하이퍼파라미터 조합을 찾고, 해당 조합으로 학습시켜 해당 기능을 사용한다.  

변수 중요도는 넘파이 형태로 변수 이름 없이 순서대로 숫자만 나열된다.  
X_train의 변수 이름을 사용하여 feature_imp라는 이름의 데이터프레임으로 만들어 변수 이름과 매칭시켜 확인한다.  
추가적으로, 변수 중요도를 맥플롯립을 이용해 바 그래프로 상위 10개의 중요 변수를 바 그래프로 가시적으로 확인한다.  



```python
# 최적의 하이퍼파라미터: {'learning_rate': 0.3, 'max_depth': 5, 'n_estimators': 1000, 'subsample': 0.5}
model = xgb.XGBClassifier(learning_rate = 0.3, max_depth = 5, n_estimators = 1000, subsample = 0.5, random_state=100)
model.fit(X_train, y_train)

# 변수 중요도 확인
model.feature_importances_

feature_imp = pd.DataFrame({'features': X_train.columns, 'values': model.feature_importances_})
feature_imp.head()

# 중요 변수 그래프로 확인
plt.figure(figsize=(20, 10)) # 그래프 크기 설정
sns.barplot(x='values', y='features',
data=feature_imp.sort_values(by='values', ascending=False).head(10))
```

<br/>

### 이해하기: XGBoost

 - `배깅`
    - 부트스트랩 샘플링: 원본 데이터에서 무작위로 중복을 허용하여 샘플을 추출하는 과정입니다. 이로써 하나의 모델이 동일한 데이터를 여러 번 학습하거나, 서로 다른 모델이 유사한 데이터를 가질 수 있습니다.
    - 모델 학습: 부트스트랩 샘플을 사용하여 각각의 모델을 독립적으로 학습합니다. 이 때, 각 모델은 약간씩 다른 데이터로 학습하게 되므로 다양성이 증가하고, 과적합을 줄일 수 있습니다.
    - 예측 결합: 각 모델의 예측을 결합하여 최종 예측을 만듭니다. 분류 문제에서는 투표(voting)를 통해 다수결로 예측을 내리고, 회귀 문제에서는 평균이나 중간값을 사용합니다.
배깅(Bagging)은 앙상블 학습의 한 형태로, 여러 개의 분류기(Classifier)나 회귀 모델을 병렬적으로 학습하고, 그 결과를 결합하여 보다 정확하고 안정적인 예측을 하려는 기법입니다. "배깅"은 부트스트랩 샘플을 사용하여 각 모델을 학습하는 것에서 비롯된 용어입니다.  
대표적인 배깅 알고리즘 중 하나는 랜덤 포레스트(Random Forest)입니다. 랜덤 포레스트는 의사결정 트리를 기반으로 하며, 각 트리는 부트스트랩 샘플을 사용하여 학습하고, 랜덤하게 선택된 특성 부분 집합만을 사용하여 분할을 수행합니다.  

<br/>

 - `부스팅`
    - 가중치 부여: 각 샘플에 가중치를 부여하며 모델을 학습시킵니다. 오분류된 샘플에 높은 가중치를 주어 다음 모델이 이를 더 잘 분류하도록 유도합니다.
    - 순차적 학습: 이전 모델의 성능을 토대로 새로운 모델을 학습시키기 때문에 순차적으로 진행됩니다. 각 모델은 이전 모델의 오차를 보완하도록 학습됩니다.
    - 자체 보정: 이전 모델이 만든 오차를 보정해가면서 성능을 향상시킵니다. 이로써 부스팅은 약한 학습기들을 결합하여 강한 학습기를 만들어내는 효과를 얻을 수 있습니다.
부스팅(Boosting)은 앙상블 학습의 한 형태로, 약한 학습기(weak learner)들을 결합하여 강한 학습기(strong learner)를 만드는 알고리즘입니다. 부스팅은 이전 모델이 잘못 분류한 샘플에 가중치를 높여주면서 순차적으로 모델을 학습시키는 특징이 있습니다. 이렇게 순차적으로 학습을 진행하면서, 각 모델이 이전 모델의 오차를 보완해나가는 방식입니다.  
대표적인 부스팅 알고리즘으로는 아다부스트(AdaBoost), 그래디언트 부스팅(Gradient Boosting), XGBoost, LightGBM, CatBoost 등이 있습니다. 이들 알고리즘은 각각 다른 방식으로 가중치를 업데이트하고 모델을 학습시키지만, 기본 아이디어는 비슷합니다.  
부스팅은 과적합에 강하고, 높은 성능을 낼 수 있으며, 다양한 종류의 데이터에 효과적입니다. 그러나 계산 비용이 크고, 훈련 시간이 오래 걸릴 수 있습니다.  

 - `경사 부스팅`
    - 손실 함수의 그래디언트 활용: 경사 부스팅은 손실 함수(예를 들면 평균 제곱 오차(Mean Squared Error) 등)의 그래디언트 정보를 사용하여 각 모델을 학습합니다. 이 그래디언트는 현재 모델의 예측과 실제 값 사이의 오차를 나타냅니다.
    - 순차적 학습: 모델은 이전 모델의 예측과 실제 값 사이의 오차에 대한 그래디언트 정보를 사용하여 학습됩니다. 이를 통해 각 모델은 이전 모델이 놓친 패턴을 학습하고, 예측을 보완합니다.
    - 충분히 작은 학습률 사용: 경사 부스팅에서는 일반적으로 작은 학습률(learning rate)을 사용합니다. 학습률이 작을수록 모델이 더욱 조금씩 업데이트되므로, 안정적으로 수렴할 수 있습니다.
    - 편향-분산 트레이드오프 해결: 경사 부스팅은 약한 학습기를 조합하여 강한 모델을 만들면서 편향과 분산의 트레이드오프를 조절합니다. 이를 통해 과적합을 피하면서도 높은 성능을 달성할 수 있습니다.
경사 부스팅(Gradient Boosting)은 부스팅의 한 형태로, 이전 모델의 오차를 보정하면서 순차적으로 약한 학습기(weak learner)를 학습시키는 앙상블 학습 알고리즘입니다. 경사 부스팅은 손실 함수의 그래디언트(기울기) 정보를 활용하여 모델을 학습하고, 이를 통해 오차를 줄이는 방향으로 모델을 계속 업데이트합니다.  
대표적인 경사 부스팅 라이브러리로는 XGBoost, LightGBM, CatBoost 등이 있습니다. 이러한 라이브러리들은 속도 및 성능 측면에서 최적화되어 있어 다양한 실제 문제에 효과적으로 적용됩니다.  

### 학습 마무리

 - `핵심 용어`
    - XGBoost: 부스팅 기법의 하나로, 각 트리가 독립적인 랜덤 포레스트와 달리 이전 트리를 기반으로 새로운 트리를 생성하며, 2차 도함수 활용과 정규화 하이퍼파라미터 지원이라는 특징을 지닌다.
    - 부스팅 알고리즘: 부스팅은 랜덤 포레스트에서 그 다음 세대로 진화하게 되는 중요한 개념으로 랜덤 포레스트에서는 각각의 트리를 독립적으로, 즉 서로 관련 없이 만드는 반면, 부스팅 알고리즘에서는 트리를 순차적으로 만들면서 이전 트리에서 학습한 내용이 다음 트리를 만들 때 반영된다.
    - 경사하강법: 경사 부스팅의 핵심 개념 중 하나로, 모델이 어떻게 최소 오차가 되는 매개변수들을 학습하는지에 대한 방법론이다. 오차식에 대한 미분계수를 통해 매개변수의 이동방향과 보폭을 결정한다. 보폭은 러닝 레이트라는 하이퍼파라미터로 조절할 수 있다.

