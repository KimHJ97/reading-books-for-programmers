# 12. DB를 사용하면서 발생 가능한 문제점들

* JDBC API
* DB Connection Pool
* DataSource
* PreparedStatement
* Close 순서
* Close 방법 예시
* AutoClosable
* 그 외 JDBC 팁

## 개요

```
Java 기반 애플리케이션의 성능을 진단해보면, 애플리케이션의 응답 속도를 지연시키는 대부분의 요인은 DB 쿼리 수행 시간과 결과를 처리하는 시간이다.
해당 책에서는 애플리케이션에 초점을 두어 DB 쿼리에 대한 튜닝을 다루지 않았지만, Java단에서 DB 사용함에 있어 많이 하는 실수를 최소화하기 위한 내용을 알려준다.
```


## 1. JDBC API

Java에서는 DataBase 접근을 위한 클래스가 아닌 인터페이스가 제공된다.  
즉, JDK의 API에 있는 java.sql 인터페이스를 각 DB 벤더에서 상황에 맞게 구현하도록 되어있다.  
때문에, 같은 인터페이스라고 해도, 각 DB 벤더에 따라서 처리 속도나 내부 처리 방식이 다를 수 있다.  

```Java
try {
    // 1. 드라이버 로드
    Class.forName("oracle.jdbc.driver.OracleDriver");

    // 2. DB 서버 정보를 통해 Connection을 연결한다.
    Connection con = DriverManager.getConnection("jdbc:oracle:thin:..", "id", "pw");

    // 3. 연결된 Connection으로 PreparedStatement 객체를 만든다.
    PreparedStatement ps = con.prepareStatement("SELECT .. WHERE id=?");
    ps.setString(1, id);
    ResultSet rs = ps.executeQuery();
    ..
} catch (ClassNotFoundException e) {
    ..
} catch(SQLException e) {
    ..
} finally {
    rs.close();
    ps.close();
    con.close();
}
```

위에 코드에서 가장 느린 부분은 Connection 객체를 얻는 부분이다.  
WAS에서 DB에 연결하기 위한 Connection에는 시간이 소요된다.  
만약, DB가 다른 장비에 있다면 네트워크 통신 시간은 더 소요된다.  
* DB 커넥션을 얻기 위해서는 3 Way Handshake와 같은 TCP/IP 연결을 위한 네트워크 동작이 발생한다.


## 2. DB Connection Pool

DB Connection을 얻기 위해서는 네트워크 부담이 발생하며 시간이 오래걸린다.
이러한 문제를 해결하기 위해 나온 것이 DB Connection Pool이다.  
매번 커넥션을 얻고 사용 후 반환하는 것은 복잡하고 시간이 많이 소요된다.  
Connection Pool 이라는 커넥션 보관함에 미리 여러 개의 커넥션을 만들어놓고, 필요할때 Pool에 보관된 커넥션을 참조로 가져다 사용한다.

* JSP와 서블릿 기술이 나오면서 많은 Connection Pool 기술이 등장했다. 하지만, 초기에 많이 등장한 Connection Pool 기술들이 실제 검증되지 않은 소스가 많았기 떄문에, 많은 사이트에서 문제점이 발견되었다.
* 현재는 WAS 자체에서 Connection Pool을 제공하고, DataSource를 사용하여 JNDI로 호출해 쓸 수 있기 때문에 출처가 불분명한 Connection Pool 보다는 안정되고 검증된 WAS에서 제공하는 DB Connection Pool 이나 DataSource를 사용하는 것이 권장된다.


## 3. DataSource

DB Connection Pool은 자바 표준이 없다.  
즉, 커넥션 보관함에 대해서 어떻게 관리하고 최적화하는지는 밴더사에서 관리한다.  
때문에, 커넥션 풀을 관리하는 구현체를 바꾸게 되면 사용하는 코드도 변경해야 한다.  
Java에서는 이러한 문제를 해결하기 위해 DataSource라는 커넥션을 획득하는 방법을 추상화한 인터페이스를 제공한다.  
단순히 커넥션을 얻는 기능을 제공한다.
* 즉, 보관함(pool)에 커넥션 상태 관리는 커넥션 풀 밴더사가 구현한다.


## 4. PreparedStatement

JDBC API로 DB 접근 제어를 위해 Statement, PreparedStatement, CallableStatement가 제공된다.
Statement는 매번 쿼리를 수행할 때마다 쿼리 문장 분석, 컴파일, 실행을 거치게 된다.
PreparedStatement는 처음 한 번만 쿼리 문장 분석, 컴파일, 실행을 거치고 캐시에 담아서 재사용하기 떄문에 동일한 쿼리를 반복적으로 수행하면 DB에 부하를 줄이고 성능이 더 좋게 된다.
CallableStatement는 PL/SQL을 처리하기 위해 사용된다.

```
executeQuery(): select 관련 쿼리를 수행한다.
executeUpdate(): select 관련 쿼리를 제외한 DML(INSERT, UPDATE, DELETE 등) 및 DDL(CREATE) 쿼리를 수행한다.

ResultSet 인터페이스: 쿼리를 수행한 결과가 담긴다. 여러 건의 데이터가 넘어올 경우 next() 메소드를 사용하여 데이터의 커서를 다음으로 옮겨 처리한다. first() 혹은 last() 메소드로 커서를 처음이나 마지막으로 이동할 수 있다.
```


## 5. Close 순서

Connection, Statement, ResultSet 등은 close() 메소드를 사용하여 닫아야 한다.  
일반적으로 Connection -> Statement -> ResultSet 순으로 얻어오고, 닫을 떄는 역순으로 ResultSet -> Statement -> Connection 순서로 닫는다.

ResultSet 객체가 닫히는 경우  
1. close() 메소드 호출하는 경우
2. GC의 대상이 되어 GC되는 경우
3. 관련된 Statement 객체의 close() 메소드가 호출되는 경우

Statement 객체가 닫히는 경우  
1. close() 메소드를 호출하는 경우
2. GC의 대상이 되어 GC되는 경우

Connection 객체가 닫히는 경우  
1. close() 메소드를 호출하는 경우
2. GC의 대상이 되어 GC되는 경우
3. 치명적인 에러가 발생하는 경우

Close 결론  
1. close()를 직접 호출하는 이유는 GC의 대상이 되어 자동으로 닫힐 수 있지만, 그 전에 DB와 JDBC 리소스를 해제하기 위함이다. 0.00001초라도 빨리 닫으면, 그만큼 DB 서버의 부담을 줄일 수 있다.
2. Statement와 ResultSet은 다른 메소드에 의해서 닫히지 않는다. 때문에, 반드시 직접 close() 메소드를 호출하여 닫는다.


## 6. Close 방법 예시

### 6-1. 안좋은 예시
```Java
// 1. NULL 처리
// NULL로 치환은 직접적으로 닫히지 않는다. NULL로 치환하면 GC의 대상이 되어 닫힐 수는 있지만, 언제 GC될지 모르기 떄문에 좋지 않다.
try {
    ..
    rs = null;
    ps = null;
    con = null;
}

// 2. try 내부에서 Close
// 만약, 내부 로직에서 예외가 발생하면 어떤 객체도 close 되지 않는다.
try {
    ..
    rs.close();
    ps.close();
    con.close();
}

// 3. finally 안에서 Close (예외 처리 X)
// 
try {
    ..
} catch(Exception e) {
    ..
} finally {
    rs.close();
    ps.close();
    con.close();
}
```

### 6-2. 정상적인 방법
가장 좋은 방법은 아닐지라도, 가장 정상적인 방법으로는 close() 마다 예외 처리를 해주는 것이다.
* 가장 좋은 방법은 DB와 관련된 처리를 담당하는 관리 클래스를 만드는 것이다. Connection 객체도 JNDI로 찾아서 사용하는 DataSource를 이용하여 얻고, ServiceLocator 패턴까지 적용한다.
```Java
try {
    ..
} catch(Exception e) {
    ..
} finally {
    try{rs.close()} catch(Exception e){}
    try{ps.close()} catch(Exception e){}
    try{con.close()} catch(Exception e){}
}
```


## 7. AutoClosable

JDK7 부터 java.lang 패키지에 AutoCloseable 인터페이스가 제공된다.
또한, JDK7 부터 try-with-resources 라는 구문이 제공된다.
해당 구문을통해 close() 메소드를 호출하는 대상이 AutoCloseable 인터페이스를 구현한 것이라면 자동으로 Close 된다.

```Java
// Before(JDK 6): finally에서 직접 Close
FileReader reader = new FileReader(new File("파일명"));
BufferedReader br = new BufferedReader(reader);
try {
    ..
} finally {
    if (br != null) br.close();
}

// After: try-with-resources 구문 (finally 및 close 생략 가능)
FileReader reader = new FileReader(new File("파일명"));
try(
    BufferedReader br = new BufferedReader(reader);
) {
    ..
}

```


## 8. 그 외 JDBC 팁

```
1. setAutoCommit() 메소드는 필요할 떄만 사용하자
여러 개의 쿼리를 동시에 작업할 때 성능에 영향을 주게 되므로 자제하자.

2. 배치성 작업은 executeBatch() 메소드를 사용하자
addBatch() 메소드를 사용하여 쿼리를 지정하고,
executeBatch() 메소드를 사용하여 쿼리를 수행한다.
여러 개의 쿼리를 한 번에 수행할 수 있어 JDBC 호출 횟수가 감소하여 성능이 좋아진다.

3. setFetchSize() 메소드를 사용하여 데이터를 더 빠르게 가져오자
가져오는 데이터의 수가 정해져 있을 경우 setFetchSize() 메소드로 원하는 개수를 정의할 수 있다.
다만, 너무 많은 건수를 지정하면 서버에 부하가 올 수 있으니 적절하게 사용해야 한다.
```