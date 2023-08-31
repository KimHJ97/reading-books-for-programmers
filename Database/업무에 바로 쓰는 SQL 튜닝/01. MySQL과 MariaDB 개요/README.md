# MySQL과 MariaDB 개요

 - MySQL
    - 1995년 오픈소스로 배포된 무료 DBMS
    - 대용량 데이터와 가용성, 안정성이라는 장점에 힙입어 다양한 용도로 활용되어 온 대표적인 소프트웨어
    - 2010년 오라클에 인수되어 2018년 5월 MySQL 8.0 버전이 배포(상용 버전, 커뮤니티 버전 구분)
    - MySQL 버전 이력: 5.1(2008.11), 5.5(2010.12), 5.6(2013.12), 5.7(2015.10), 8.0(2018.05)
    - https://dev.mysql.com/doc/refman/8.0/en/select.html
 - MariaDB
    - MySQL이 오라클로 인수되고, 개발 지침과 라이센스 정책 변화에 따른 MySQL의 핵심 개발자 주도로 오픈소스 정책을 지향하는 Maria DB 탄생
    - MySQL의 소스 코드에 기반을 두고 개발되어 MySQL과 일부 기능과 수행 메커니즘, 시스템 상태 등 차이가 있지만, SQL 문의 주요 뼈대는 거의 동일
    - MySQL과 MariaDB 버전에 따라 DB 엔진 레벨에서 제공하는 옵티마이저 기능의 차이가 있으므로 DBA라면 이점에 염두해야 한다. (MySQL 5.5와 MariaDB 10.0 까지는 같은 길을 걸었지만, 그 이후 버전부터 독자적으로 바뀜)
    - MariaDB 버전 이력: 5.1(2010.01), 5.2(2010.04), 10.0(2012.11), 10.1(2014.06), 10.2(2016.04), 10.3(2017.04), 10.4(2018.11), 10.5(2019.12), 10.6(2021.04)
    - https://mariadb.com/kb/en/selecting-data/

<br/>

## 현황

 - MySQL은 상용 버전과 무료 버전으로 구분된다.
    - 무료 버전은 GPL 라이선스를 따른다.
    - 상용 버전은 오라클에서 다양한 보안 패치와 개선된 기능을 제공하는 반면, GPL 라이선스를 사용하는 무료 버전은 MySQL 소스 코드 공개의 부담이 있으며 제약된 기능과 서비스만 사용 가능하다.
 - MariaDB는 GPL v2 라이선스를 따른다.
    - 완전한 오픈소스 소프트웨어로, MariaDB가 포함된 소프트웨어를 고객에게 판매하는 등의 영리 목적 활동 외에는 소스 코드 공개 의무가 없다.
 - 오픈소스 DB 엔진 영향력 (Most Popular Open Source Databases)
    - 2021년 기준 MySQL이 58%로 1위이고, MariaDB가 5%로 5위

<br/>

## 상용 RDBMS와의 차이점

__`구조적 차이`__

RDBMS를 실제 서비스에 도입할 때는 장애 예방 효과 또는 장애 발생 시 가용성을 기대하며 이중화 구조로 구축한다. 나아가 삼중화 이상의 다중화 구조로 구축하여 가용성 수준을 더 높일 수 있다.  

이때, 기본적으로 데이터가 저장되는 스토리지의 구조 측면에서 큰 차이를 보인다. 오라클 DB는 통합된 스토리지 하나를 공유하여 사용하는 방식이지만, MySQL은 물리적인 DB 서버마다 독립적으로 스토리지를 할당하여 구성한다.
 - 오라클은 공유 스토리지를 사용하므로 사용자가 어느 DB 서버에 접속하여 SQL 문을 수행하더라도 같은 결과를 출력한다.
 - MySQL은 독립적인 스토리지 할당에 기반을 두는 만큼 이중화를 위한 클러스터나 복제 구성으로 운영하더라도 보통은 마스터-슬레이브 구조가 대부분이다. 이때, 마스터 노드는 쓰기/읽기 처리를 모두 수행할 수 있고 슬레이브 노드는 읽기 처리만 수행할 수 있다.
 - 즉, MySQL의 경우 쿼리 튜닝을 할 때 구축된 DB 서버의 구조를 충분히 이해하고 적합한 서버(Master 또는 Slave)에 접근하여 쿼리 튜닝을 수행해야 정확한 결과를 확인할 수 있다. 다만, 각 DB 서버의 운영체제 설정, 할당된 스토리지 크기, 시스템 변수, 하드웨어 사양 등이 같을 때는 마스터 노드 중심으로 쿼리 튜닝을 진행해도 무방하다.

<br/>

__`지원 기능 차이`__

MySQL과 오라클 DB에서 제공하는 조인 알고리즘의 기능에는 차이가 있다. MySQL은 대부분 중첩 루프 조인 방식으로 조인을 수행하는 한편, 오라클에서는 중첩 루프 조인 방식뿐만 아니라 정렬 병합 조인과 해시 조인 방식도 제공한다. MySQL 8.0.18 버전에서도 제약적으로 해시 조인을 제공하지만 여전히 대부분의 조인은 중첩 루프 조인으로 풀린다.  
 - MySQL은 쥻 중첩 루프 조인 알고리즘만으로 풀리고, 필요한 DBMS를 설정해 사용할 수 있고, 상대적으로 낮은 메모리 사용으로 저사양 PC에서 손쉽게 설치 및 개발을 할 수 있다.

<br/>

__`SQL 구문 차이`__

오라클 함수명이나 문법이 MySQL과 조금 다르다.  

 - Null 대체
    - MySQL: IFNULL(컬럼, '대체값')
    - Oracle: NVL(컬럼, '대체값')
 - 페이징 처리
    - MySQL: LIMIT 숫자
    - Oracle: ROWNUM <= 숫자
 - 현재 날짜
    - MySQL: NOW()
    - Oracle: SYSDATE
 - 조건문
    - MySQL: IF(조건식, '참값', '거짓값')
    - Oracle: DECODE(컬럼, '비교값', '참값', '거짓값')
 - 날짜 형식 형변환
    - MySQL: DATE_FORMAT()
    - Oracle: TO_CHAR()
 - 자동 증갓값
    - MySQL, Oracle 모두 각자 시퀀스라는 오브젝트를 활용할 수 있다.
    - MySQL: nextval(시퀀스명)
    - Oracle: 시퀀스명.nextval
 - 문자 결합
    - MySQL: CONCAT(문자열, 문자열)
    - Oracle: 문자열 || 문자열, CONCAT(문자열, 문자열)
 - 문자 추출
    - MySQL: SUBSTRING(컬럼, 시작위치, 추출문자개수)
    - Oracle: SUBSTR(컬럼, 시작위치, 추출문자개수)

```SQL
-- Null 대체
SELECT IFNULL(col1, 'N/A') col1 FROM tab;
SELECT NVL(col1, 'N/A') col1 FROM tab;

-- 페이징 처리
SELECT col1 FROM tab LIMIT 5;
SELECT col1 FROM tab WHERE ROWNUM <= 5;

-- 현재 날짜
SELECT NOW() AS date;
SELECT SYSDATE AS date FROM dual;

-- 조건문
SELECT IF(col1='A', 'apple', '-') AS col1 FROM tab;
SELECT DECODE(col1, 'A', 'apple', '-') AS col1 FROM tab;

-- 날짜 형식 형변환
SELECT DATE_FORMAT(NOW(), '%Y%m%d %H%i%s') AS date;
SELECT TO_CHAR(SYSDATE, 'YYYYMMDD HH24MISS') AS date FROM dual;

-- 시퀀스 생성
CREATE SEQUENCE MARIA_SEQ_SAMPLE
INCREMENT BY 1
START WITH 1
MINVALUE 1
MAXVALUE 99999999999
CYCLE
CACHE;
SELECT NEXTVAL(시퀀스명);

CREATE SEQUENCE ORACLE_SEQ_SAMPLE
INCREMENT BY 1
START WITH 1
MINVALUE 1
MAXVALUE 99999999999
CYCLE
CACHE;
SELECT 시퀀스명.NEXTVAL FROM dual;

-- 문자 결합
SELECT CONCAT('A', 'B') TEXT;
SELECT 'A' || 'B' AS TEXT FROM dual;

-- 문자 추출
SELECT SUBSTRING('ABCDE', 2, 3) AS sub_string; -- 'BCD'
SELECT SUBSTR('ABCDE', 2, 3) AS sub_string FROM dual; -- 'BCD'
```

<br/>

__`MySQL과 MariaDB 튜닝의 중요성`__

최근 클라우드 환경과의 접목으로 한 대의 기본 노드와 다수의 복제본 노드, 여러 개의 마스터 노드 구조 등 다양한 방식의 안정적인 아키텍처를 서비스에 활용한다.  
MySQL 내부를 보면 기능적인 제약사항이 있따. 그것은 대다수의 SQL 문이 중첩 루프 조인 알고리즘으로 수행되고, 상용 DBMS와는 다르게 수행된 쿼리 결과가 메모리에 적재되는 캐시 기능에 한계가 있으므로 일반적인 쿼리 작성 및 튜닝이 통하지 않을 수 있다.  
따라서, DBMS가 제공하는 기능을 자세히 알아야 하며, 제공되는 실행 계획 정보를 해석하고 문제점을 인지하거나 대응할 수 있는 능력을 갖춘 뒤 쿼리 튜닝을 진행해야 한다.  
