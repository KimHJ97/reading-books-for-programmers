# 16장. 전역 메서드 보안: 사전 및 사후 권한 부여

현재까지 엔드포인트 수준에서의 권한 부여 구성을 논의했다.  
구현한 앱이 웹 애플리케이션이 아닌 경우에도 스프링 시큐리티의 권한 부여를 구성할 수 있다.  

<br/>

## 전역 메서드 보안 활성화

전역 메서드 보안은 기본적으로 비활성화 상태이므로 이 기능을 사용하려면 먼저 활성화부터 해야 한다.  

<br/>

### 호출 권한 부여

정립된 여러 이용 권리 규칙에 따라 누군가가 메서드를 호출할 수 있는지(사전 권한 부여) 또는 메서드가 실행된 후 메서드가 반환하는 것에 액세스할 수 있는지(사후 권한 부여) 결정한다.  
전역 메서드 보안의 동작 원리로는 전역 메서드 보안을 활성화하면 스프링 애스팩트 하나가 활성화된다.  
이 애스팩트는 권한 부여 규칙을 적용하는 메서드에 대한 호출을 가로채고 권한 부여 규칙을 바탕으로 가로챈 메서드로 호출을 전달할지 결정한다.  

__사전 권한 부여__ 는 메서드 호출을 위임하기 전에 권한 부여 규칙을 확인한다. 권한 부여 규칙이 준수되지 않으면 프레임워크가 호출을 위임하지 않고 메서드 호출자에 예외를 투척한다. 인증된 사용자를 기준으로 조건을 적용할 수도 있고 메서드가 매개 변수를 통해 받은 값을 참조할 수도 있다.  
__사후 권한 부여__ 에서 애스팩트는 보호된 메서드로 호출을 위임하고 보호된 메서드가 실행을 완료하면 권한 부여 규칙을 검사한다. 규칙이 준수되지 않으면 애스팩트는 결과를 호출자에 반환하지 않고 예외를 투척한다. 일반적으로 메서드가 실행한 후 반환하는 결과에 따라 권한 부여 규칙을 적용할 때 적합하다. 주의점으로는 메서드가 실행 중에 무엇인가를 변경하면 권한 부여의 성공 여부와 관계없이 변경이 남게된다.  

<br/>

## 전역 메서드 보안 활성화

스프링 시큐리티에서 기본적으로 전역 메서드 보안이 활성화되어있지 않다.  
전역 메서드 보안을 활성화하기 위해서는 @EnableGlobalMethodSecurity 어노테이션을 정의하면 된다.  
전역 메서드 보안에는 권한 부여 규칙을 정의하는 세 가지 접근 방식이 있다. (사전/사후 권한 부여 어노테이션, JSR 250 어노테이션, @Secured 어노테이션)  

 - 전역 메서드 보안 활성화
```Java
@Configuration
@EnableGlobalMethodSecurity
public class ProjectConfig {
}
```

<br/>

### 사전 권한 부여

메서드에 대한 권한 부여 규칙을 정의하기 위해 @PreAuthorize 어노테이션을 이용할 수 있다.  
@PreAuthorize 어노테이션은 권한 부여 규칙을 기술하는 SpEL 식을 값으로 받는다.  

 - ProjectConfig
    - 전역 메서드 보안을 활성화하고, 인증된 사용자 테스트하기 위해 InMemoryUserDetailsManager로 계정 2개를 등록한다.
```Java
@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class ProjectConfig {

    @Bean
    public UserDetailsService userDetailsService() {
        var user1 = User.withUsername("natalie") // read 권한이 있는 사용자
                    .password("12345")
                    .authorities("read")
                .build();

        var user2 = User.withUsername("emma") // write 권한이 있는 사용자
                .password("12345")
                .authorities("write")
                .build();

        return new InMemoryUserDetailsManager(user1, user2);
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }
}
```

 - HelloController
```Java
@RestController
public class HelloController {

    @Autowired
    private NameService nameService;

    @GetMapping("/hello")
    public String hello() {
        return "Hello, " + nameService.getName();
    }

    @GetMapping("/secret/names/{name}")
    public List<String> names(@PathVariable String name) {
        return nameService.getSecretNames(name);
    }
}
```

 - NameService
    - hasAuthority(): 여러 권한을 지정한다. 메서드를 호출하는 사용자는 이러한 권한 중 하나만 있으면 된다.
    - hasRole(): 메서드를 호출하는 사용자에게 필요한 역할을 지정한다.
    - hasAnyRole(): 여러 역할을 지정한아. 메서드를 호출하는 사용자는 이러한 역할 중 하나만 있으면 된다.
```Java
@Service
public class NameService {

    private Map<String, List<String>> secretNames = Map.of(
            "natalie", List.of("Energico", "Perfecto"),
            "emma", List.of("Fantastico"));

    @PreAuthorize("hasAuthority('write')")
    public String getName() {
        return "Fantastico";
    }

    @PreAuthorize("#name == authentication.principal.username")
    public List<String> getSecretNames(String name) {
        return secretNames.get(name);
    }
}
```

<br/>

### 사후 권한 부여

사후 권한은 메서드 호출은 허용하지만 조건을 충족하지 못하면 호출자가 반환된 값을 받지 못하게 할 수 있다.  

 - Employee
```Java
@Settger
@Getter
@EqualsAndHashCode
@AllArgsConstructor
public class Employee {

    private String name;
    private List<String> books;
    private List<String> roles;

    public Employee(String name, List<String> books, List<String> roles) {
        this.name = name;
        this.books = books;
        this.roles = roles;
    }

}
```

 - BookService
    - 직원 세부 정보는 데이터베이스에서 얻는 것이 맞지만 간단히 Map으로 구현
```Java
@Service
public class BookService {

    private Map<String, Employee> records =
            Map.of("emma",
                   new Employee("Emma Thompson", // name
                           List.of("Karamazov Brothers"), // books
                           List.of("accountant", "reader")), // roles: accountant, reader
                   "natalie",
                   new Employee("Natalie Parker", // name
                           List.of("Beautiful Paris"), // books
                           List.of("researcher")) // roles: researcher
                  );

    @PostAuthorize("returnObject.roles.contains('reader')") // 사후 권한 부여
    public Employee getBookDetails(String name) {
        return records.get(name);
    }
}
```

 - BookController
```Java
@RestController
public class BookController {

    @Autowired
    private BookService bookService;

    @GetMapping("/book/details/{name}")
    public Employee getDetails(@PathVariable String name) {
        return bookService.getBookDetails(name);
    }
}
```

<br/>

### 메서드 사용 권한 구현

 - 엔티티 및 레포지토리(Document, DocumentRepository)
    - 간단한 예제를 위해 Map을 이용하여 메모리에 저장한다.
```Java
@Settger
@Getter
@EqualsAndHashCode
@AllArgsConstructor
public class Document {
    private String owner;
}

@Repository
public class DocumentRepository {

    private Map<String, Document> documents =
            Map.of("abc123", new Document("natalie"),
                    "qwe123", new Document("natalie"),
                    "asd555", new Document("emma"));


    public Document findDocument(String code) {
        return documents.get(code);
    }
}
```

 - DocumentService
```Java
@Service
public class DocumentService {

    @Autowired
    private DocumentRepository documentRepository;

    @PostAuthorize("hasPermission(returnObject, 'ROLE_admin')")
    public Document getDocument(String code) {
        return documentRepository.findDocument(code);
    }

    @PreAuthorize("hasPermission(#code, 'document', 'ROLE_admin')")
    public Document getDocument2(String code) {
        return documentRepository.findDocument(code);
    }
}
```

 - DocumentsPermissionEvaluator
    - hasPermission()의 사용 권한 논리를 구현할 책임은 개발자가 PermissionEvaluator 인터페이스를 직접 구현해야 한다.
```Java
@Component
public class DocumentsPermissionEvaluator implements PermissionEvaluator {

    // 객체, 사용 권한
    @Override
    public boolean hasPermission(Authentication authentication,
                                 Object target, // 객체
                                 Object permission // 사용 권한
                                 ) {
        Document document = (Document) target; // target 객체를 Document로 형변환
        String p = (String) permission; // permission 객체는 역할 이름으로 String으로 형변환

        boolean admin =
           authentication.getAuthorities()
           .stream()
           .anyMatch(a -> a.getAuthority().equals(p)); // 인증 객체에 매개변수로 받은 역할이 있는지 검사

        return admin || document.getOwner().equals(authentication.getName()); // 사용자가 운영자이거나 문서의 소유자면 사용 권한 부여
    }

    // 객체 ID, 객체 형식, 사용 권한
    // 사용 권한 평가기는 필요한 객체를 얻는 데 이용할 수 있는 객체 ID를 받는다.
    // 또한 같은 권하 평가기가 여러 객체 형식에 적용될 때 이용할 수 있는 객체 형식을 받으며 사용 권한을 평가하기 위한 추가 세부 정보를 제공하는 객체가 필요하다.
    @Override
    public boolean hasPermission(Authentication authentication,
                                 Serializable targetId, // 객체 ID
                                 String targetType, // 객체 형식
                                 Object permission // 사용 권한
                                 ) {
        String code = targetId.toString();
        Document document = documentRepository.findDocument(code);

        String p = (String) permission;


        boolean admin =
                authentication.getAuthorities()
                        .stream()
                        .anyMatch(a -> a.getAuthority().equals(p));

        return admin || document.getOwner().equals(authentication.getName());
    }
}
```

 - ProjectConfig
    - 스프링 시큐리티가 새 PermissionEvaluator 구현을 인식할 수 있도록 구성 클래스에 MethodSecurityExpressionHandler를 정의해야 한다.
```Java
@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class ProjectConfig extends GlobalMethodSecurityConfiguration {

    @Autowired
    private DocumentsPermissionEvaluator evaluator;

    @Override
    protected MethodSecurityExpressionHandler createExpressionHandler() {
        var expressionHandler =
                new DefaultMethodSecurityExpressionHandler();
        expressionHandler.setPermissionEvaluator(evaluator);

        return expressionHandler;
    }

    @Bean
    public UserDetailsService userDetailsService() {
        var user1 = User.withUsername("natalie")
                    .password("12345")
                    .roles("admin")
                .build();

        var user2 = User.withUsername("emma")
                .password("12345")
                .roles("manager")
                .build();

        return new InMemoryUserDetailsManager(user1, user2);
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }
}
```

 - DocumentController
```Java
@RestController
public class DocumentController {

    @Autowired
    private DocumentService documentService;

    @GetMapping("/documents/{code}")
    public Document getDetails(@PathVariable String code) {
        return documentService.getDocument(code);
    }
}
```
