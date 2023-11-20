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
