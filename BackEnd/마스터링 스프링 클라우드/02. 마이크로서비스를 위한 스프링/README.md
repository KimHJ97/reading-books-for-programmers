# 02장. 마이크로서비스를 위한 스프링

 
## 스프링 부트 소개

스프링 부트는 스프링 설정을 쉽게 적용할 수 있는 스타터 패키지를 제공한다.  
스타터는 프로젝트 의존성에 포함될 수 있는 아티팩트로 애플리케이션에 포함해야 하는 다른 의존성을 제공한다. 이 방식으로 제공된 패키지는 즉시 사용할 수 있어 동작을 위해 별도의 설정을 할 필요가 없다.  
스타터에 포함된 아티팩트는 기본 설정이 있고 속성이나 다른 유형의 스타터로 쉽게 재정의할 수 있다.  

 - spring-boot-starter: 자동 컨피규레이션 지원, 로깅, YAML을 포함하는 핵심 스타터
 - spring-boot-starter-web: RESTful과 스프링 MVC를 포함하는 웹 애플리케이션 개발. 톰캣을 기본 컨테이너로 내장
 - spring-boot-starter-jetty: 기본 내장 서블릿 컨테이너로 제티를 프로젝트에 포함
 - spring-boot-starter-undertow: 기본 내장 서블릿 컨테이너로 언더토우를 프로젝트에 포함
 - spring-boot-starter-tomcat: 내장 서블릿 컨테이너로 톰캣을 프로젝트에 포함
 - spring-boot-starter-actuator: 애플리케이션 모니터링 및 관리 기능을 제공하는 스프링 부트 액추에이터 프로젝트를 포함
 - spring-boot-starter-jdbc: tOMCAT cONNECTION POOL을 포함하는 스프링 jdbc를 포함. 특정 데이터베이스의 드라이버는 직접 제공해야 함
 - spring-boot-starter-data-jpa: JPA 또는 Hibernate를 이용해 관계형 데이터베이스에 상호작용하기 위해 필요한 모든 아티팩트를 포함
 - spring-boot-starter-data-mongodb: 몽고디비와 상호작용하고 로컬 호스트의 몽고에 대한 클라이언트 연결을 초기화하기 위한 모든 아티팩트를 포함
 - spring-boot-starter-security: 프로젝트에 스프링 시큐리티를 포함하고 애플리케이션에 기본 시큐리티를 활성화
 - spring-boot-starter-test: JUnit, 햄크레스트, 모키토와 같은 라이브러리를 활용한 단위 테스트의 생성을 허가
 - spring-boot-starter-amqp: 스프링 AMQP를 프로젝트에 추가하고 기본 AMQP 브로커로서 레빗엠큐를 시작

<br/>

## 스프링 부트를 이용해 애플리케이션 개발하기

스프링 부트를 이용하기 위해서는 부모 의존성을 정의하고, 필요한 스타터 라이브러리를 추가하면 된다.  

 - `의존 라이브러리 설정`
    - 스프링 Web을 추가하면 기본적으로 spring-core, spring-aop, spring-context, 스프링 부트, 내장형 톰캣, 로그백과 Log4j, Slf4j와 같은 로깅 라이브러리, JSON의 직렬화 및 역직렬화에 사용하는 잭슨 라이브러리 등이 포함된다.
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>1.5.7.RELEASE</version>
</parent>
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```
```gradle
plugins {
    id 'org.springframework.boot' version '1.5.7.RELEASE'
}
dependencies {
    compile("org.springframework.boot:spring-boot-starter-web:1.5.7.RELEASE")
}
```

<br/>

## 컨피규레이션 파일 사용자 정의하기

스프링 부트는 편리하게 설정을 관리할 수 있는 메커니즘을 제공한다. 스프링 부트는 'application'으로 시작하는 컨피규레이션 파일을 자동으로 찾는다. 지원하는 파일 타입은 .properties와 .yml이 있다.  
설정 파일명으로 'application-{profile}' 같은 이름을 부여하여 사용자별 설정 파일을 정의할 수 있으며, 그 외에 특정한 이름을 부여하려면 애플리케이션이 시작할 때 spring.config.name 환경 변수를 제공하면 된다. spring.config.location 설정에 콤마로 분리된 설정 디렉토리 경로와 컨피규레이션 파일 경로 목록을 설정할 수도 있다.  

```bash
$ java -jar sample.jar --spring.config.name=example
$ java -jar sample.jar --spring.config.location=classpath:/example.properties
```

<br/>

 - `설정 파일 예시`
    - 로깅 설정을 위해 log4j.xml 또는 logback.xml 등을 설정할 필요가 없다.
```yml
server:  
  port: ${port:2222}

spring:  
  application:
    name: first-service
    
logging:
  pattern:
    console: "%d{HH:mm:ss.SSS} %-5level %logger{36} - %msg%n"
    file: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"
#  level:
#    org.springframework.web: DEBUG
  file: app.log
  
management:
  security:
    enabled: false

# 사용자 정의 속성
name: first-service
my:
  servers:
    - dev.bar.com
    - foo.bar.com
```

<br/>

 - `사용자 정의 속성 주입`
    - 사용자 정의 속성 값을 코드 내에서 사용하기 위해서는 여러가지 주입 방법이 있다.
    - 간단한 속성은 @Value 어노테이션을 통해 주입한다.
    - @ConfigurationProperties 어노테이션을 활용해 좀 더 복잡한 속성을 주입할 수 있다. YAML 파일에 정의된 my.servers 속성의 값 목록은 java.util.List 빈으로 주입된다.
```java
@Component
public class CustomBean {
    @Value("${name}")
    private String name;
    // ..
}

@ConfigurationProperties(prefix="my")
public class Config {
    private List<String> servers = new ArrayList<String>();
    public List<String> getServers() {
        return this.servers;
    }
}
```

<br/>

 - `API 문서화`
    - 스웨거는 RESTful API를 설계하고 빌드하고 문서화하는 데 가장 많이 사용되는 도구이다.
    - 스프링부트와 스웨거2의 통합은 스프링폭스 프로젝트에 구현됐다. 이것은 애플리케이션이 실행될 때 스프링 컨피규레이션, 클래스 구조, 자바 어노테이션을 기반으로 API의 의미를 추론한다.
```xml
<!-- Swagger2 의존성 -->
<dependency>
  <groupId>io.springfox</groupId>
  <artifactId>springfox-swagger2</artifactId>
  <version>2.7.0</version>
</dependency>
<dependency>
  <groupId>io.springfox</groupId>
  <artifactId>springfox-swagger-ui</artifactId>
  <version>2.7.0</version>
</dependency>
```
```java
@SpringBootApplication
@EnableSwagger2 // 스웨거 활성화
public class Application {

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}

	@Bean
	public Docket api() throws IOException, XmlPullParserException {
		MavenXpp3Reader reader = new MavenXpp3Reader();
		Model model = reader.read(new FileReader("pom.xml"));
		ApiInfoBuilder builder = new ApiInfoBuilder()
				.title("Person Service Api Documentation")
				.description("Documentation automatically generated")
				.version(model.getVersion())
				.contact(new Contact("Piotr Mińkowski", "piotrminkowski.wordpress.com", "piotr.minkowski@gmail.com"));
		return new Docket(DocumentationType.SWAGGER_2).select()
				.apis(RequestHandlerSelectors.basePackage("pl.piomin.services.boot.controller"))
				.paths(PathSelectors.any()).build()
				.apiInfo(builder.build());
	}
	
	@Bean
	UiConfiguration uiConfig() {
	    return new UiConfiguration("validatorUrl", "list", "alpha", "schema",
	            UiConfiguration.Constants.DEFAULT_SUBMIT_METHODS, false, true, 60000L);
	}

}
```

<br/>

 - `스프링 부트 액추에이터 기능`
    - 스프링 부트 액추에이터는 애플리케이션을 모니터링하고 상호작용 하기 위한 내장된 수많은 종단점을 제공한다.
      - '/beans': 애플리케이션에 초기화된 모든 스프링 빈의 목록 표시
      - '/env': 스프링의 설정 가능한 환경 속성 목록 표시
      - '/health': 애플리케이션의 상태 정보 표시
      - '/info': 애플리케이션의 임의 정보 표시
      - '/loggers': 애플리케이션의 로거 컨피규레이션 정보 표시
      - '/metrics': 애플리케이션의 메트릭 정보 표시
      - '/trace': 트레이스 정보 표시
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

추가적으로 자신만의 메트릭을 생성해야 하는 경우가 있다. 스프링 부트 액추에이터는 CounterService와 GaugeService라는 두 클래스를 제공한다.  
CounterService는 값의 증가와 감소, 초기화를 위한 메서드를 제공한다. GaugeService는 단순히 현재의 값을 전달한다.  

```java
// PersonCounterService: CounterService를 이용하여 특정 정보를 카운트한다.
@Service
public class PersonCounterService {

	private final CounterService counterService;
	
    @Autowired
    public PersonCounterService(CounterService counterService) {
        this.counterService = counterService;
    }
    
    public void countNewPersons() {
    	this.counterService.increment("services.person.add");
    }
    
    public void countDeletedPersons() {
    	this.counterService.increment("services.person.deleted");
    }
    
}

// PersonController: Person 객체가 추가, 삭제될때 PersonCounterService의 메서드를 호출한다.
@RestController
@RequestMapping("/person")
public class PersonController {

	private List<Person> persons = new ArrayList<>();

	@PostMapping
	public Person add(@RequestBody Person p) {
		p.setId((long) (persons.size()+1));
		persons.add(p);
		counterService.countNewPersons();
		return p;
	}
	
	@DeleteMapping("/{id}")
	public void delete(@RequestParam("id") Long id) {
		List<Person> p = persons.stream().filter(it -> it.getId().equals(id)).collect(Collectors.toList());
		persons.removeAll(p);
		counterService.countDeletedPersons();
	}
}
```

<br/>

 - `개발자 도구`
    - 스프링 부트는 개발제에게 유용한 도구를 제공한다. devtools 라이브러리는 클래스 경로상의 파일이 변경되면 애플리케이션이 변경을 감지하여 자동으로 재시작하는 기능을 제공한다.
    - 코드 수정을 적용하기 위해 개발자가 직접 재시작할 필요없이 자동으로 재시작하도록 할 수 있다.
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <optional>true</optional>
</dependency>
```

<br/>

만약, 변경시 애플리케이션이 재시작하지 않도록 하려면 해당 리소스를 제외 항목에 포함하면 된다.  
기본적으로 폴더를 가리키는 클래스 경로상의 모든 파일은 변경 시 모니터링된다.  
심지어 정적인 애셋과 뷰 템플릿과 같이 재시작이 필요 없는 것도 모니터링된다.  
이 경우 이러한 파일이 static 폴더에 있다면 application 설정 파일에 속성을 추가해 모니터링에서 제외할 수 있다.  

```yml
spring:
  devtools:
    restart:
      exclude: static/**
```

<br/>

 - `데이터베이스와 애플리케이션 통합`
    - @Document 어노테이션을 정의한 모델 클래스를 만들고, MongoRepository를 상속받는 저장소 인터페이스를 만든다.
    - 해당 인터페이스를 이용하면 CRUD 메서드를 손쉽게 사용할 수 있다.
```java
// Person 엔티티
@Getter
@Setter
@Document(collection = "person")
public class Person {

	@Id
	private String id;
	private String firstName;
	private String lastName;
	private int age;
	private Gender gender;
}

// 레포지토리: MongoRepository를 상속하는 저장소 인터페이스
public interface PersonRepository extends MongoRepository<Person, String> {
	public List<Person> findByLastName(String lastName);
	public List<Person> findByAgeGreaterThan(int age);
	
}

// 컨트롤러
@RestController
@RequestMapping("/person")
public class PersonController {
	
	@Autowired
	private PersonRepository repository;
	@Autowired
	private PersonCounterService counterService;
	
	@GetMapping
	public List<Person> findAll() {
		return repository.findAll();
	}
	
	@GetMapping("/{id}")
	public Person findById(@RequestParam("id") String id) {
		return repository.findOne(id);
	}
	
	@PostMapping
	public Person add(@RequestBody Person p) {
		p = repository.save(p);
		counterService.countNewPersons();
		return p;
	}
	
	@DeleteMapping("/{id}")
	public void delete(@RequestParam("id") String id) {
		repository.delete(id);
		counterService.countDeletedPersons();
	}
	
	@PutMapping
	public void update(@RequestBody Person p) {
		repository.save(p);
	}

}
```
