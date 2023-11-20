# 06장. 커뮤니케이션 자동화(메일&문자)

## 커뮤니케이션 자동화가 필요한 상황

업무 커뮤니케이션에서 반복 수행되는 일들이 많다.  
예를 들어, 주기적으로 메일을 발송, 메일 내용을 문자로 대신 전송하는 경우가 있다.  
그중에서도 특정 수신자만 봐야 할 메일을 작성하는 경우에는 수신자를 일일히 지정하는 등 반복 작업이 많이 발생한다.  

소중한 시간을 지키기 위해 기업용 메일/문자 발송 관련 유료 서비스를 이용할 수도 있지만, 파이썬 코딩으로 이메일/문자/카카오톡/노션/슬랙 등 다양한 형태의 도구들 모두 자동화가 가능하다.  

<br/>

## 사전 내용

 - `이메일 작동 원리`

이메일은 SMTP(간이 전자 우편 전송 프로토콜)라는 방식을 활용하여 메일이 전송된다.  
발신인에서 수신인으로 메일이 바로 전달되는 게 아니라 하나의 서버에서 서버로 메일이 전달되는 방식이다.  
때문에, 메일을 보내기 위해서는 나의 이메일이 있는 메일 서버의 정보가 필요하다.  

<br/>

 - `Gmail 활용을 위한 사전 세팅`
    - Gmail 설정
        - 지메일 로그인
        - [메일 설정] 클릭 (모든 설정 클릭)
        - 전달 및 POP/IMAP 클릭
        - [Imap 액세스 > IMAP 사용] 클릭
        - 변경 사항 저장
    - Google 서비스 2단계 인증 설정
        - 구글 계정 보안 페이지에 접속
        - 웹 비밀번호 클릭
        - 생성된 앱 비밀번호 저장
        - google에 로그인 탭에서 2단계 인증
        - 앱 비밀번호 생성 (앱(메일) 선택, 기기 선택)

<br/>

## 기초 사용법

 - `메일 발송(Gmail)`
```py
import getpass
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

my_mail = input('나의 발신 이메일:')
your_mail = input('수신 이메일:')
pw = getpass.getpass('Gmail 앱 비밀번호:')
server = 'smtp.gmail.com'
port = 587

msg = MIMEMultipart("alternative")
msg["Subject"] = "안녕하세요."
msg["From"] = my_mail
msg["To"] = your_mail
msg_html = f"""
<p>
    .. HTML 내용
    입사를 축하드립니다.\n
    명함 보내드립니다.
</p>
"""

msg.attach(
    MIMEText(
        msg_html, 'html'
    )
)

# 명함 첨부
attachment = open('명함/홍길동 차장.jpg', 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disopsition', 'attachment;filename=' + 'wordcloud_news2.png')
msg.attach(part)

# 메일 전송
s = smtplib.SMTP(server, port)
s.ehlo()
s.starttls()
s.login(my_mail, pw)
s.sendmail(my_mail, your_mail, msg.as_string())
s.quit()

```

<br/>

## 메일 발송 자동화 실습

 - `메일로 명함 파일 및 수료증 파일 전송`
    - 텍스트 파일 HTML 변환 사이트: https://wordtohtml.net/
    - 코드 설계
        - Chapter 5에서 만든 수천 개의 명함 파일을 파이썬으로 불러오기
        - 이메일 주소 불러오기
        - 파일 이름을 넣으면 이메일 반환되게 하기
        - 텍스트 파일을 HTML로 변환
        - Gmail을 활용한 메일 전송
```py
import getpass
import os
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

mail_address = input('Gmail 계정을 입력주세요: ')
mail_pwd = getpass.getpass('Gmail 보안 패스워드를 입력해주세요: ')
server = 'smtp.gmail.com'
port = 587



# 1. 이메일 주소 불러오기
df = pd.read_csv('명함제작용data.csv')
df2 = df[['이름', '직위', '전화번호', '이메일']]

# 2. 파일 이름을 넣으면 이메일이 반환되게 하기
file_list = os.listdir("명함_1/") # 02-1234-5678.jpg 형식으로 저장되어 있다고 가정
for fileName in file_list[:5]:
    file_nj = fileName.replace('.jpg', '')
    name = df2[df2['전화번호'] == file_nj]['이름'].iloc[0] # 데이터프레임에서 전화번호와 파일명이 동일한 행의 이름 조회
    email = df2[df2['전화번호'] == file_nj]['이메일'].iloc[0]

    msg_html = f"""
    <p>
        .. HTML 내용
        {name}님 입사를 축하드립니다.\n
        명함 보내드립니다.
    </p>
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f'{name}님 명함 제작이 완료되었습니다.'
    msg["From"] = mail_address
    msg["To"] = email
    msg.attach(
        MIMEText(
            msg_html,
            'html'
        )
    )

    # 명함 첨부
    attachment = open(f'명함_1/{fileName}', 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disopsition', 'attachment;filename=' + 'wordcloud_news2.png')
    msg.attach(part)

    # 메일 전송
    s = smtplib.SMTP(server, port)
    s.ehlo()
    s.starttls()
    s.login(mail_address, mail_pwd)
    s.sendmail(mail_address, email, msg.as_string())
    s.quit()

```
