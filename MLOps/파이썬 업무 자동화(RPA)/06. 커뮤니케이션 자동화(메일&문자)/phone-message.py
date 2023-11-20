import pandas as pd
import twilio
import getpass
import os
from twilio.rest import Client

# 문자 전송 함수
def send_msg(account_sid, auth_token, from_phone, to_phone, message_contents):
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                        body = message_contents,
                        from_ = from_phone,
                        to = to_phone
                    )
    print(message.sid)

# 계정 SID, 인증 토큰, 발신 전화번호 입력받기
account_sid = getpass.getpass("account_sid:")
auth_token = getpass.getpass("auth_token:")
from_pnb = getpass.getpass("from_pnb:")

# 1. CSV 파일에서 정보 조회
df = pd.read_csv('문자전송용data.csv')

# 2. 데이터 프레임에서 원하는 정보 가공
for unit in range(len(df)):
    df_unit = df.loc[unit]
    phone_number = df_unit[5] # 휴대폰 번호
    to_gnb = "+82" + str(phone_number)
    name = df_unit[2] # 이름
    rank = df_unit[3] # 직급
    company = df_unit[0] # 회사명
    team = df_unit[4] # 소속팀
    email = df_unit[8] # 이메일
    message = f"반갑습니다.{name} {rank}님. {company} {team} 소속으로 일하시느라 고생 많으셨습니다. 얼마 전 {email}로 메일을 보내드렸는데, 아직 회신을 받지 못하여 문자로 문의드립니다. 답변 부탁드립니다."

    send_msg(account_sid, auth_token, from_pnb, to_gnb, message)
