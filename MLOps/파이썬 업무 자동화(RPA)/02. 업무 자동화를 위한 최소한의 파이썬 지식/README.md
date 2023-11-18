# 2장. 업무 자동화를 위한 최소한의 파이썬 지식

## 업무 자동화를 위한 개발 환경 설정

 - `Jupyter Notebook`
    - 아나콘다 설치
    - 기본 웹 브라우저 설정
    - 웹 드라이버 설치
    - Jupyter Notebook 실행 및 기본 폴더 설정
```
1. 아나콘다 설치
 - https://www.anaconda.com/
공식 문서에 접속하여 Anaconda를 설치한다. 이때, Add Anaconda3 to my PATH environment varialbe를 체크한다.
Anaconda를 설치하면 기본적으로 Jupyter Notebook이 설치된다.


2. 기본 웹 브라우저 설정
jupyter Notebook은 인터넷 환경을 빌려서 실행되며, 컴퓨터의 기본 브라우저로 열린다.
학습 편의상 Chrome 브라우저로 자동 실행하도록 한다.
 - [Windows + S] > 기본 웹 브라우저 선택
 - 웹 브라우저 > Google Chrome

3. 크롬 웹 드라이버 설치
크롬 웹 드라이버란 파이썬을 통해서 웹을 제어할 때 사용하는 소프트웨어이다.
해당 소프트웨어를 통해서 인터넷을 자유롭게 제어할 수 있다.
 - 크롬 버전 확인
    - 크롬 우측 상단 > 도움말 > Chrome 정보
 - 크롬 드라이버 설치
    - Chrome Web Driver 검색 > 브라우저 버전에 맞는 드라이버 설치

4. Jupyter Notebook 실행 및 기본 폴더 설정
 - Jupyter Notebook 실행
    - [Windows + S] > Jupyter Notebook
 - Jupyter Notebook 기본 폴더 설정
    - Jupyter Notebook 설치 경로 > 실행 파일 우클릭
    - "%USERPROFILE%/" 경로 변경
```

<br/>

## 파이썬 기본 사용법

파이썬에서 들여쓰기는 가독성을 높일 뿐 아니라 계층을 구분하는 기능을 한다.  

 - `파이썬 기본 연산`
    - 출력 함수: print()
    - 비교 연산: '<', '>', '==', '>=' 등
    - 계산 연산: '+', '*', '/', '%'(나머지), '//'(몫)
    - 입력 함수: input()
```py
# 출력 함수
print('Hello World!')

# 비교 연산
print(1 < 2) # True
print(1 > 2) # False
print(1 == 2) # False
print(1 >= 2) # False

# 계산 연산
print(7 + 3) # 10
print(7 * 3) # 21
print(7 / 3) # 2.6666667
print(7 % 3) # 1 (나머지)
print(7 // 3) # 2 (몫)

# 입력 함수
print("이름을 입력하세요:")
my_name = input()
print("당신의 이름은 " + my_name + " 입니다.")

```

<br/>

 - `변수와 자료형`
    - 변수
        - 다른 언어와 다르게 변수를 만들 때 자료형 타입을 지정하지 않는다. 파이썬은 변수에 저장된 값을 스스로 판단하여 자료형의 타입을 지정한다.
        - 변수명은 '_' 혹은 영문자로 시작해야 한다. 숫자로 시작할 수 없다.
        - 변수명에 공백이 포함될 수 없고, 특수문자도 사용할 수 없다.
        - 변수명은 대소문자를 구분한다.
    - 기본 자료형
        - 숫자형(number): 수학적 연산에 활용하는 자료형. 정수(int), 실수(float), 복소수(complex)
        - 문자열(string): 문자를 나타내는 자료형. 문자열(str)
        - 불린형(boolean): 명제를 참(True)/거짓(False)을 구분하는 자료형. 불리언(bool)
    - 인덱싱, 슬라이싱
        - 인덱싱
            - 원하는 자료에 번호를 매김
        - 슬라이싱
            - 자료를 구분하기 위해 자름
            - 변수[시작인덱스:끝인덱스:증가폭]
```py
# 변수
Name = "Tom"
nAme = "Paul"
NAME = "Ben"
print(Name) # Tom

# 기본 자료형
a = 'tom' # type(a): str
b = 1 # type(b): int
c = 10.123 # type(c): float
d = True # type(d): bool

# 인덱싱, 슬라이싱
language = 'python'
print(language[0]) # p
print(language[1]) # y
print(language[-1]) # n
print(language[-3]) # h

language = 'python'
print(language[::]) # python
print(language[0:6:1]) # python: 0번째 인덱스 부터 5번째 인덱스까지, 1씩 증가
print(language[3:5:]) # ho: 3번째 인덱스 부터 4번째 인덱스까지
print(lnaguage[::2]) # pto: 0번쨰 인덱스 부터 마지막 인덱스까지, 2씩 증가
print(language[::-1]) # nohtyp

```

<br/>

 - `자료구조`
    - 리스트
        - 리스트는 대괄호 '[]'로 표현한다.
        - 요소의 중복이 가능하고 순서가 있다.
        - 리스트 요소 추가: append()
        - 리스트 요소 삭제: del 변수명[인덱스]
        - 리스트 요소 개수 확인: len(변수명)
        - 리스트 요소 변경: 변수명[인덱스] = 값
    - 딕셔너리
        - 딕셔너리는 중괄호 '{}'로 표현한다. 중괄호 안에 요소를 ,(쉼표)로 구분한다.
        - Key와 Value 쌍으로 저장된다. (Map, JSON 구조와 비슷하다.)
        - Key는 정수(int), 실수(float), 문자열(str), 불린(bool), 튜플(tuple), frozenset 등 불변객체만 사용할 수 있다.
        - 요소 추가: 변수명[키] = 값
        - 값 변경: 변수명[키] = 값
        - 요소 삭제: del 변수명[키]
        - 키 추출: keys()
        - 값 추출: values()
        - 요소 추출: items()
    - range
        - range는 범위를 표현하는 시퀀스 자료형(순서가 있는 자료형)이다.
        - range(시작숫자, 종료숫자, 간격)
```py
# 리스트
word1 = 'apple'
word2 = 'banana'
my_list = ['grape', word1, word2, 'orange']

print(my_list[0]) # grape
print(my_list[1]) # apple
print(my_list[-1]) # orange

print(my_list[:2:]) # ['grape', 'apple']: 0번인덱스 부터 1번 인덱스까지
print(my_list[2::]) # ['banana', 'orange']: 2번인덱스 부터 마지막 인덱스까지

my_list.append('cherry') # 마지막 순서에 cherry 추가
del my_list[4] # 4번쨰 인덱스(cherry) 삭제
print(len(my_list)) # 리스트 크기: 4
my_list[3] = 'cherry' # 3번쨰 인덱스(orange)를 cherry로 변경

# 딕셔너리
alien = {
    'color': 'green',
    'points': 5
}
alien['name'] = '에일리언'

list(alien.keys()) # ['color', 'points', 'name']
list(alien.values()) # 'green', 5, '에일리언'
list(alien.items()) # {('color', 'green'), ('points', 5), ('name', '에일리언')}

# range
my_range = range(5) # range(0,5)
list(my_range) # [0, 1, 2, 3, 4]

my_range = range(2, 5)
list(my_range) # [2, 3, 4]

my_range = range(1, 7, 2)
list(my_range) # [1, 3, 5]
```

<br/>

 - `조건문/반복문`
    - if문
    - for문
    - while문
    - break: 루프를 일괄 종료시킨다.
    - continue: 현재 루프을 종료시키고, 다음 루프를 실행한다.
```py
# if문
num = 10
if a < 10:
    print('a가 10보다 작다.')
elif a > 10:
    print('a가 10보다 크다.')
else:
    print('a는 10이다.')

# for문
numbers = [0, 1, 2, 3, 4]
for number in numbers: # 0 ~ 4 반복
    print(number)

for number in range(5): # 0 ~ 4 반복
    print(number)

my_dict = {
    "a": "apple",
    "b": "banana",
    "g": "grape",
    "k": "kiwi",
    "o": "orange"
}
for fruit in my_dict: # 모든 key 출력
    print(fruit)

for fruit in my_dict.values(): # 모든 Value 출력
    print(fruit)

for fruit in my_dict.items(): # 모든 Key, Value 출력
    print(fruit)

# while문
number = 1
while number < 10:
    print(number)
    number = number + 1
```

<br/>

 - `함수 및 예외 처리`
    - 함수 정의
        - def 함수명(매개변수): .. return 값
    - 예외 처리
        - try-except 구문
```py
# 함수 정의
def plus(a, b):
    return a + b

plus(1, 2)

# 예외 처리
try:
    a = 1 / 0
except:
    print("오류 발생")
```

<br/>

 - `라이브러리, 패키지, 모듈, 클래스, 함수`
```
라이브러리/패키지 > 모듈 > 클래스 > 함수, 변수

라이브러리안에 여러 개의 모듈이 존재한다.
모듈안에 여러 개의 클래스가 존재한다.
클래스 안에 여러 개의 함수와 변수가 존재한다.
```

<br/>

 - `절대경로/상대경로`
```
현재 경로 설정 방법
 - 현재경로: 'text.xlsx'
 - 하위경로: '폴더명/test.xlsx'
 - 상위경로: '../폴더명/test.xlsx'

절대 경로 설정 방법
 - 'c:/usrs/abcd/test.xlsx'
```

<br/>

## 업무 유형별 파이썬 활용 기술

 - `인터넷 자동화`
    - 활용 기술: request, bs4, selenium 라이브러리, 외부 API 활용
    - 인터넷 제어: 인터넷에 활동하는 동작(클릭, 이미지 찾기, 타이핑) 등을 자동화한다.
    - 인터넷 정보 획득: 인터넷에 보이는 많은 정보를 내 컴퓨터로 저장한다.
 - `데이터 편집 자동화`
    - 활용 기술: pandas, openpyxl, os 라이브러리
    - 데이터 관리: 내가 만든 데이터나 타인이 만든 데이터를 언제든지 원하는 형태로 불러올 수 있도록 자동화한다.
    - 데이터 편집: 엑셀의 행/열을 바꾸거나 약간의 편집을 통해서 다양한 엑셀 데이터를 합치거나 하는 작업을 자동화한다.
 - `개인화된 자료`
    - 활용 기술: python-pptx, openpyxl, python-docs, PIL, moviepy 라이브러리 등
    - PPT, EXCEL, WORD, 사진 등: 다수에게 임명장을 주거나, 매주 입사하는 직원에게 명함을 만들어서 제공하는 경우 등 동일한 자료에서 일부 내용의 변경을 반복하는 작업을 자동화한다.
 - `커뮤니케이션`
    - 활용 기술: smtplib, win32com 라이브러리, 외부 API 활용
    - 메일, 문자: 메일로 어떤 내용을 전달하거나 다른 사람이 보낸 메일을 확인하고 저장하는 것, 수신인의 정보(이름/직급/이메일)만 일부 변경하여 단체 문자를 발송하는 것을 자동화한다.
 - `물리적인 자동화(단순 반복 업무)`
    - 활용 기술: pyautogui, win32com, winsound 라이브러리 등
    - 마우스 제어, 키보드 제어, 화면 제어: 엑셀 매크로처럼 미세한 마우스 조정이나 키보드 제어가 필요한 업무를 자동화할 수 있다.
 - `협업 및 기타`
    - 활용 기술: pyinstaller, google spreadsheet 등
    - 보고서 자동 작성: 비정기적으로 보고서를 올리기도 하지만, 경우에 따라서 월/주 단위 혹은 매일매일 보고서를 올려야 할 수 있다.
    - ex) 기업 교육 설문 조사
        - 교육 진행
            - 교육 진행은 사람이 진행해야 한다.
        - 설문 진행
            - 설문 진행에 대해서는 지정된 시간에 문자로 보내는 일을 자동화한다.
        - 설문 데이터 다운로드
            - 크롤링을 이용해 설문 데이터를 자동화한다.
        - 데이터 분석 후 결과 보고서 작성
            - 정례화된 결과 보고서라면 파이썬의 데이터 처리와 시각화를 이용해 결과를 만든다.
