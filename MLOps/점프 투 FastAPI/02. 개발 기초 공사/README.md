# 02장. 개발 기초 공사

 - APIRouter를 이용해 엔드포인트를 관리한다.
 - SQLAlchemy를 이용해 데이터베이스를 제어한다.
 - 게시판에 질문 목록과 상세 조회 기능을 만든다.

<br/>

## FastAPI 프로젝트 구조

 - `폴더 구조`
    - main.py: app 객체는 FastAPI의 핵심 객체로 main.py는 FastAPI 프로젝트의 전체적인 환경 설정하는 파일이다.
    - database.py: database.py는 데이터베이스와 관련된 설정을 하는 파일이다.
    - models.py: ORM을 지원하는 SQLAlchemy를 사용하여 모델 기반으로 데이터베이스를 처리한다. models.py 파일은 모델 클래스를 정의한다.
    - domain 디렉토리: 각 도메인별로 관련된 작업을 처리하도록 한다. 예를 들어, domain/question에는 router, crud, schema 파일이 존재할 것이다.
        - 라우터 파일: URL와 API의 전체적인 동작 관리
        - 데이터베이스 처리 파일: CRUD 처리를 관리
        - 입출력 관리 파일: 입력 데이터와 출력 데이터의 스팩 정의 및 검증
```
├─ main.py
├─ database.py
├─ models.py
├─ domain
│   ├─ answer
│   ├─ question
│   └─ user
└─ frontend
```

<br/>

## 모델로 데이터베이스 관리하기

 - `ORM 라이브러리 설치`

```bash
(venv) pip install sqlalchemy
```

<br/>

 - `설정 파일 추가하기`
    - FastAPI에 ORM을 적용하려면 데이터베이스 설정이 필요하다.
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

```

<br/>

 - `모델 만들기`
    - 질문 모델
        - id: 질문 데이터의 고유 번호
        - subject: 질문 제목
        - content: 질문 내용
        - create_date: 질문 작성일시
    - 답변 모델
        - id: 답변 데이터의 고유 번호
        - question_id: 질문 데이터의 고유 번호
        - content: 답변 내용
        - create_date: 답변 작성일시
    - 모델 클래스는 앞서 database.py에서 정의한 Base 클래스를 상속하여 만들어야 한다.
    - relationship의 첫 번째 파라미터는 참조할 모델명이고 두 번째 backref 파라미터는 역참조 설정이다.
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

# 질문 모델
class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

# 답변 모델
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")
```

<br/>

 - `모델을 이용해 테이블 자동 생성하기`
    - 모델을 구상하고 생성했으므로 SQLAlchemy의 alembic을 이용해 데이터베이스 테이블을 생성한다.
    - alembic은 SQLAlchemy로 작성한 모델을 기반으로 데이터베이스를 쉽게 관리할 수 있게 도와주는 도구이다.
    - 초기화를 진행하면 디렉토리 하위에 migrations라는 디렉터리와 alembic.ini 파일이 생성된다. migrations 디렉터리는 alembic 도구를 사용할 때 생성되는 리비전 파일들을 저장하는 용도로 사용되고 alembic.ini 파일은 alembic의 환경설정 파일이다.
```bash
# alembic 설치
(venv) pip install alembic

# alembic 초기화
(venv) alembic init migrations
```

<br/>

 - `alembic.ini`
    - alembic이 사용할 데이터베이스의 접속주소를 설정한다.
```python
# (... 생략 ...)
sqlalchemy.url = sqlite:///./myapi.db
# (... 생략 ...)
```

<br/>

 - `migrations/env.py`
    - migrations 디렉터리의 env.py를 수정한다.
```python
# (... 생략 ...)
import models
# (... 생략 ...)
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = models.Base.metadata
# (... 생략 ...)
```

<br/>

 - `리비전 파일 생성하기`
    - 리비전 파일에는 테이블을 생성 또는 변경하는 실행문들이 들어 있다.
    - migrations/versions 디렉터리에 fed28bf52b05_.py와 같은 리비전 파일이 생성된다. 리비전(revision)이란 생성된 fed28bf52b05_.py 파일에서 .py 확장자를 제외한 fed28bf52b05_와 같은 버전 번호를 가리킨다. 리비전은 alembic revision --autogenerate 명령을 수행할 때 무작위로 만들어진다.
```bash
(venv) alembic revision --autogenerate
```

<br/>

 - `리비전 파일 실행하기`
    - alembic revision --autogenerate 명령으로 만들어진 리비전 파일을 alembic upgrade head 명령으로 실행한다.
    - 이 과정에서 데이터베이스에 모델에 정의한 question과 answer라는 이름의 테이블이 생성된다.
```bash
(venv) alembic upgrade head
```

<br/>

## 모델로 데이터 처리하기

 - `모델 사용 예시`
```python
# Question 모델 객체 만들기
from models import Question, Answer
from datetime import datetime
q = Question(subject='pybo가 무엇인가요?', content='pybo에 대해서 알고 싶습니다.', create_date=datetime.now())

# Question 모델 저장하기
from database import SessionLocal
db = SessionLocal()
db.add(q)
db.commit()

q = Question(subject='FastAPI 모델 질문입니다.', content='id는 자동으로 생성되나요?', create_date=datetime.now())
db.add(q)
db.commit()

# 데이터 조회하기
db.query(Question).all() # 전체 데이터 조회
db.query(Question).filter(Question.id==1).all() # 첫 번째 질문만 조회
db.query(Question).get(1) # id로 조회
db.query(Question).filter(Question.subject.like('%FastAPI%')).all() # like 조건 조회

# 데이터 수정하기
q = db.query(Question).get(2)
q.subject = 'FastAPI Model Question'
db.commit()

# 데이터 삭제하기
q = db.query(Question).get(1)
db.delete(q)
db.commit()


# 답변 데이터 저장하기
from datetime import datetime
from models import Question, Answer
from database import SessionLocal
db = SessionLocal()
q = db.query(Question).get(2)
a = Answer(question=q, content='네 자동으로 생성됩니다.', create_date=datetime.now())
db.add(a)
db.commit()

# 연관 관계 모델 찾기
a.question # Answer 모델의 question 속성으로 답변에 연결된 질문을 조회
q.answers # Question 모델의 answers 속성으로 질문에 연결된 답변을 조회
```
