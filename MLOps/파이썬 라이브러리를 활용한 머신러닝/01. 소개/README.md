# 소개

## 머신 러닝 소개

### 머신러닝으로 풀 수 있는 문제

 - `지도 학습`
    - 알고리즘에 입력과 기대되는 출력을 제공하고 알고리즘은 주어진 입력에서 원하는 출력을 만드는 방법을 찾는다. 이렇게 학습된 알고리즘은 사람의 도움 없이도 새로운 입력이 주어지면 적절한 출력을 만들 수 있다.
    - 입력한 데이터로부터 기대한 출력이 나오도록 알고리즘을 가르치는 것으로 입력과 출력으로부터 학습하는 머신러닝 알고리즘을 지도 학습 알고리즘이라고 한다.
    - __지도 학습 활용 예시__
        - 편지 봉투에 손으로 쓴 우편번호 숫자 판별
        - 의료 영상 이미지에 기반한 종양 판단
        - 의심되는 신용카드 거래 감지
 - `비지도 학습`
    - 비지도 학습은 알고리즘에 입력은 주어지지만 출력은 제공되지 않는다.
    - __비지도 학습 활용 예시__
        - 블로그 글의 주제 구분
        - 고객들을 취향이 비슷한 그룹으로 묶기
        - 비정상적인 웹사이트 접근 탐지

<br/>

### 문제와 데이터 이해하기

머신러닝 프로세스에서 가장 중요한 과정은 사용할 데이터를 이해하고 그 데이터가 해결해야 할 문제와 어떤 관련이 있는지 이해하는 일이다. 알고리즘마다 잘 들어맞는 데이터나 문제의 종류가 다르다.  

<br/>

## 파이썬

파이썬은 데이터 과학 분야를 위한 표준 프로그래밍 언어가 되어가고 있다.  
파이썬은 범용 프로그래밍 언어의 장점은 물론 매트랩과 R 같은 특정 분야를 위한 스크립팅 언어의 편리함을 갖췄다.  
또한, 파이썬은 데이터 적재, 시각화, 통계, 자연어 처리, 이미지 처리 등에 필요한 라이브러리를 갖고 있다.  

<br/>

## scikit-learn

사이킷런(scikit-learn)은 오픈 소스로 자유롭게 사용하거나 배포할 수 있고, 누구나 소스 코드를 보고 어떻게 동작하는 쉽게 확인할 수 있다. 사이킷런은 다양한 머신러닝 알고리즘을 제공하며, 꾸준히 개발 향상되고 활발한 커뮤니티를 갖고 있다.  
 - 사이킷런 공식 문서: http://scikit-learn.org/stable/documentation
 - 사이킷런 사용자 가이드: http://scikit-learn.org/stable/user_guide.html
 - 사이킷런 API 문서: http://scikit-learn.org/stable/modules/classes.html

<br/>

### scikit-learn 설치

사이킷런은 NumPy와 SciPy를 사용한다.  
그래프를 그리려면 matplotlib(맷플롯립), 대화식으로 개발하려면 IPython(아이파이썬)과 주피터 노트북을 설치해야 한다.  
 - `Anaconda`
    - 공식 사이트: https://www.anaconda.com
    - 아나콘다는 대용량 데이터 처리, 예측 분석, 과학 계산용 파이썬 배포판으로 NumPy, SciPy, matplotlib, pandas, IPython, 주피터 노트북, scikit-learn 등을 포함한다.
    - macOs, 윈도우, 리눅스 모두 지원하며 매우 편리한 기능을 제공한다.
 - `ActivePython`
    - 공식 사이트: https://www.activestate.com/products/python/
    - 범용 파이썬 배포판으로 NumPy, SciPy, matplotlib, pandas, Jupyter, scikit-learn을 포함한다.
    - 무료로 사용할 수 있는 Community Edition과 기업을 위한 유료 버전이 존재한다.
 - `Python (x,y)`
    - 공식 사이트: http://python-xy.github.io/
    - 윈도우 환경을 위한 과학 계산용 무료 파이썬 배포판으로 NumPy, SciPy, matplotlib, pandas, IPython, scikit-learn을 포함한다.
 - `직접 설치`
    - 파이썬을 설치했다면 pip 명령을 사용하여 필요한 패키지들을 설치할 수 있다.
    - $ pip install numpy scipy matplotlib ipython scikit-learn pandas pillow imageio

<br/>

## 필수 라이브러리

 - `주피터 노트북`
    - 주피터 노트북은 프로그램 코드를 브라우저에서 실행해주는 대화식 환경이다.
 - `NumPy`
    - NumPy는 다차원 배열을 위한 기능과 선형 대수 연산, 푸리에 변환 같은 고수준 수학 함수와 유사 난수 생성기를 포함한다.
    - NumPy의 핵심 기능은 다차원 배열인 ndarray 클래스로 이 배열의 모든 원소는 동일한 데이터 타입이어야 한다.
    - scikit-learn은 NumPy 배열 혀앹의 데이터를 입력 받는다.
 - `SciPy`
    - SciPy는 고성능 선형 대수, 함수 최적화, 신호 처리, 특수한 수학 함수와 통계 분포 등을 포함한 많은 기능을 제공하는 과학 계산용 함수를 모아놓은 파이썬 패키지이다.
    - scikit-learn은 알고리즘을 구현할 때 SciPy의 여러 함수를 사용한다.
    - 가장 중요한 기능은 scipy.sparse 모ㅠㄹ로 데이터를 표현하는 또 하나의 방법인 희소 행렬 기능을 제공한다.
 - `matplotlib`
    - matplotlib은 대표적인 과학 계산용 그래프 라이브러리로 선 그래프, 히스토그램, 산점도 등을 지원하며 고품질 그래프를 그려준다.
    - 주피터 노트북에서 사용할 떄는 %matplotlib notebook이나 %matplotlib inline 명령을 사용하면 브라우저에서 바로 이미지를 볼 수 있다.
 - `pandas`
    - pandas는 R의 data.frame을 본떠서 설계한 DataFrame이라는 데이터 구조를 기반으로 만들어진 데이터 처리와 분석을 위한 파이썬 라이브러리이다.
    - DataFrame이라는 테이블 형태를 제공하며, 수정 및 조작하는 다양한 기능을 제공한다. SQL처럼 테이블에 쿼리나 조인을 수행할 수 있다.
    - pandas는 NumPy와 달리 각 열의 타입이 달라도 된다.
 - `mglearn`
    - mglearn은 머신러닝 모델을 시각화하고 이해하는 데 도움을 주는 함수와 도구를 제공한다. 이 패키지는 다양한 데이터셋, 예제, 플롯 함수 등을 포함하고 있어, scikit-learn을 사용하여 머신러닝을 공부하거나 시각화할 때 유용하게 사용된다.
```python
# NumPy
import numpy as np

x = np.array([[1, 2, 3], [4, 5, 6]])
print("x:\n", x)


# SciPy
from scipy import sparse

# 대각선 원소는 1이고 나머지는 0인 2차원 NumPy 배열을 만든다.
eye = np.eye(4) 
# NumPy 배열을 CSR 포맷의 SciPy 희박 행렬로 변환한다. 0이 아닌 원소만 저장된다.
sparse_matrix = sparse.csr_matrix(eye)


# matplotlib
%matplotlib inline
import matplotlib.pyplot as plt

# -10에서 10까지 100개의 간격으로 나뉘어진 배열을 생성한다.
x = np.linspace(-10, 10, 100)
# 사인 함수를 사용하여 y 배열을 생성한다.
y = np.sin(x)
# plot 함수는 한 배열의 갑승ㄹ 다른 배열에 대응해서 선 그래프를 그린다.
plt.plot(x, y, market="x")


# pandas
import pandas as pd

data = {
    "Name": ["John", "Anna", "Peter", "Linda"],
    "Location": ["New York", "Paris", "Berlin", "London"],
    "Age": [24, 13, 53, 33]
}
data_pandas = pd.DataFrame(data)
```

 - `예제 코드 라이브러리 버전`
    - Python: 3.7.3
    - pandas: 1.3.5
    - matplotlib: 3.5.1
    - NumPy: 1.21.4
    - SciPy: 1.7.3
    - IPython: 7.30.1
    - scikiet-learn: 1.0.1
```py
import sys
print("Python 버전:", sys.version)

import pandas as pd
print("pandas 버전:", pd.__version__)

import matplotlib
print("matplotlib 버전:", matplotlib.__version__)

import numpy as np
print("NumPy 버전:", np.__version__)

import scipy as sp
print("SciPy 버전:", sp.__version__)

import IPython
print("IPython 버전:", IPython.__version__)

import sklearn
print("scikit-learn 버전:", sklearn.__version__)
```

<br/>

## 첫 번쨰 애플리케이션 붖꽃의 품종 종류

식물학자는 붓꽃의 꽃잎과 꽃받침의 폭과 길이를 센티미터 단위로 측정한다.  
식물학자는 setosa, versicolor, virgincia 종으로 분류한 붓꽃의 측정 데이터를 가지고 있다.  
이 측정값을 이용해서 채집한 붓꽃 품종을 구분하며, 붓꽃 종류는 세 종류뿐이라고 가정한다.  

붓꽃의 품종을 정확하게 분류한 데이터를 가지고 있으므로 지도 학습에 속한다.  
몇 가지 선택사항(붓꽃의 품종) 중 하나를 선택하는 문제로 __분류 문제__ 에 해당하며, 출력될 수 있는 값(붓꽃의 조류)들을 __클래스__ 라고 한다.  
데이터 포인트 하나(붓꽃 하나)에 대한 기대 출력은 꽃의 품종이 되며, 이런 특정 데이터 포인트에 대한 출력(품종)을 __레이블__ 이라고 한다.  

 - `데이터 적재`
    - sklearn.dataset 안에는 빌트인(built-in) 데이터 셋들이 존재한다.
        - load_boston: 보스톤 집값 데이터
        - load_iris: 아이리스 붓꽃 데이터
        - load_diabetes: 당뇨병 환자 데이터
        - load_digits: 손글씨 데이터
        - load_linnerud: multi-output regression 용 데이터
        - load_wine: 와인 데이터
        - load_breast_cancer: 위스콘신 유방암 환자 데이터
    - 빌트인 데이터셋은 sklearn.utils.Bunch라는 자료 구조를 활용한다.
        - key-value 형식으로 구성되어 있으며, 사전형 타입과 유사한 구조를 가진다.
        - data: 샘플 데이터, NumPy 배열로 이루어져 있다.
        - target: Label 데이터, NumPy 배열로 이루저여 있다.
        - feature_names: Feature 데이터의 이름
        - target_names: Label 데이터의 이름
        - DESCR: 데이터 셋의 설명
        - filename: 데이터 셋의 파일 저장 위치(csv)
```py
# iris 붓꽃 데이터 로드
from sklearn.datasets import load_iris
iris_dataset = load_iris()

# Bunch 클래스의 객체로 구성된다.
print("iris_dataset의 키:", iris_dataset.keys())

# DESCR 키에는 데이터셋에 대한 간략한 설명이 있다.
print("dataset 설명:", iris_dataset['DESCR'][:193])

# Label 데이터의 이름(품종 종류)
print("타깃의 이름:", iris_dataset['target_names'])

# Feature 데이터의 이름(각 특성을 설명하는 문자열 리스트)
print("특성의 이름:", iris_dataset['feature_names'])

# 실제 데이터는 target과 data 필드에 있다.
print("data의 타입", type(iris_dataset['data']))
print("data의 크기", iris_dataset['data'].shape)
print("data 5개 출력:", iris_dataset['data'][:5])

print("target의 타입", type(iris_dataset['target']))
print("target의 크기:", iris_dataset['target'].shape)
print("타깃:", iris_dataset['target']) # 0은 setosa, 1은 versicolor, 2는 virginica
```

<br/>

 - `성과 측정: 훈련 데이터와 테스트 데이터`
    - 빌트인 데이터인 붓꽃 품종 데이터로 머신러닝 모델을 만들고 새로운 데이터의 품졸을 예측하려 한다. 모델을 새 데이터에 적용하기 전에 이 모델이 정말 잘 작동하는지 알아야 한다.
    - 모델의 성능을 측정하려면 레이블을 알고 있는 새 데이터를 모델에 적용해봐야 한다. 때문에, 빌트인 데이터 150개를 두 그룹으로 나눈다. 하나는 머신러닝 모델을 만들기 위한 훈련 데이터(훈련 세트)로 사용하고, 나머지는 모델이 잘 작동하는지 측정하기 위한 테스트 데이터(테스트 세트, 홀드아웃 세트)로 사용한다.
    - scikit-learn은 데이터셋을 섞어서 나눠주는 train_test_split 함수를 제공한다. 해당 함수는 전체 행 중에 75%를 레이블 데이터와 훈련 세트로 뽑고, 나머지 25%를 레이블 데이터와 테스트 세트로 뽑는다. scikit-learn에서 데이터는 대문자 X로 표시하고, 레이블은 소문자 y로 표기한다.
    - train_test_split 함수로 데이터를 나누기 전에 유사 난수 생성기를 사용해 데이터셋을 무작위로 섞어야 한다.
```python
# iris 붓꽃 데이터 로드
from sklearn.datasets import load_iris
iris_dataset = load_iris()

# 훈련 세트와 테스트 세트 나누기
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)

print("X_train 크기:", X_train.shape) # (112, 4)
print("X_test 크기:", X_test.shape) # (38, 4)

print("y_train 크기:", y_train.shape) # (112,)
print("y_test 크기:", y_test.shape) # (38,)
```

<br/>

 - `가장 먼저 할 일: 데이터 살펴보기`
    - 머신러닝 모델을 만들기 전에 머신러닝 없이도 풀 수 있는 문제인지, 혹은 필요한 정보가 누락되지 않았는지 데이터를 조사해보아야 한다.
    - 시각화는 데이터를 조사하는 아주 좋은 방법이다.
        - 산점도는 데이터에서 한 특성을 x 축에 놓고 다른 하나는 y 축에 놓아 각 데이터 포인트를 하나의 점으로 나타내는 그래프이다.
        - 컴퓨터 화면은 2차원이라 한 번에 2개의 특성만 그릴 수 있으므로, 산점도로 3개 이상의 특성을 표현하기에는 어렵다. 대신에 모든 특성을 짝지어 만드는 산점도 행렬을 사용할 수 있다.
        - 산점도 그래프를 그리기 위해서는 먼저 NumPy 배열을 pandas의 DataFrame으로 변경해주어야 하며, pandas에서 산점도 행렬을 그려주는 scatter_matrix 함수를 제공해준다.
    - 예제 코드로 그래프르 ㄹ만들어 확인하면, 세 클래스가 꽃잎과 꽃받침의 측정값에 따라 비교적 잘 구분되는 것을 알 수 있다.
```py
from sklearn.datasets import load_iris
iris_dataset = load_iris()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)

# X_train 데이터를 사용해서 데이터프레이믕ㄹ 만든다.
# 열의 이름은 iris_dataset.feature_names에 있는 문자열을 사용한다.
iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)

# 데이터 프레임을 사용해 y_train에 따라 색으로 구분된 산점도 행렬을 만든다.
pd.plotting.scatter_matrix(iris_dataframe, c=y_train, figsize=(15, 15), marker='o', hist_kwds={'bins': 20}, s=60, alpha=.8, cmap=mglearn.cm3)
```

<br/>

 - `첫 번째 머신러닝 모델: k-최근접 이웃 알고리즘`
    - scikit-learn은 다양한 분류 알고리즘을 제공한다.
        - k-최근접 이웃 분류기 모델은 단순히 훈련 데이터를 저장하여 만들어진다. k는 가장 가까운 이웃 하나가 아니라 훈련 데이터에서 새로운 데이터 포인트에 가장 가까운 'k개'의 이웃을 찾는다는 뜻이다.
        - 새로운 데이터 포인트에 대한 예측이 필요하면 알고리즘은 새 데이터 포인트에서 가장 가까운 훈련 데이터 포인트를 찾는다. 그 다음 찾은 훈련 데이터의 레이블을 새 데이터 포인트의 레이블로 지정한다.
        - scikit-learn의 모든 머신러닝 모델은 Estimator라는 파이썬 클래스로 각각 구현되어 있다. k-최근접 이웃 분류 알골지ㅡㅁ은 neighbors 모듈 아래 KNeighborsClassifier 클래스에 구현되어 있다.
```python
from sklearn.datasets import load_iris
iris_dataset = load_iris()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)

# knn 객체는 훈련 데이터로 모델을 만들고 새로운 데이터 포인트에 대해 예측하는 알고리즘을 캡슐화한 것이다.
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)

# 훈련 데이터셋으로부터 모델을 만들려면 knn 객체의 fit 메서드를 사용한다.
# 해당 메서드는 훈련 데이터인 NumPy 배열을 X_train과 훈련 데이터의 레이블을 담고 있는 NumPy 배열 y_train을 매개변수로 받는다.
knn.fit(X_train, y_train)
```

<br/>

 - `예측하기`
    - 모델을 사용해서 정확한 레이블을 모르는 새 데이터에 대해 예측을 만들 수 있다.
```python
from sklearn.datasets import load_iris
iris_dataset = load_iris()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

# 야생에서 꽃받침의 길이가 5cm, 폭이 2.9cm, 꽃잎의 길이가 1cm, 폭이 0.2cm인 붓꽃을 보았다고 가정
X_new = np.array([[5, 2.9, 1, 0.2]])
print("X_new.shape:", X_new.shape) # (1, 4)

# 예측에는 knn 객체의 predict 메서드를 사용한다.
prediction = knn.predict(X_new)
print("예측:", prediction) # [0]
print("예측한 타깃의 이름:", iris_dataset['target_names'][prediction]) # ['setosa']
```

<br/>

 - `모델 평가하기`
    - 모델 평가를 위해서 앞서 만든 테스트 세트를 이용한다.
    - 해당 데이터는 모델을 만들때 사용하지 않았고, 각 붓꽃의 품종을 정확히 알고 있다.
    - 따라서, 테스트 데이터에 있는 붓꽃의 품종을 예측하고 실제 레이블(품종)과 비교할 수 있다. 얼마나 많은 붓꽃 품종이 정확히 맞았는지 정확도를 계산하여 모델의 성능을 평가한다.
```python
# iris 붓꽃 데이터 로드
from sklearn.datasets import load_iris
iris_dataset = load_iris()

# 훈련 세트와 테스트 세트 나누기
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)

# 모델 만들기
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

# 모델 평가하기
y_pred = knn.predict(X_test)
print("테스트 세트에 대한 예측값:", y_pred)
print("테스트 세트의 정확도: {:.2f}".format(np.mean(y_pred == y_test)))
print("테스트 세트의 정확도: {:.2f}".format(knn.score(X_test, y_test)))
```
