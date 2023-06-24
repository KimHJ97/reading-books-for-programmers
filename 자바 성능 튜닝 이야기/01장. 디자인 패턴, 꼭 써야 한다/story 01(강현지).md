# story 01

# MVC 모델

Model, View, Controller의 약자

모델 역할, 뷰 역할, 컨트롤러 역할을 하는 클래스를 각각 만들어서 개발하는 모델

View : 사용자가 결과를 보거나 입력할 수 있는 화면

Controller : 뷰와 모델의 연결자. 뷰에서 받은 이벤트를 모델로 연결하는 역할

Model : 뷰에서 입력된 내용을 저장, 관리, 수정하는 역할

3티어로 되어있는 JSP 모델은 주로 모델1과 모델2를 사용

- 3 Tier Architecture
    
    > 3 Tier Architecture : 어떤 플랫폼을 3 계층으로 나누어 별도의 논리적/물리적인 장치에 구축 및 운영하는 형태
    > 
    
    ### 2 Tier
    
    **클라이언트 ↔ 서버**
    
    - 클라이언트가 직접 서버의 DB에 접속하여 자원을 활용
    
    ### 3 Tier
    
    **클라이언트 ↔ 웹/애플리케이션 서버 ↔ DB**
    

## JSP 모델1

JSP에서 자바 빈을 호출하고 데이터베이스에서 정보를 조회, 등록, 수정, 삭제 업무를 한 후 결과를 브라우저로 보내주는 방식

- 간단하게 개발 가능
- 개발 후 프로세스 변경이 생길 경우 수정 어려움. 즉, 유지보수 어려움
- 화면과 비즈니스 모델의 분업화가 어려움 → 개발자의 역량에 따라 코드가 많이 달라질 수 있음
- 컨트롤러가 없기 때문에 MVC 모델이라고 하기 어려움

## JSP 모델2

JSP 모델1의 단점을 해결하기 위해 나온 모델

모델1과의 가장 큰 차이점은 모델1은 JSP로 요청을 직접 하지만 모델2에서는 서블릿으로 요청함

서블릿이 컨트롤러 역할

# J2EE 패턴

디자인 패턴이란?

시스템을 만들기 위해 전체 중 일부 의미 있는 클래스들을 묶은 각각의 집합

### 패턴 특징

**Interceptin Filter**

요청 타입에 따라 다른 처리를 하기 위한 패턴

**Front Controller**

요청 전후에 처리하기 위한 컨트롤러를 지정하는 패턴

************************************View Helper************************************

프레젠테이션 로직과 상관 없는 비즈니스 로직을 헬퍼로 지정하는 패턴

**Composite View**

최소 단위의 하위 컴폰넌트를 분리하여 화면을 구성하는 패턴

**Service to Worker** 

Front Controller와 View Helper 사이에 디스패처를 두어 조합하는 패턴

********************************************Dispatcher View********************************************

Front Controller와 View Helper로 디스패처 컴포넌트를 형성

뷰 처리가 종료될 때까지 다른 활동을 지연한다는 점이 Service to Worker 패턴과의 차이점

******Business Delegate******

비즈니스 서비스 접근을 캡슐화 하는 패턴

**Service Locator**

서비스와 컴포넌트 검색을 쉽게 하는 패턴

**Session Facade**

비즈니스 티어 컴포넌트를 캡슐화하고, 원격 클라이언트에서 접근할 수 있는 서비스를 제공하는 패턴

**Composite Entity**

로컬 엔티티 빈과 POJO를 이용하여 큰 단위의 엔티티 객체를 구현

**Transfer Object**

일명 Value Object 패턴이라고 많이 알려져 있음

데이터를 전송하기 위힌 객체에 대한 패턴

**Transfer Object Assembler**

하나의 Transfer Object로 모든 타입 데이터를 처리할 수 없으므로, 여러 Transfer Object를 조합하거나 변형한 객체를 생성하여 사용하는 패턴

**Value List Handler**

데이터 조회를 처리하고, 결과를 임시 저장하며, 결과 집합을 검색하여 필요한 항목을 선택하는 역할 수행

**Data Access Object**

일명 DAO라고 많이 알려져 있음

DB에 접근을 전담하는 클래스를 추상화하고 캡슐화

**Service Activator**

비동기적 호출을 처리하기 위한 패턴

- Service to Worker vs Dispatcher View
    
    Dispatcher View 패턴은 Helper 클래스를 직접 컨트롤하지 않음
    

<aside>
💡 J2EE 패턴 중 성능과 가장 밀접한 패턴은 Service Locator 패턴이다.
성능에 직접적으로 많은 영향을 미치지는 않지만, 애플리케이션 개발 시 반드시 사용해야 하는 패턴은 Transfer Object 패턴이다.

</aside>

## Transfer Object 패턴

데이터를 전송하기 위한 객체에 대한 패턴

Transfer Object를 만들어 하나의 객체에 여러 타입의 값을 전달하는 일을 수행

```java
public class EmployeeTO implements Serializable {
	// 필드
	private String empName;
	private String empID;

	// 생성자
	public EmployeeTO() {
		super();
	}
	public EmployeeTO(String empName, String empID) {
		super();
		this.empName = empName;
		this.empID = empID;
	}

	// getter, setter
	public String getEmpName() {}
	public void setEmpName(String empName) {}
	public String getEmpID() {}
	public void setEmpID(String empID) {}

	// toString
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append("empName=").append(empName).append("empID=").append(empID);
		return sb.toString();
	}
}
```

- Transfer Object를 사용할 때 필드를 private으로 지정해서 getter, setter 메서드를 만들지 않고 public으로 지정하는게 성능상으로는 더 빠름
    - 하지만 정보 은닉과 필드의 값을 아무나 수정 못하게 하기 위해 getter, setter 메서드를 만드는게 일반적
- Transfer Object를 생성할 때는 반드시 toString() 메서드를 구현하기 바람
    - 이 메서드를 구현하지 않고 객체의 toString() 메서드를 수행하면 알 수 없는 값을 리턴

<aside>
💡 Serializable 인터페이스를 구현하면 객체를 직렬화 할 수 있다. 즉, 서버 사이의 데이터 전송이 가능하다. 
원격지 서버에 데이터를 전송하거나, 파일로 객체를 저장할 경우 이 인터페이스를 구현해야 한다.

</aside>

## Service Locator 패턴

```java
public class ServiceLocator {
	private InitialContext ic;
	private Map cache;
	private static ServiceLocator me;

	static {
		me = new ServiceLocator();
	}
	private ServiceLocator() {
		cache = Collections.synchronizedMap(new HashMap());
	}
	public InitialContext getInitialContext() throws Exception {
		try {
			if(ic == null) {
				ic = new InitialContext();
			}
		} catch (Exception e) {
			throw e;
		}
		return ic;
	}
	public static ServiceLocator getInstance() {
		 return me;
	}
	public EJBLocalHome getLocalHome (String jndiHomeName) throws Exception {
  EJBLoclaHome home = null;
  try {
   if (cache.containsKey(jndiHomeName)) {
    home = (EJBLocalHome)cache.get(jndiHomeName);
   } else {
    home = (EJBLocalHome)getInitialContext().lookup(jndiHomeName);
    cache.put(jndiHomeName, home);
   }
  } catch (Exception e) {
   throw new Exception(e.getMessage());
  }
  return home;
 }
}
```

EJB의 EJB Home 객체나 DB의 DataSource를 찾을 때 소요되는 응답 속도를 감소시키기 위해 사용

<aside>
💡 EJB란?
Enterprise Java Beans의 약자로 기업 환경의 시스템을 구현하기 위한 서버측 컴포넌트 모델이다. 즉, EJB는 애플리케이션의 업무 로직을 가지고 있는 서버 애플리케이션이다.

</aside>

소스 내용

cache라는 Map 객체에 home 객체를 찾은 결과를 보관하고 있다가, 누군가 그 객체를 필요로 할 때 메모리에서 찾아서 제공하도록 되어있음.

만약 해당 객체가 cache라는 맵에 없으면 메모리에서 찾음