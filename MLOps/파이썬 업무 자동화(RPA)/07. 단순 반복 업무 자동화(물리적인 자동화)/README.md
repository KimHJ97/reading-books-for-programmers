# 07장. 단순 반복 업무 자동화

파이썬을 통해서 업무 자동화를 진행하다 보면 종종 파이썬으로 접근하기 어려운 상황을 만날 수 있다.  
예를 들어, 인터넷으로 구성된 인트라넷이 아닌 누군가 만들어 놓은 GUI 프로그램을 이용할 경우 Selenium으로 정보를 획득하거나 다루기 어렵다.  
또한, 회사 보안으로 인해 파이썬으로 파일을 열 수 없는 경우도 있다.  

이러한경우 일부 역할(마우스 클릭, 스크린샷 등)은 파이썬으로 해결할 수 있다.  
 - 일부 역할
    - 시각: 이미지 스크린샷(pyautogui) + 이미지 텍스트 추출
    - 촉각: 키보드 제어(pyautoguui)
    - 촉각: 마우스 제어(pyautogui)
    - 청각: 알림음 라이브러리(winsound)
 - 사내 보안 환경에서 파일 다루기
    - 보안 프로그램으로 인해 pandas에서 엑셀 파일을 열 수 없는 경우가 있다.
    - 이때, 물리 자동화를 활용해 엑셀을 직접 컨트롤하여 엑셀의 데이터를 파이썬의 pandas로 올리는 방법을 사용한다.

<br/>

## 사전 내용

PyAutoGUI 라이브러리를 활용해 타이핑, 마우스 클릭, 화면 캡처를 이용한 이미지 위치 찾기 등을 할 수 있다.  
win32com으로 프로그램을 자동으로 열람할 수 있다.  
winsound로 컴퓨터에서 어떤 상황이 되었을 때 소리를 내도록 할 수 있다.  

 - `라이브러리 설치`
```py
!pip install pyautogui
!pip install pywin32 == 227
!pip install winsound
```

<br/>

 - `PyAutoGUI`
    - 공식 문서: https://pyautogui.readthedocs.io/en/latest/
```py
import pyautogui as pg

## 1. 마우스 컨트롤
# 마우스 위치 확인
pag.position()

# 마우스 이동
pag.moveTo(x = 180, y = 348)

# 마우스 드래그
pag.dragTo(508, 600, 1, button = 'left') # 1초간 마우스 좌클릭을 한 상태로 지정한 위치까지 드래그

# 마우스 클릭
pag.click(x = 249, y = 51) # 지정한 위치를 클릭(기본 좌클릭)


## 2. 키보드 컨트롤
# 문자열 입력
pag.click(x = 249, y = 51) # 임의의 위치 클릭
pag.typewrite('Hello World!', interval = 0.1)

# 여러키 동시 입력
pag.click(x = 406, y = 402) # 임의의 위치 클릭
pag.hotkey("ctrl", "v") # 붙여넣기: Ctrl + V


## 3. 화면 프로그램 컨트롤
pag.screenshot('test1.png', region = (1, 20, 100, 100)) # x좌표, y좌표, 가로길이, 세로길이를 지정하고 test1.png 파일로 저장
pag.locateOnScreen('test1.png') # 이미지 위치 좌표 확인

```

 - `win32com`
```py
import win32com.client
import os
import pandas as pd

# 엑셀 프로그램 실행
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True # 열린 엑셀 프로그램이 보이게 설정

# 기존 엑셀 파일 열고, 활성화된 엑셀 시트 바인딩
ab_ads = os.getcwd()
wb = excel.Workbooks.Open(f"{ab_ads}/1.xlsx")
ws = wb.ActiveSheet

# 엑셀 시트의 데이터 가져오기
df = pd.DataFrame(ws.UsedRange())
```

 - `winsound`
    - 공식 문서: https://docs.python.org/ko/3/library/winsound.html
```py
import winsound

# 특정 조건에서 알림음 내기
winsound.Beep(1000, 5) # 5초간 beep음 울리기
```

<br/>

## 물리 자동화 실습

 - `Nox 모바일 애뮬레이터를 열고 애플리케이션 실행`
```py
import pyautogui as pag
import time

# 1. Nox 플레이어 실행
st = 1
time.sleep(st)
pag.press('super')
time.sleep(st)
pag.typewrite('nox')
time.sleep(st)
pag.press('enter')
time.sleep(30) # 프로그램 로딩 시간


# 2. 윈도우 시작 버튼을 누르고 Nox 프로그램 실행
# 클릭을 원하는 위치의 이미지 확보
nox_x = int(pag.locateOnScreen('nox.png').left)
nox_y = int(pag.locateOnScreen('nox.png').height)

pag.moveTo(nox_x, nox_y) # 좌측 최상단 클릭
time.sleep(st)

try:
    pag.dragTo(0, 0, 1, button = 'left') # (0,0)으로 드래그
except:
    print(1)

pag.FAILSAFE = False # 오류 발생시 (0,0)으로 마우스를 이동시키는가? 아니오
pag.mouseUp() # 마우스 클릭 해제


# 3. Nox 프로그램의 이미지를 확인하여 위치를 체크하고 그 위치를 (0,0)으로 이동
time.sleep(st)
pag.click(x = 414, y = 378)


# 4. 세부 자동화
# 4-1. 내 모임 클릭 (346, 996)
time.sleep(st)
pag.click(348, 996)

# 4-2. 가입한 모임 클릭 (138, 361)
time.sleep(st)
pag.click(138, 361)

# 4-3. 채팅창 클릭 (51, 993)
time.sleep(st)
pag.click(51, 993)

# 4-4. 원하는 인사말 쓰기
time.sleep(st)
pag.typewrite('noce to meet you.')

# 4-5. 원하는 인사말 전송 (521, 991)
time.sleep(st)
pag.click(521, 991)

# 4-6. 정보 탭 클릭 (66, 144)
time.sleep(st)
pag.click(66, 144)

# 4-7. 클래스 만들기 클릭 (278, 880)
time.sleep(st)
pag.click(278, 880)

# ..
```
