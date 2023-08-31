# Stroy 1. 디자인 패턴 꼭 써야 한다.

디자인 패턴

시스템을 만들기 위해서 전체 중 일부 의미 있는 클래스들을 묶은 각각의 집합.

반복되는 의미 있는 집합을 정의하고 이름을 지정해서 누가 이야기하더라도 동일한 의미의 패턴이 되도록 만들어 놓은 것이다.

성능 개선은 물론 개발과 유지보수의 편의에 도움을 준다.

디자인패턴

- Intercepting Filter 패턴: 요청 타입에 따라 다른 처리를 하기 위한 패턴
- Front Controller 패턴: 요청 전후에 처리하기 위한 컨트롤러를 지정하는 패턴
- View Helper 패턴: 프레젠테이션 로직과 상관 없는 비즈니스 로직을 헬퍼로 지정하는 패턴
- Composite View 패턴: 최소 단위의 하위 컴포넌트를 분리하여 화면을 구성하는 패턴
- Service to Worker 패턴: Front Controller와 View Helper 사이에 디스패처를 두어 조합하는 패턴
- Dispatcher View 패턴: Front Controller와 View Helper로 디스패처 컴포넌트를 형성한다. 뷰 처리가 종료될 때까지 다른 활동을 지연한다는 점이 Service to Worker 패턴과 다르다.
- Business Delegate 패턴: 비즈니스 서비스 접근을 캡슐화하는 패턴
- Service Locator 패턴: 서비스와 컴포넌트 검색을 쉽게 하는 패턴
- Session Facade 패턴: 비즈니스 티어 컴포넌트를 캡슐화하고, 원격 클라이언트에서 접근할 수 있는 서비스를 제공하는 패턴
- Composite Entity 패턴: 로컬 엔티티 빈과 POJO를 이용하여 큰 단위의 엔티티 객체를 구현
- Transfer Object 패턴: 일명 Value Object 패턴이라고 많이 알려져 있다. 데이터를 전송하기 위한 객체에 대한 패턴
- Transfer Object Assembler 패턴: 하나의 Transfer Object로 모든 타입 데이터를 처리할 수 없으므로, 여러 Transfer Object를 조합하거나 변형한 객체를 생성하여 사용하는 패턴
- Value List Handler 패턴: 데이터 조회를 처리하고, 결과를 임시 저장하며, 결과 집합을 검색하여 필요한 항목을 선택하는 역할
- Data Access Object 패턴: 일명 DAO라고 많이 알려져 있다. DB에 접근을 전담하는 클래스를 추상화하고 캡슐화한다.
- Service Activator 패턴: 비동기적 호출을 처리하기 위한 패턴

적어도 Business Delegate, Session Facade, Data Access Object, Service Locator, Transfer Object 패턴은 알아야 하고 Service Locator, Transfer Object 패턴은 성능과 관련이 있다.

**Transfer Object 패턴**

데이터를 전송하기 위한 객체에 대한 패턴

```jsx
public class EmployeeTO implements Serializable {
  private String empName;
  private String empID;
  private String empPhone;
  
  public EmployeeTO() {
    super();
  }
  
  public EmployeeTO(String empName, String empID, String empPhone) {
    this.empName = empName;
    this.empID = empID;
    this.empPhone = empPhone;
  }

  public String getEmpName() {
    if(empName==null) return "";
    else return empName;
  }

  public void setEmpName(String empName) {
    this.empName = empName;
  }

  public String getEmpID() {
    return empID;
  }

  public void setEmpID(String empID) {
    this.empID = empID;
  }

  public String getEmpPhone() {
    return empPhone;
  }

  public void setEmpPhone(String empPhone) {
    this.empPhone = empPhone;
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("empName=").append(empName).append("empID=").append(empID)
        .append( " empPhone=").append(empPhone);
    return sb.toString();
  }
}
```

Tranfer Object를 사용할 때 필드를 private로 지정해서 getter() 메서드와 setter() 메서드를 만들어야 할지,

아니면 public으로 지정해서 메서드를 만들지 않을지에 대한 정답은 없지만, 

성능상으로 따져볼 때 getter()와 setter()를 만들지 않는 것이 더 빠르다. 

하지만 정보를 은닉하고, 모든 필드의 값들을 아무나 마음대로 수정할 수 없게 하려면 위의 코드와 같이 각 getter(), setter() 메서드를 작성하는 것이 일반적이다.

Transfer Object를 생성할 때는 반드시 toString() 메서드를 구현해야 한다. 이 메서드를 구현하지 않고 toString() 메서드를 수행하면 com.perf.pattern.EmployEETo@c1716처럼 알 수 없는 값을 리턴한다.

Serializable을 구현하면 객체를 직렬화할 수 있다. 다시 말해 서버 사이의 데이터 전송이 가능해진다. 그러므로 원격지 서버에 데이터를 전송하거나, 파일로 객체를 저장할 경우에는 이 인터페이스를 구현해야 한다.

그렇다면 이 Transfer Obejct를 사용한다고 성능이 좋아질까?

엄청난 성능 개선 효과가 발생하는 것은 아니다. 하지만 하나의 객체에 결과 값을 담아올 수 있어 두 번, 세 번씩 요청을 하는 일이 발생하는 것을 줄여주므로, 이 패턴을 사용하기를 권장한다.

**Service Locator 패턴**

```jsx
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
      if (ic == null) {
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
  // ... 지면상 생략
}
```

Service Locator 패턴은 누군가 그 객체를 필요로 할 때 인스턴스를 반환하는 한다. 

위의 소스를 간단히 보면, cache라는 Map 객체에 home 객체를 찾은 결과를 보관하고 있다가, 누군가 그 객체를 필요로 할 때 메모리에서 찾아서 제공하도록 되어 있다. 만약 해당 객체가 cache라는 맵에 없으면 메모리에서 찾는다. 미리 객체를 생성하는 게 아니라 객체가 필요할때 생성하므로 성능에 영향이 있다고 볼 수 있다.

Service Locator 패턴은 예전에 많이 사용되었던 EJB의 Home 객체와 DB의 DataSource를 찾을 때(lookup 할 때) 소요되는 응답 속도를 감소시키기 위해서 사용된다. 

자바 기반의 시스템을 분석 설계하고 개발하면서 패턴을 모른다면 반쪽 분석 설계자나 개발자라고 할 수 있다.

프레임워크를 사용할 때도 마찬가지이다. 프레임워크를 만든 사람의 사상과 프레임워크의 구조, 기능을 정학히 알고 있어야 제대로 프레임워크를 활용할 수 있다.

---

참고 : DI와 서비스 로케이터 

https://incheol-jung.gitbook.io/docs/study/undefined/di