# 07장. 나이브 베이즈: 스팸 여부 판단하기

## 나이브 베이즈

나이브 베이즈는 베이즈 정리를 적용한 조건부 확률 기반의 분류 모델이다.  
여기서 조건부 확률은 A가 일어났을 때 B가 일어날 확률을 의미한다.  
예를 들어, '무료'라는 단어가 들어있는 메일은 스팸 메일일 확률이 높은 것과 같이 이러한 특징으로 스팸 필터링을 위한 대표적인 모델로 꼽힌다.  

최근에는 딥러닝 같은 대안이 있어 나이브 베이즈 모델을 사용하는 상황이 많지 않지만, 스팸 메일 필터처럼 자연어 처리가 목적일 때는 여전히 나이브 베이즈 모델이 좋은 선택이 될 수 있다.  
범용성이 높지는 않지만 독립변수들이 모두 독립적이라면 충분히 경쟁력 있는 알고리즘이다.  
 
 - 장점
    - 비교적 간단한 알고리즘에 속하며 속도 또한 빠르다.
    - 작은 훈련셋으로도 잘 예측한다.
 - 단점
    - 모든 도립변수가 각각 독립적임을 전제로 하는데 이는 장점이 되기도 하고 단점이 되기도 한다.
    - 실제로 독립변수들이 모두 독립적이라면 다른 알고리즘보다 우수할 수 있지만, 실제 데이터에서 그런 경우가 많지 않아 단점이 될 수 있다.
 - 사용처
    - 각 독립변수들이 모두 독립적이고 그 중요도가 비슷할 때 유용하다.
    - 자연어 처리에서 간단하지만 좋은 성능을 보인다.
    - 범주 형태의 변수가 많을 때 적합하며, 숫자형 변수가 많을 떄 적합하지 않다.

<br/>

### 문제 정의

자연어로 된 스팸 문자를 판단한다.  

 - 미션: 문자 데이터셋을 이용해 스팸 여부 판단
 - 알고리즘: 나이브 베이즈
 - 데이터셋: 스팸 문자에 대한 데이터로, 독립변수는 text 하나이다. 해당 변수에는 긴 문장 형태의 데이터들이 들어있어 많은 전처리 작업이 필요하다. 각 문장에 들어간 단어들을 활용하여 문자가 스팸인지 아닌지를 예측한다.
 - 문제 유형: 분류
 - 평가지표: 정확도, 혼동 행렬
 - 사용 라이브러리
    - numpy: 1.19.5
    - pandas: 1.3.5
    - seaborn: 0.11.2
    - matplotlib: 3.2.2
    - sklearn: 1.0.2
    - nltk: 3.2.5

<br/>

### 라이브러리 및 데이터 불러오기 & 데이터 확인

 - `데이터 확인`
    - 독립 변수(1개)
        - text: 스팸 여부를 판별하는 데 사용할 문자열
    - 종속 변수(1개)
        - target: 스팸인지 아닌지 정보가 들어있음(ham: 스팸X, spam: 스팸 문자)
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/spam.csv'
data = pd.read_csv(file_url)

data.head()
data['target'].unique() # 목표 변수의 고윳값 확인
```

<br/>

### 전처리: 특수 기호 제거하기

쉼표, 마침표 등과 같은 특수 기호를 제거한다.  
자연어를 다룰 때 데이터의 기준은 단어로 특수 기호는 단어를 처리할 때 노이즈가 되므로 제거한다.  

 - `특수 기호 제거하기`
    - 파이썬에 내장된 string 모듈에서 특수 기호 목록을 얻을 수 있다.
    - apply() 함수로 데이터프레임 전체가 아닌 한 줄씩 함수에 적용할 수 있다.
```python
import string

# 문자열에서 문자 하나씩 꺼내 특수기호 제거
sample_string = data['text'].loc[0]
new_string = [] # 빈 리스트 생성
for i in sample_string: # 문자열 순회
    if i not in string.punctuation # 특수 기호가 아닌 경우
        new_string.append(i) # 리스트에 문자 추가
new_string = ''.join(new_string) # 리스트를 문자열 형태로 변환

# 별도의 함수로 만들기
def remove_punc(x):
    new_string = []
    for i in x:
        if i not in string.punctuation:
            new_string.append(i)
    new_string = ''.join(new_string)
    return new_string

data['text'].apply(remove_punc) # 함수에 한 행씩 적용되도록 실행
data['text'] = data['text'].apply(remove_punc) # 데이터셋 업데이트
```

<br/>

### 전처리: 불용어 제거하기

불용어는 자연어 분석에 큰 도움이 안 되는 단어를 의미한다.  
이러한 단어를 제거함으로써 데이터를 조금이나마 더 가볍게 만들 수 있다.  
자연어 처리에서는 각 단어가 하나의 독립변수처럼 작용하기 때문에, 컬럼이 2개뿐이더라도 분석 과정에서 데이터를 방대하게 펼치게 된다.  


 - `불용어 제거`
    - 한국어 불용어는 https://www.ranks.nl/stopwords/korean 에서 받을 수 있다.
```python
import nltk
nltk.download('stopwords') # 불용어 목록 가져오기

import nltk.corpus import stopwords

stopwords.words('english') # 영어 불용어 선택
print(stopwords.fileids())

# 불용어 제거
sample_string = data['text'].loc[0]
sample_string.split() # 단어 단위로 문장 분할
new_string = [] # 빈 리스트 생성
for i in sample_string.split() # 순회
    if i.lower() not in stopwords.words('english'): # 소문자로 변환한 단어가 불용어가 아닌 경우
        new_string.append(i.lower()) # 문자 단위로 추가
new_string = ' '.join(new_string) # 공백 단위로 묶기

# 함수로 만들기
def stop_words(x):
    new_string = []
    for i in x.plit():
        if i.lower() not in stopwords.words('english'):
            new_string.append(i.lower())
    new_string = ' '.join(new_string)
    return new_string

data['text'] = data['text'].apply(stop_words)
```

<br/>

### 전처리: 카운트 기반으로 벡터화하기

카운트 기반 벡터화는 문자를 개수 기반으로 벡터화하는 방식이다.  
데이터 전체에 존재하는 모든 단어들을 사전처럼 모은 뒤에 인덱스를 부여하고, 문장마다 속한 단어가 있는 인덱스를 카운트하는 것이다.  

 - `카운트 기반 벡터화하기`
    - CountVectorizer 사용방법은 scaling과 상당히 유사하다. fit()으로 학습하며 transform()으로 변환한다.
```python
from sklearn.feature_extraction.text import CountVectorizer

x = data['text'] # 독립변수
y = data['target'] # 종속변수

cv = CountVectorizer() # 객체 생성
cv.fit(x) # 학습하기
cv.vocabulary_ # 단어와 인덱스 출력

x = cv.transform(x) # 트랜스폼
print(x)
print(cv.vocabulary_['go'])
print(cv.vocabulary_['jurong'])
print(cv.vocabulary_['point'])
```


<br/>

### 모델링 및 예측/평가하기

카운트 기반 벡터화 과정에서 X와 y로 데이터를 나누어주었다.  
이를 활용하여 train_test_split() 함수로 독립변수/종속변수에 대한 훈련셋/시험셋 분할을 진행한다.  

 - `모델링 및 예측/평가하기`
    - 나이브 베이즈 알고리즘으로 MultinomialNB 모듈을 사용한다.
    - 해당 모듈은 다항 분포에 대한 Naive Bayes 알고리즘이다. 그 외에도 정규분포, 베르누이 분포에 따른 NB 모듈이 있다.
    - confusion_matrix()는 실제값과 예측값들이 각각 어떻게 분포되었는지를 행렬로 나타낸다.
```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 100)

model = MultinomialNB()
model.fit(x_train, y_train)
pred = model.predict(x_test)

accuracy_score(y_test, pred) # 정확도 계산
print(confusion_matrix(y_test, pred)) # 혼동 행렬 출력
sns.heatmap((confusion_matrix(y_test, pred), annot=True, fmt='.0f')
```

<br/>

### 이해하기: K-최근접 이웃

나이브 베이즈 알고리즘의 근간은 베이즈 정리이다.  
따라서 나이브 베이즈 알고리즘을 이해하려면 조건부 확률을 구하는 베이즈 정리를 이해해야만 한다.  
 - 사후 확률: 사건 A와 B가 있을 때, 사건 A가 발생한 상황에서 사건 B가 발생할 확률
 - 사전 확률: 사건 A와 상관없이 사건 B가 발생할 확률
 - 베이즈 정리: 두 확률 변수의 사전 확률과 사후 확률 사이의 관계를 나타내는 정리로, 사후 확률을 구할 때 쓰임
 - 사후 확률 = 사전 확률 * 가능도(A가 발생했을 때 B가 발생할 확률) / 전체에서 B가 발생할 확률
    - 사후 확률 P(A|B) = B라는 특정 단어가 등장했을 때 A가 스팸일 확률
    - 사전 확률 P(A) = B의 발생유무와 관련없이 기본적으로 A가 발생할 확률로 전체 문자 중 스팸문자의 비율
    - 가능도 P(B|A) = A가 발생했을 때 B가 발생할 확률로 스팸 메일인 경우 B라는 특정 단어가 들어 있을 확률
    - P(B) = 전체에서 B가 발생할 확률로 전체 문자에서 B라는 특정 단어가 들어 있을 확률

<br/>

### 학습 마무리

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 라이브러리 및 데이터 불러오기 & 데이터 확인
file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/spam.csv'
data = pd.read_csv(file_url)

data.head()
data['target'].unique() # 목표 변수의 고윳값 확인

# 전처리: 특수 기호 제거 함수
def remove_punc(x):
    new_string = []
    for i in x:
        if i not in string.punctuation:
            new_string.append(i)
    new_string = ''.join(new_string)
    return new_string

data['text'] = data['text'].apply(remove_punc) # 데이터셋 업데이트

# 전처리: 불용어 제거 함수
def stop_words(x):
    new_string = []
    for i in x.plit():
        if i.lower() not in stopwords.words('english'):
            new_string.append(i.lower())
    new_string = ' '.join(new_string)
    return new_string

data['text'] = data['text'].apply(stop_words) # 데이터셋 업데이트

# 전처리: 카운트 기반으로 벡터화하기
x = data['text'] # 독립변수
y = data['target'] # 종속변수

cv = CountVectorizer() # 객체 생성
cv.fit(x) # 학습하기

# 모델링 및 예측하기
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 100)

model = MultinomialNB()
model.fit(x_train, y_train)
pred = model.predict(x_test)

accuracy_score(y_test, pred) # 정확도 계산
print(confusion_matrix(y_test, pred)) # 혼동 행렬 출력
sns.heatmap((confusion_matrix(y_test, pred), annot=True, fmt='.0f')

```

<br/>

 - `핵심 용어`
    - 나이브 베이즈 분류기: 조건부확률을 기반으로 하는 모델로, 자연어와 같이 변수의 개수가 많을 때 유용하다.
    - 1종 오류: 실제 음성인 것을 양성으로 예측하는 오류
    - 2종 오류: 실제 양성인 것을 음성으로 예측하는 오류
    - 사후 확률: 사건 A와 B가 있을 때, 사건 A가 발생한 상황에서 사건 B가 발생할 확률
    - 사전 확률: 사건 A와 상관없이 사건 B가 발생할 확률
    - 베이즈 정리: 두 확률 변수의 사전 확률과 사후 확률 사이의 관계를 나타내는 정리로, 사후 확률을 구할 때 쓰인다.

