# 20장. 스프링 시큐리티 테스트

## 모의 사용자로 테스트

모의 사용자로 권한 부여 구성을 테스트한다.  

@WithMockUser 어노테이션을 이용하면 해당 테스트는 정의된 사용자로 성공적으로 인증된 것처럼 동작하게 된다.  
주의할 점으로는 실제로 인증 처리를 하지는 않는다.  

```Java
// 1
@SpringBootTest // 스프링 부트가 테스트를 위한 스프링 컨텍스트를 관리
@AutoConfigureMockMvc // 스프링 부트가 MockMvc 자동 구성
public class MainTests {

    @Autowired
    private MockMvc mvc;

    @Test
    @DisplayName("Test calling /hello endpoint without authentication returns unauthorized.")
    public void helloUnauthenticated() throws Exception {
        mvc.perform(get("/hello"))
              .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("Test calling /hello endpoint authenticated with a mock user returns ok.")
    @WithMockUser // 인증된 모의 사용자로 메서드 호출
    public void helloAuthenticated() throws Exception {
        mvc.perform(get("/hello"))
              .andExpect(content().string("Hello!"))
              .andExpect(status().isOk());
    }

    @Test
    @DisplayName("Test calling /hello endpoint authenticated with a real user returns ok.")
    public void helloAuthenticatedWithUser() throws Exception {
        mvc.perform(get("/hello")
                    .with(user("mary")))
                .andExpect(content().string("Hello!"))
                .andExpect(status().isOk());
    }
}

// 2
@SpringBootTest
@AutoConfigureMockMvc
public class MainTests {

    @Autowired
    private MockMvc mvc;

    @Test
    @DisplayName("Test calling /hello endpoint without authentication returns unauthorized.")
    public void helloUnauthenticated() throws Exception {
        mvc.perform(get("/hello"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("Test calling /hello endpoint authenticated returns ok.")
    @WithMockUser(username = "mary") // 모의 사용자 세부 정보 설정
    public void helloAuthenticated() throws Exception {
        mvc.perform(get("/hello"))
                .andExpect(content().string("Hello, mary!"))
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("Test calling /ciao endpoint authenticated returns ok.")
    @WithMockUser(username = "mary")
    public void ciaoAuthenticated() throws Exception {
        mvc.perform(get("/ciao"))
                .andExpect(content().string("Ciao, mary!"))
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("Test calling /hola endpoint authenticated returns ok.")
    @WithMockUser(username = "mary")
    public void holaAuthenticated() throws Exception {
        mvc.perform(get("/hola"))
                .andExpect(content().string("Hola, mary!"))
                .andExpect(status().isOk());
    }

}
```

<br/>

## UserDetailsService의 사용자로 테스트

테스트에 사용할 SecurityContext를 만들 때 모의 사용자를 만들지 않고 UserDetailsService에서 사용자 세부 정보를 가져온다.  
이렇게 하면 데이터 원본에서 가져온 실제 사용자로 권한 부여를 테스트할 수 있다.  

이 접근 방식에서는 컨텍스트에 UserDetailsService 빈이 있어야한다.  

```Java
@SpringBootTest
@AutoConfigureMockMvc
public class MainTests {

    @Autowired
    private MockMvc mvc;

    @Test
    @DisplayName("Test calling /hello endpoint without authentication returns unauthorized.")
    public void helloUnauthenticated() throws Exception {
        mvc.perform(get("/hello"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("Test calling /hello endpoint authenticated returns ok.")
    @WithUserDetails("john")
    public void helloAuthenticated() throws Exception {
        mvc.perform(get("/hello"))
                .andExpect(status().isOk());
    }

}
```

<br/>

## 맞춤형 인증 Authentication 객체를 이용한 테스트

테스트에 이용할 SecurityContext를 정의하는 방법을 완전히 제어하기 위해 SecurityContext를 구축하는 방법을 지시하는 팩토리 클래스를 만든다.  
이렇게 하면 유연성을 높일 수 있고 어떤 종류의 Authentication 객체를 이용할지 선택할 수 있다.  

해당 방식도 @WithMockUser와 @WithUserDetails와 마찬가지로 인증 논리를 건너뛴다.  
따라서 권한 부여와 그 이후 작업을 테스트하는 데만 사용할 수 있다.  

 - 1단계. 
    - @WithMockUser 또는 @WithUserDetails를 이용하는 방식과 비슷하게 테스트에 이용할 어노테이션을 작성한다.
    - 테스트 SecurityContext를 맞춤 구성해야하는 테스트 메서드에 지정할 맞춤형 어노테이션을 정의한다.
    - 2단계를 진행하고, @WithSecurityContext 어노테이션으로 팩토리 클랫르르 지정한다.
```Java
@Retention(RetentionPolicy.RUNTIME)
@WithSecurityContext(factory = CustomSecurityContextFactory.class)
public @interface WithCustomUser {

    String username();
}
```

 - 2단계.
    - WithSecurityContextFactory 인터페이스를 구현하는 클래스를 작성한다. 이 클래스는 프레임워크가 테스트에 이용하는 모의 SecurityContext를 반환하는 createSecurityContext() 메서드를 구현한다.
    - 맞춤형 테스트 SecurityContext를 구축할 팩토리 클래스를 구현한다. 프레임워크는 1단계에서 만든 맞춤형 어노테이션이 지정된 테스트 메서드를 찾을 때 이 팩토리 클래스를 이용한다.
```Java
public class CustomSecurityContextFactory implements WithSecurityContextFactory<WithCustomUser> {

    @Override
    public SecurityContext createSecurityContext(WithCustomUser withCustomUser) {
        // 비어 있는 보안 컨텍스트를 만든다.
        SecurityContext context = SecurityContextHolder.createEmptyContext();

        // Authentication(인증 객체)를 만든다.
        var a = new UsernamePasswordAuthenticationToken(withCustomUser.username(), null, null);
        context.setAuthentication(a); // 모의 Authentication을 SecurityContext에 추가한다.

        return context;
    }
}
```

 - 3단계.
    - 테스트 코드를 작성하고, 인증이 필요한 곳에 커스텀 어노테이션을 정의한다.
```Java
@SpringBootTest
@AutoConfigureMockMvc
public class MainTests {

    @Autowired
    private MockMvc mvc;

    @Test
    @DisplayName("Test calling /hello endpoint without authentication returns unauthorized.")
    public void helloUnauthenticated() throws Exception {
        mvc.perform(get("/hello"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("Test calling /hello endpoint authenticated returns ok.")
    @WithCustomUser(username = "mary") // 사용자 이름이 마리인 사용자로 테스트 실행
    public void helloAuthenticated() throws Exception {
        mvc.perform(get("/hello"))
                .andExpect(status().isOk());
    }

}
```

<br/>

## 메서드 보안 테스트

 - Service
```Java
@Service
public class NameService {

    @PreAuthorize("hasAuthority('write')")
    public String getName() {
        return "Fantastico";
    }
}
```

 - MainTests
    - HTTP 요청이 인증되지 않으면 AuthenticationException 예외 발생
    - HTTP 요청이 인증됐지만 사용자에게 필요한 권한이 없으면 AccessDeniedException 예외 발생
    - 필요한 권한이 있는 인증된 사용자로 호출하면 성공
```Java
@SpringBootTest
class MainTests {

    @Autowired
    private NameService nameService;

    @Test
    @DisplayName("When the method is called without an authenticated user, " +
            "it throws AuthenticationException")
    void testNameServiceWithNoUser() {
        assertThrows(AuthenticationException.class,
                () -> nameService.getName());
    }

    @Test
    @WithMockUser(authorities = "read")
    @DisplayName("When the method is called with an authenticated user having a wrong authority, " +
            "it throws AccessDeniedException")
    void testNameServiceWithUserButWrongAuthority() {
        assertThrows(AccessDeniedException.class,
                () -> nameService.getName());
    }

    @Test
    @WithMockUser(authorities = "write")
    @DisplayName("When the method is called with an authenticated user having a correct authority, " +
            "it returns the expected result")
    void testNameServiceWithUserButCorrectAuthority() {
        var result = nameService.getName();

        assertEquals("Fantastico", result);
    }
}
```

<br/>

## 인증 테스트

 - Http Basic 인증
```Java
// AuthenticationTests
@SpringBootTest
@AutoConfigureMockMvc
public class AuthenticationTests {

    @Autowired
    private MockMvc mvc;

    @Test
    @DisplayName("Test calling /hello endpoint authenticating with valid credentials returns ok.")
    public void helloAuthenticatingWithValidUser() throws Exception {
        mvc.perform(get("/hello")
                .with(httpBasic("john","12345"))) // 올바른 자격 증명으로 인증
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("Test calling /hello endpoint authenticating with wrong credentials returns unauthorized.")
    public void helloAuthenticatingWithInvalidUser() throws Exception {
        mvc.perform(get("/hello")
                .with(httpBasic("mary","12345"))) // 잘못된 자격 증명으로 인증
                .andExpect(status().isUnauthorized());
    }
}
```

 - 폼 로그인 인증
```Java
@SpringBootTest
@AutoConfigureMockMvc
public class MainTests {

    @Autowired
    private MockMvc mvc;

    // 잘못된 자격 증명 집합으로 인증할 때
    @Test
    @DisplayName("Authenticating with wrong user")
    public void loggingInWithWrongUser() throws Exception {
        mvc.perform(formLogin()
                .user("joey").password("12345"))
                .andExpect(header().exists("failed"))
                .andExpect(unauthenticated());
    }

    // 올바른 자격 증명 집합으로 인증했지만, 사용자에게 AuthenticationSuccessHandler에 작성한 요구 권한이 없을 때
    @Test
    @DisplayName("Logging in authenticating with valid user but wrong authority")
    public void loggingInWithWrongAuthority() throws Exception {
        mvc.perform(formLogin()
                    .user("mary").password("12345")
                )
                .andExpect(redirectedUrl("/error"))
                .andExpect(status().isFound())
                .andExpect(authenticated());
    }

    // 올바른 자격 증명 집합으로 인증했고, 요구 권한이 있을 때
    @Test
    @DisplayName("Logging in authenticating with valid user and correct authority")
    public void loggingInWithCorrectAuthority() throws Exception {
        mvc.perform(formLogin()
                .user("bill").password("12345")
                )
                .andExpect(redirectedUrl("/home"))
                .andExpect(status().isFound())
                .andExpect(authenticated());
    }

}
```

<br/>

## CSRF 구성 테스트

 - MainTests
    - testHelloPOST(): CSRF 토큰 없이 엔드포인트를 호출하면 HTTP 응답 상태 '403 금지됨' 반환
    - testHelloPOSTWithCSRF(): CSRF 토큰을 보내고 엔드포인트를 호출하면 HTTP 응답 상태 '200 성공' 반환
```Java
@SpringBootTest
@AutoConfigureMockMvc
public class MainTests {

    @Autowired
    private MockMvc mvc;

    @Test
    @DisplayName("Call endpoint /hello using GET")
    public void testHelloGET() throws Exception {
        mvc.perform(get("/hello"))
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("Call endpoint /hello using POST without providing the CSRF token")
    public void testHelloPOST() throws Exception {
        mvc.perform(post("/hello"))
                .andExpect(status().isForbidden());
    }

    @Test
    @DisplayName("Call endpoint /hello using POST providing the CSRF token")
    public void testHelloPOSTWithCSRF() throws Exception {
        mvc.perform(post("/hello").with(csrf()))
                .andExpect(status().isOk());
    }
}
```

<br/>

## CORS 구성 테스트

 - MainTests
```Java
@SpringBootTest
@AutoConfigureMockMvc
public class MainTests {

    @Autowired
    private MockMvc mvc;

    @Test
    @DisplayName("Test CORS configuration for /test endpoint")
    public void testCORSForTestEndpoint() throws Exception {
        mvc.perform(options("/test")
                .header("Access-Control-Request-Method", "POST")
                .header("Origin", "http://www.example.com")
        )
        .andExpect(header().exists("Access-Control-Allow-Origin"))
        .andExpect(header().string("Access-Control-Allow-Origin", "*"))
        .andExpect(header().exists("Access-Control-Allow-Methods"))
        .andExpect(header().string("Access-Control-Allow-Methods", "POST"))
        .andExpect(status().isOk());
    }

}
```

<br/>

## 리액티브 스프링 시큐리티 구현 테스트

리액티브 앱 HTTP 요청 테스트를 위해서는 MockMvc를 이용할 수 없고, WebTestClient를 이용해야 한다.  

```Java
@SpringBootTest
@AutoConfigureWebTestClient // 테스트에 이용할 WebTestClient 자동 구성
class MainTests {

    @Autowired
    private WebTestClient client;

    @Test
    @DisplayName("When calling the /hello endpoint without a user, " +
            "the application should return HTTP 401 Unauthorized.")
    void testCallHelloWithoutUser() {
        client.get()
                .uri("/hello")
                .exchange()
                .expectStatus().isUnauthorized();
    }

    @Test
    @DisplayName("When calling the /hello endpoint with a valid user, " +
            "the application should return HTTP 200 OK.")
    @WithUserDetails("john")
    void testCallHelloWithValidUser() {
        client.get()
                .uri("/hello")
                .exchange()
                .expectStatus().isOk();
    }

    @Test
    @DisplayName("When calling the /hello endpoint with a mock user, " +
            "the application should return HTTP 200 OK.")
    @WithMockUser
    void testCallHelloWithMockUser() {
        client.get()
                .uri("/hello")
                .exchange()
                .expectStatus().isOk();
    }

    @Test
    @DisplayName("When calling the /hello endpoint with a mock user, " +
            "the application should return HTTP 200 OK.")
    void testCallHelloWithValidUserWithMockUser() {
        client.mutateWith(mockUser())
                .get()
                .uri("/hello")
                .exchange()
                .expectStatus().isOk();
    }
}
```
