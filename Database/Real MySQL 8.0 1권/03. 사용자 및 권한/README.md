# 사용자 및 권한

## 1. 사용자 식별

MySQL의 사용자는 사용자 계정뿐 아니라 사용자의 접속 지점도 계정의 일부가 된다.  
만약, 모든 외부 컴퓨터에서 접속이 가능한 사용자 계정을 생성하고 싶다면 사용자 계정의 호스트 부분을 % 문자로 대체하면 된다.  
사용자 계정 식별에서 주의해야 할 점은 서로 동일한 아이디가 있을 때 MySQL 서버는 접속 범위가 작은 것을 우선 순위로 한다.  

```
# scott 아이디로 '127.0.0.1' 주소만 접속 가능
'scott'@'127.0.0.1'

# scott 아이디로 모든 호스트에서 접속 가능
'scott'@'%'
```

<br/>

## 2. 사용자 계정 관리

MySQL 8.0부터 계정은 SYSTEM_USER 권한에 따라 시스템 계쩡과 일반 계정으로 구분된다. 시스템 계정은 데이터베이스 서버 관리자를 위한 계정이며, 일반 계정은 응용 프로그램이나 개발자를 위한 계정으로 생각하면 된다.  

 - __시스템 계정 권한__
    - 계정 관리(계정 생성 및 삭제, 그리고 계정의 권한 부여 및 제거)
    - 다른 세션 또는 그 세션에서 실행 중인 쿼리를 강제 종료
    - 스토어드 프로그램 생성 시 DEFINER를 타 사용자로 설정
 - __MySQL 내장 계정__
    - 'mysql.sys'@'localhost': MySQL 8.0부터 기본으로 내장된 sys 스키마의 객체(뷰, 함수, 프로시저)들의 definer로 사용되는 계정
    - 'mysql.session'@'localhost': MySQL 플러그인이 서버로 접근할 떄 사용되는 계정
    - 'mysql.infoschema'@'localhost': information_schema에 정의된 뷰의 DEFINER로 사용되는 계정
```bash
mysql> SELECT user, host, account_locked FROM mysql.user WHERE user LIKE 'mysql.%';
```

<br/>

### 계정 생성

MySQL 5.7 버전까지 GRANT 명령으로 권한 부여와 계정 생성이 가능했지만, MySQL 8.0 부터는 계정 생성은 CREATE USER 명령으로, 권한 부여는 GRANT 명령으로 구분해서 사용하도록 바뀌었다.  

 - __CREATE USER 명령어__
    - 계정의 인증 방식과 비밀번호
    - 비밀번호 관련 옵션(유효기간, 이력 개수, 재사용 불가 기간)
    - 기본 역할(Role)
    - SSL 옵션
    - 계정 잠금 여부
```sql
CREATE USER 'user'@'%'
    IDENTIFIED WITH 'mysql_native_password' BY 'password'
    REQUIRE NONE
    PASSWORD EXPIRE INTERVAL 30 DAY
    ACCOUNT UNLOCK
    PASSWORD HISTORY DEFAULT
    PASSWORD REUSE INTERVAL DEFAULT
    PASSWORD REQUIRE CURRENT DEFAULT;
```

<br/>

 - `IDENTIFIED WITH`
    - 사용자의 인증 방식과 비밀번호를 설정한다.
    - IDENTIFIED WITH 뒤에는 반드시 인증 방식을 명시해야 하는데, MySQL 서버의 기본 인증 방식을 사용하는 경우 IDENTIFIED BY 'password' 형식으로 명시해야 한다.
    - MySQL 5.7 버전까지 Native Authentication이 기본 인증 방식으로 사용됐지만, MySQL 8.0 버전부터는 Caching SHA-2 Authentication이 기본 인증으로 바뀌었다.
    - __Native Pluggable Authentication__: MySQL 5.8 버전까지 기본으로 사용되던 방식, 단순히 비밀번호에 대한 해시(SHA-1) 값을 저장해두고, 일치하는지 비교
    - __Caching SHA-2 Pluggable Authentication__: MySQL 5.6 버전에 도입되고 MySQL 8.0 버전에 보완된 인증 방식으로, 암호화 해시값 생성을 위해 SHA-2 알고리즘을 사용한다. 해당 인증 방식을 사용하려면 SSL/TLS 또는 RSA 키페어를 반드시 사용해야 한다. 클라이언트에서 접속할 때 SSL 옵션을 활성화해야 한다.
```sql
-- MySQL 8.0에서 Native Authentication을 기본 인증 방식으로 설정하고자 한다면 MySQL의 설정을 변경해야 한다.
SET GLOBAL default_authentication_plugin="mysql_native_password"
```

<br/>

 - `REQUIRE`
    - MySQL 서버에 접속할 떄 암호화된 SSL/TLS 채널을 사용할지 여부를 설정한다. 만약, 별도로 설정하지 않으면 비암호화 채널로 연결하게 된다.

<br/>

 - `PASSWORD EXPIRE`
    - 비밀번호의 유효 기간을 설정한다.
    - 별도로 명시하지 않으면 default_password_lifetime 시스템 변수에 저장된 기간으로 유효 기간이 설정된다.
```
PASSWORD EXPIRE: 계정 생성과 동시에 비밀번호의 만료 처리
PASSWORD EXPIRE NEVER: 계정 비밀번호의 만료 기간 없음
PASSWORD EXPIRE DEFAULT: default_password_lifetime 시스템 변수에 저장된 기간으로 비밀번호의 유효 기간을 설정
PASSWORD EXPIRE INTERVAL n DAY: 비밀번호의 유효 기간을 오늘부터 n일자로 설정
```

<br/>

 - `PASSWORD HISTORY`
    - 한 번 사용했던 비밀번호를 재사용하지 못하게 설정하는 옵션
```
 - PASSWORD HISTORY DEFAULT
password_history 시스템 변수에 저장된 개수만큼 비밀번호의 이력을 저장하며, 
저장된 이력에 남아있는 비밀번호는 재사용할 수 없다.

 - PASSWORD HISTORY n
비밀번호의 이력을 최근 n개까지만 저장하며, 
저장된 이력에 남아있는 비밀번호는 재사용할 수 없다.
```

<br/>

 - `PASSWORD REUSE INTERVAL`
    - 한 번 사용했던 비밀번호의 재사용 금지 기간을 설정한다. 별도로 명시하지 않으면 password_reuse_interval 시스템 변수에 저장된 기간으로 설정한다.
```
 - PASSWORD REUSE INTERVAL DEFAULT
password_reuse_interval 변수에 저장된 기간으로 설정

 - PASSWORD REUSE INTERVAL n DAY
n일자 이후에 비밀번호를 재사용할 수 있게 설정
```

<br/>

 - `PASSWORD REQUIRE`
    - 비밀번호가 만료되어 새로운 비밀번호로 변경할 때 현재 비밀번호를 필요로 할지 말지를 결정하는 옵션
    - 별도로 명시되지 않으면 password_require_current 시스템 변수의 값으로 설정된다.
```
 - PASSWORD REQUIRE CURRENT
비밀번호를 변경할 때 현재 비밀번호를 먼저 입력하도록 설정

 - PASSWORD REQUIRE OPTIONAL
비밀번호를 변경할 때 현재 비밀번호를 입력하지 않아도 되도록 설정

 - PASSWORD REQUIRE DEFAULT
password_require_current 시스템 변수의 값으로 설정
```

<br/>

 - `ACCOUNT LOCK / UNLOCK`
    - 계정 생성 시 또는 ALTER USER 명령을 사용해 계정 정보를 변경할 때 계정을 사용하지 못하게 잠글지 여부를 결정
```
 - ACCOUNT LOCK
계정을 사용하지 못하게 잠금

 - ACCOUNT UNLOCK
잠긴 계정을 다시 사용 가능 상태로 잠금 해제
```

<br/>

## 4. 비밀번호 관리

### 고수준 비밀번호

MySQL 서버의 비밀번호는 유효기간이나 이력 관리를 통한 재사용 금지 기능뿐만 아니라 비밀번호를 쉽게 유추할 수 있는 단어들이 사용되지 않게 글자의 조합을 강제하거나 금칙어를 설정하는 기능도 있다.  
MySQL 서버에서 비밀번호의 유효성 체크 규칙을 적용하기 위해서는 validate_password 컴포넌트를 설치해야 한다. validate_password 컴포넌트는 MySQL 서버 프로그램에 내장되어 있어 INSTALL COMPONENT 명령의 file:// 부분에 별도의 파일 경로를 지정하지 않아도 된다.  

```bash
## validate_password 컴포넌트 설치
mysql> INSTALL COMPONENT 'file://component_validate_password';

## 설치된 컴포넌트 확인
mysql> SELECT * FROM mysql.component;

## 컴포넌트가 제공하는 시스템 변수 확인
mysql> SHOW GLOBAL VARIABLES LIKE 'validate_password%';
```

<br/>

비밀번호의 길이는 validate_password.length 시스템 변수에 설정된 길이 이상의 비밀번호가 사용됐는지 검증하며, 숫자와 대소문자, 특수문자는 validate_password.mixed_case_count와 validate_password.number_count, validate_password.special_char_count 시스템 변수에 설정된 글자 수 이상을 포함하고 있는지 검증한다. 금칙어는 validate_password.dictionary_file 시스템 변수에 설정된 사전 파일에 명시된 단어를 포함하고 있는지를 검증한다.  

```bash
## 금칙어 적용: 'STRONG'으로 설정되어야만 금칙어가 적용된다.
mysql> SET GLOBAL validate_password.dictionary_file='파일명';
mysql> SET GLOBAL validate_password.policy='STRONG';
```

<br/>

### 이중 비밀번호

데이터베이스 계정의 비밀번호는 서비스가 실행 중인 상태에서 변경이 불가능했다. 보안을 위해 주기적으로 변경해야 하지만, 서비스를 멈추지 않고서는 비밀번호를 변경하는 것이 불가능했다.  
이러한 문제점을 해결하기 위해 MySQL 8.0 부터는 계정의 비밀번호로 2개의 값을 동시에 사용할 수 있는 기능을 추가했다.  

```bash
# root 계정의 프라이머리 비밀번호 변경
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'old_password';

# root 계정의 이전 비밀번호를 세컨더리 비밀번호로 설정하고,
# 새롭게 설정한 비밀번호를 프라이머리 비밀번호로 설정
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password' RETAIN CURRENT PASSWORD

# 세컨더리 비밀번호 삭제
mysql> ALTER USER 'root'@'localhost' DISCARD OLD PASSWORD;
```

<br/>

### 권한

MySQL 5.7 버전까지 권한은 글로벌 권한과 객체 단위의 권한으로 구분되었다.  
MySQL 8.0 버전부터는 MySQL 5.7 버전의 구너한에 동적 권한이 더 추가되었다.  

 - __글로벌 권한__
    - FILE, CREATE ROLE, CREATE TABLESPACE, CREATE USER, DROP ROLE, PROCESS, PROXY, RELOAD, REPLICATION CLIENT, REPLICATION SLAVE, SHOW DATABASES, SHUTDOWN, SUPER, USAGE
 - __객체 권한__
    - EVENT, LOCK TABLES, REFERENCES, CREATE, GRANT OPTION, DROP, ALTER ROUTINE, CREATE ROUTINE, EXECUTE, ALTER, CREATE TEMPORARY TABLES, DELETE, INDEX, TRIGGER, INSERT, SELECT, UPDATE, CREATE VIEW, SHOW VIEW
 - __동적 권한__
    - INNODB_REDO_LOG_ARCHIVE, RESOURCE_GROUP_ADMIN, RESOURCE_GROUP_USER, BINLOG_ADMIN, BINLOG_ENCRYPTION_ADMIN, BACKUP_ADMIN, CLONE_ADMIN, GROUP_REPLICATION_ADMIN, REPLICATION_APPLIER, REPLICATION_SLAVE_ADMIN, CONNECTION_ADMIN 등
```sql
-- 사용자에게 권한 부여: GRANT
GRANT privilega_list ON db.table TO 'user'@'host';

-- 글로벌 권한
-- 글로벌 권한은 특정 DB나 테이블에 부여될 수 없기 떄문에
-- 글로벌 권한을 부여할 때 GRAN 명령의 ON 절에는 항상 *.*을 사용하게 된다.
GRANT SUPER ON *.* TO 'user'@'localhost';

-- DB 권한
-- DB 권한은 특정 DB에 대해서만 권한을 부여하거나 서버에 존재하는 모든 DB에 대해 권한을 부여할 수 있다.
-- ON 절에 *.*이나 employees.* 모두 사용할 수 있다.
GRANT EVENT ON *.* TO 'user'@'localhost';
GRANT EVENT ON employees.* TO 'user'@'localhost';

-- 테이블 권한
GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'user'@'localhost'; -- 서버 모든 DB에 대한 권한 부여
GRANT SELECT, INSERT, UPDATE, DELETE ON employees.* TO 'user'@'localhost'; -- 특정 DB의 오브젝트
GRANT SELECT, INSERT, UPDATE, DELETE ON employees.department TO 'user'@'localhost'; -- 특정 DB의 특정 테이블

-- 테이블의 특정 컬럼 권한(컬럼 단위 권한)
-- ※ 컬럼 단위의 접근 권한이 필요한 경우 GRANT 명령보다는 허용하고자 하는 컬럼만 별도의 뷰를 만들어 사용하는 방법도 있다.
-- ※ 뷰도 하나의 테이블로 인식되어 뷰를 만들어 두면 뷰의 컬럼에 대해 권한을 체크하지 않고 뷰 자체에 대한 권한만 체크한다.
GRANT SELECT, INSERT, UPDATE(dept_name) ON employees.department TO 'user'@'localhost';
```

<br/>

 - `DB 권한 테이블`
   - 각 계정이나 권한에 부여된 권한이나 역할을 확인하기 위해서는 SHOW GRANTS 명령을 사용할 수도 있지만, MySQL DB 관련 테이블을 통해 표 형태로 확인할 수 있다.
```
★ 정적 권한
 - mysql.user: 계정 정보&계정이나 역할에 부여된 글로벌 권한
 - mysql.db: 계쩡이나 역할에 DB 단위로 부여된 권한
 - mysql.tables_priv: 계정이나 역할에 테이블 단위로 부여된 권한
 - mysql.columns_priv: 계정이나 역할에 컬럼 단위로 부여된 권한
 - mysql.procs_priv: 계정이나 역할에 스토어드 프로그램 단위로 부여된 권한

★ 동적 권한
 - mysql.global_grants: 계정이나 역할에 부여되는 동적 글로벌 권한
```

<br/>

## 5. 역할(Role)

MySQL 8.0 버전부터는 권한을 묶어서 역할을 사용할 수 있다.  

 - `예시`
   - CREATE ROLE 명령어로 역할을 정의한다.
   - GRANT 명령으로 각 역할에 대해 권한을 부여한다.
   - GRANT 명령으로 만들어진 역할을 계정에 부여할 수 있다.
   - 계정이 역할을 활성화하기 위해서는 SET ROLE 명령을 수행해야 한다.
      - 기본적으로 MySQL 서버는 역할이 자동으로 비활성화되도록 설정되어 있다.
      - 때문에, SET ROLE을 통해 역할을 활성화하더라도 재로그인하면 초기화가 된다.
      - 시스템 변수(activate_all_roles_on_login)을 활성화하면 자동으로 활성화된다.
   - __저장소 테이블__
      - mysql.default_roles: 계정별 기본 역할
      - mysql.role_edges: 역할에 부여된 역할 관계 그래프
```sql
-- 역할 정의
CREATE ROLE role_emp_read, role_emp_write;

-- 역할에 권한 부여
GRANT SELECT ON employees.* TO role_emp_read;
GRANT INSERT, UPDATE, DELETE ON employees.* TO role_emp_write;

-- 계정 생성
CREATE USER reader@'127.0.0.1' IDENTIFIED BY 'querty';
CREATE USER writer@'127.0.0.1' IDENTIFIED BY 'querty';

-- 계정에 역할 부여
GRANT role_emp_read TO reader@'127.0.0.1';
GRANT role_emp_read, role_emp_writer TO writer@'127.0.0.1';

-- 역할 활성화
SET ROLE 'role_emp_read';
SET GLOBAL activate_all_roles_on_login=ON;
```

