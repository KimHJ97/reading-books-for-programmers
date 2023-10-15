# 5장. 인증 구현

인증 논리를 담당하는 것은 AuthenticationProvider 계층이며 여기에서 요청을 허용할지 결정하는 조건과 명령을 발견할 수 있다.  
AuthenticationManager는 HTTP 필터 계층에서 요청을 수신하고 이 책임을 AuthenticationProvider에 위임하는 구성 요소이다.  

<br/>

## AuthenticationProvider의 이해

엔터프라이즈 애플리케이션에서는 사용자 이름과 암호 기반의 기본 인증 구현이 적합하지 않을 수 있다.  
예를 들어, 사용자가 SMS 메시지로 받거나 특정 애플리케이션에 표시된 코드를 이용해 신원을 증명하는 기능이 필요할 수 있다.  
또는, 사용자가 파일에 저장된 특정한 유형의 키를 제공해야 하는 인증 시나리오를 구현하거나 심지어 사용자의 지문을 이용하는 인증 논리를 구현해야 할 수도 있다.  

### 인증 프로세스 중 요청 나타내기

Authentication 인터페이스는 인증 요청 이벤트를 나타내며 애플리케이션에 접근을 요청한 엔티티의 세부 정보를 담는다. 이늦ㅇ 요청 이벤트와 관련한 정보는 인증 프로세스 도중과 이후에 이용할 수 있다. 애플리케이션에 접근을 요청하는 사용자를 주체(Principal) 라고 한다.  

 - Authentication 인터페이스
    - isAuthenticated(): 인증 프로세스가 끝났으면 true를 반환하고 아직 진행중이면 false를 반환한다.
    - getCredentials(): 인증 프로세스에 이용된 암호나 비밀을 반환한다.
    - getAuthorities(): 인증된 요청에 허가된 권한의 컬렉션을 반환한다.
```Java
public interface Authentication extends Principal, Serializable {
    Collection<? extends GrantedAuthority> getAuthorities();
    Object getCredentials();
    Object getDetails();
    Object getPrincipal();
    boolean isAuthenticated();
    void setAuthenticated(boolean isAuthenticated) throws IllegalArgumentException;
}
```

<br/>

### 맞춤형 인증 논리 구현

스프링 시큐리티의 AuthenticationProvider는 인증 논리를 처리한다.  
AuthenticationProvider 인터페이스의 기본 구현은 시스템의 사용자를 찾는 책임을 UserDetailsService에 위임하고 PasswordEncoder로 인증 프로세스에서 암호를 관리한다.  

 - AuthenticationProvider 인터페이스
    - 인증 논리를 정의하기 위해서는 authenticate() 메서드를 구현해야 한다.
        - 1. 인증이 실패하면 AuthenticationException 예외를 발생시킨다.
        - 2. 메서드가 현재 AuthenticationProvider 구현에서 지원되지 않는 인증 객체를 받으면 null을 반환해야 한다. 이렇게 하면 HTTP 필터 수준에서 분리된 여러 Authentication 형식을 사용할 가능성이 생긴다.
        - 반환값으로는 완전히 인증된 객체를 나타내는 Authentication 인스턴스를 반환해야 한다. 이 인스턴스에 대해 isAuthenticated() 메서드는 true를 반환하며, 여기에는 인증된 엔티티의 모든 필수 세부 정보가 포함된다. 또한, 일반적으로 애플리케이션은 이 인스턴스에서 암호와 같은 민감한 데이터는 제거해야 한다. 인증 후에는 암호가 더는 필요가 없다.
    - supports() 메서드
        - 해당 메서드가 true를 반환해도 authenticate() 메서드가 null을 반환하면 요청을 거부할 수 있다.
        - 인증 유형만이 아니라 요청의 세부 정보를 기준으로 인증 요청을 거부하도록 설계되어 있다.
```Java
public interface AuthenticationProvider {
    Authentication authenticate(Authentication authentication) throws AuthenticationException;
    boolean supports(Class<?> authentication);
}
```

<br/>

### 맞춤형 인증 논리 적용

 - `AuthenticationProvider 구현 과정`
    - 1. AuthenticationProvider 계약을 구현하는 클래스를 선언한다.
    - 2. 새 AuthenticationProvider가 어떤 종류의 Authentication 객체를 지원할지 결정한다.
        - 정의하는 AuthenticationProvider가 지원하는 인증 유형을 나타내도록 supports() 메서드를 재정의한다.
        - authenticate() 메서드를 재정의해 인증 논리를 구현한다.
    - 3. 새 AuthenticationProvider 구현의 인스턴스를 스프링 시큐리티에 등록한다.

<br/>

 - AuthenticationProvider 구현
    - 사용자가 존재하지 않으면 loadUserByUsername() 메서드는 AuthenticationException 예외를 발생시킨다. 이때는 인증 프로세스가 중단되고 HTTP 필터는 응답 상태를 HTTP 401 권한 없음으로 설정한다.
    - 사용자 이름이 발견되면 컨텍스트에서 PasswordEncoder의 matches() 메서드로 사용자의 암호를 확인할 수 있다.
    - 암호가 일치하지 않으면 AuthenticationException 예외를 발생시키고, 암호가 일치하면 요청의 세부 정보를 포함하는 Authentication을 인증됨으로 표시하고 반환한다.
```Java
@Component
public class CustomAuthenticationProvider implements AuthenticationProvider {

    @Autowired
    private UserDetailsService userDetailsService;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public Authentication authenticate(Authentication authentication) {
        
        String username = authentication.getName();
        String password = authentication.getCredentials().toString();

        UserDetails userDetails = userDetailsService.loadUserByUsername(username);

        if (passwordEncoder.matches(password, userDetails.getPassword())) {
            // 암호가 일치하면 필요한 세부 정보가 포함된 Authentication 계약의 구현을 반환한다.
            return new UsernamePasswordAuthenticationToken(
                username,
                password,
                userDetails.getAuthorities()
            );
        } else {
            // 암호가 일치하지 않으면 AuthenticationException 예외를 발생시킨다.
            // BadCredentialsException은 AuthenticationException을 상속한다.
            throw new BadCredentialsException("Something went wrong!");
        }
    }

    @Override
    public boolean supports(Class<?> authenticationType) {
        return authenticationType.equals(UsernamePasswordAuthenticationToken.class);
    }
}
```

 - ProjectConfig
    - AuthenticationProvider 구현체를 스프링 시큐리티에 등록하기 위해서는 WebSecurityConfigurerAdapter 클래스의 configure() 메서드를 재정의해야 한다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private AuthenticationProvider authenticationProvider;

    @Override
    protected void configure(AuthenticationManagerBuilder auth) {
        auth.authenticationProvider(authenticationProvider);
    }

    ..
}
```

<br/>

## SecurityContext 이용

인증 프로세스 이후에 인증된 엔티티에 대한 세부 정보가 필요할 수 있다. 예를 들어 현재 인증된 사용자의 이름이나 권한을 참조해야 할 수 있다.  
AuthenticationManager는 인증 프로세스를 성공적으로 완료한 후 요청이 유지되는 동안 Authentication 인스턴스를 저장한다. Authentication 객체를 저장하는 인스턴스를 보안 컨텍스트라고 한다.  

 - SecurityContext 인터페이스
    - SecurityContext의 주 책임은 Authentication 객체를 저장하는 것이다. 이때 세 가지 전략을 이용할 수 있다.
        - MODE_THREADLOCAL: 각 쓰레드가 보안 컨텍스트에 각자의 세부 정보를 저장할 수 있게 한다. 요청당 쓰레드 방식의 웹 애플리케이션에서는 각 요청이 개별 쓰레드를 가지므로 일반적인 접근법이다.
        - MODE_INHERITABLETHREADLOCAL: MODE_THREADLOCAL과 비슷하지만 비동기 메서드의 경우 보안 컨텍스트를 다음 쓰레드로 복사하도록 스프링 시큐리티에 지시한다. 이 방식으로 @Async 메서드를 실행하는 새 쓰레드가 보안 컨텍스트를 상속하게 할 수 있다.
        - MODE_GLOBAL: 애플리케이션의 모든 쓰레드가 같은 보안 컨텍스트 인스턴스를 보게 한다.
```Java
public interface SecurityContext extends Serializable {
    Authentication getAuthentication();
    void setAuthentication(Authentication authentication);
}
```

<br/>

### 보안 컨텍스트를 위한 보유 전략 이용

기본적으로 MODE_THREADLOCAL 전략으로 스프링 시큐리티는 ThreadLocal을 이용해 컨텍스트를 관리한다. TrheadLocal은 JDK 기본 기능으로 애플리케이션에서 각 쓰레드가 컬렉션에 저장된 데이터만 볼 수 있도록 보장한다. 각 요청은 자신의 보안 컨텍스트에 접근하며 쓰레드는 다른 쓰레드의 ThreadLocal에 접근할 수 없다.  

인증 프로세스가 끝난 후 필요할 때마다 SecurityContextHolder의 getContext() 메서드로 보유자에게 보안 컨텍스트를 요청할 수 있다. 그 다음에는 보안 컨텍스트에서 인증된 엔티티의 세부 정보를 저장하는 Authentication 객체를 추가로 얻을 수 있다.

 - HelloController
```Java
@RestController
public class HelloController {

    @Autowired
    private HelloService helloService;

    @GetMapping("/hello")
    public String hello(Authentication a) {
        SecurityContext context = SecurityContextHolder.getContext();
        Authentication a = context.getAuthentication();

        return "Hello, " + a.getName() + "!";
    }

    @GetMapping("/hello2")
    public String hello(Authentication a) {

        return "Hello, " + a.getName() + "!";
    }

}
```

<br/>

### 비동기 호출을 위한 보유 전략 이용

MODE_THREADLOCAL 전략은 각 쓰레드의 보안 컨텍스트를 격리할 수 있게 해준다.  
하지만, 요청당 여러 쓰레드가 사용될 때는 해당 메서드가 보안 컨텍스트를 상속하지 않는 다른 쓰레드에서 실행되기 떄문이 사용하기 어렵다.  

이러한 경우 MODE_INHERITABLETHREADLOCAL 전략으로 문제를 해결할 수 있다.  
해당 전략을 사용하기 위해서는 SecurityContextHolder.setStrategyName() 메서드를 호출하거나 spring.security.strategy 시스템 속성을 이용할 수 있다.  
이 전략을 설정하면 프레임워크는 요청의 원래 쓰레드에 있는 세부 정보를 비동기 메서드의 새로 생성된 쓰레드로 복사한다.

 - ProjectConfig
    - @Async 어노테이션 활성화
```Java
@Configuration
@EnableAsync
public class ProjectConfig {

    @Bean
    public InitializingBean initializingBean() {
        return () -> SecurityContextHolder.setStrategyName(SecurityContextHolder.MODE_INHERITABLETHREADLOCAL);
    }
}
```

 - HelloController
```Java
@RestController
public class HelloController {

    @GetMapping("/bye")
    @Async
    public void goodbye() {
        SecurityContext context = SecurityContextHolder.getContext();
        String username = context.getAuthentication().getName();
    }
}
```

<br/>

### 독립형 애플리케이션을 위한 보유 전략 이용

보안 컨텍스트가 애플리케이션의 모든 쓰레드에 공유되는 전략을 원한다면 MODE_GLOBAL을 이용할 수 있다.  
이 전략은 일반적인 애플리케이션에서는 맞지 않다. 백엔드 웹 애플리케이션은 수신하는 요청을 독립적으로 관리하므로 모든 요청에 대해 하나의 컨텍스트를 이용하기보다는 요청별로 보안 컨텍스트를 분리하는 것이 더 합리적이다.  
하지만, 독립형 애플리케이션에는 공유하는 것이 좋은 전략이 될 수 있다.

 - ProjectConfig
```Java
@Configuration
@EnableAsync
public class ProjectConfig {

    @Bean
    public InitializingBean initializingBean() {
        return () -> SecurityContextHolder.setStrategyName(SecurityContextHolder.MODE_GLOBAL);
    }
}
```

<br/>

### DelegatingSecurityContextRunnable로 보안 컨텍스트 전달

스프링 시큐리티에는 DelegatingSecurityContextRunnable 및 DelegatingSecurityContextCallable과 같은 몇 가지 훌륭한 유틸리티 클래스가 있다. 이들 클래스는 비동기적으로 실행하는 작업을 장식하고 구현이 새로 생성된 쓰레드의 보안 컨텍스트에 액세스할 수 있도록 보안 컨텍스트에서 세부 정보를 복사하는 일도 한다.  
 - DelegatingSecurity-ContextExecutor: Executor 인터페이스를 구현하며 Executor 객체를 장식하면 보안 컨텍스트를 해당 풀에 의해 생성된 쓰레드로 전달하는 기능을 제공하도록 디자인됐다.
 - DelegatingSecurityContext-ExecutorService: ExecutorService 인터페이스를 구현하며 ExecutorService 객체를 장식하면 보안 컨텍스트를 해당 풀에 의해 생성된 쓰레드로 전달하는 기능을 제공하도록 디자인됐다.
 - DelegatingSecurityContext-ScheduledExecutorService: ScheduledExecutorService 인터페이스를 구현하며 ScheduledExecutorService 객체를 장식하면 보안 컨텍스트를 해당 풀에 의해 생성된 쓰레드로 전달하는 기능을 제공하도록 디자인됐다.
 - DelegatingSecurityContext-Runnable: Runnable 인터페이스를 구현하고 다른 쓰레드에서 실행되며 응답을 반환하지 않는 작업을 나타낸다. 일반 Runnable의 기능에 더해 새 쓰레드에서 이용하기 위해 보안 컨텍스트를 전파할 수 있다.
 - DelegatingSecurityContext-Callable: Callable 인터페이스를 구현하고 다른 쓰레드에서 실행되며 최종적으로 응답을 반환하는 작업을 나타낸다. 일반 Callable의 기능에 더해 새 쓰레드에서 이용하기 위해 보안 컨텍스트를 전파할 수 있다.

 - HelloController
```Java
@RestController
public class HelloController {

    @GetMapping("/ciao")
    public String ciao() throws Exception {
        Callable<String> task = () -> {
            SecurityContext context = SecurityContextHolder.getContext();
            return context.getAuthentication().getName();
        };

        ExecutorService e = Executors.newCachedThreadPool();
        try {
            var contextTask = new DelegatingSecurityContextCallable<>(task);
            return "Ciao, " + e.submit(contextTask).get() + "!";
        } finally {
            e.shutdown();
        }
    }

    @GetMapping("/hola")
    public String hola() throws Exception {
        Callable<String> task = () -> {
            SecurityContext context = SecurityContextHolder.getContext();
            return context.getAuthentication().getName();
        };

        ExecutorService e = Executors.newCachedThreadPool();
        e = new DelegatingSecurityContextExecutorService(e);
        try {
            return "Hola, " + e.submit(task).get() + "!";
        } finally {
            e.shutdown();
        }
    }
}
```

<br/>

## HTTP Basic 인증과 양식 기반 로그인 인증 이해하기

 - CustomEntryPoint
    - 인증이 실패했을 때의 응답을 구성하려면 AuthenticationEntryPoint를 구현하면 된다.
    - 인증이 실패했을 때 시스템의 클라이언트가 응답에서 특정한 항목을 기대하는 경우 이러한 맞춤 구성이 필요하며 이를 위해 하나 이상의 헤더를 추가하거나 제거해야 할 수 있다. 또는 애플리케이션이 민감한 데이터를 클라이언트에 노출하지 않도록 응답 본문을 필터링하는 논리를 작성할 수 있다.
```Java
public class CustomEntryPoint implements AuthenticationEntryPoint {

    @Override
    public void commence(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, AuthenticationException e) throws IOException {
        httpServletResponse.addHeader("message", "Luke, I am your father!");
        httpServletResponse.sendError(HttpStatus.UNAUTHORIZED.value());
    }
}
```

 - ProjectConfig
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic(c -> {
            c.realmName("OTHER");
            c.authenticationEntryPoint(new CustomEntryPoint());
        });
        http.authorizeRequests().anyRequest().authenticated();
    }
}
```

<br/>

### 양식 기반 로그인으로 인증 구현

웹 애플리케이션을 개발할 때는 사용자가 자격 증명을 입력할 수 있는 사용자 친화적인 로그인 양식을 제공하고 인증된 사용자가 로그인 후 웹 페이지 사이를 탐색하고 로그아웃하는 기능을 구현하길 원한다.  

기본적으로 formLogin() 메서드를 정의하면, 스프링 시큐리티에서 로그인 양식과 로그아웃 페이지를 제공한다.  
자신의 UserDetailsService를 등록하지 않으면 기본 제공된 자격 증명으로 로그인할 수 있다. ('user'와 UUID 암호)  

 - ProjectConfig
    - HttpSecurity를 통해 httpBasic()이 아닌, formLogin() 메서드를 호출한다.
    - formLogin() 메서드는 FormLoginConfigurer<HttpSecurity> 형식의 객체를 반환하며이를 이용해 맞춤 구성을 할 수 있다. defaultSuccessUrl() 메서드로 성공 페이지를, 
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private CustomAuthenticationSuccessHandler authenticationSuccessHandler;

    @Autowired
    private CustomAuthenticationFailureHandler authenticationFailureHandler;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.formLogin()
            .successHandler(authenticationSuccessHandler)
            .failureHandler(authenticationFailureHandler)
        .and()
            .httpBasic();

        http.authorizeRequests()
                .anyRequest().authenticated();
    }
}
```

 - CustomAuthenticationFailureHandler
    - 인증이 실패했을 때 실행할 논리 구성
```Java
@Component
public class CustomAuthenticationFailureHandler implements AuthenticationFailureHandler {

    @Override
    public void onAuthenticationFailure(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, AuthenticationException e)  {
        httpServletResponse.setHeader("failed", LocalDateTime.now().toString());
    }
}
```

 - CustomAuthenticationSuccessHandler
    - 인증이 성공했을 때 실행할 논리 구성
```Java
@Component
public class CustomAuthenticationSuccessHandler implements AuthenticationSuccessHandler {

    @Override
    public void onAuthenticationSuccess(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Authentication authentication) throws IOException {
        var authorities = authentication.getAuthorities();

        // read 권한이 없으면 비어 있는 Optional 객체 반환
        var auth = authorities.stream()
                    .filter(a -> a.getAuthority().equals("read"))
                    .findFirst();

        if (auth.isPresent()) {
            // read 권한이 있으면 /home으로 리다이렉션
            httpServletResponse.sendRedirect("/home");
        } else {
            httpServletResponse.sendRedirect("/error");
        }
    }
}
```

 - HelloController
    - "/home" 요청에 대한 엔드포인트를 정의한다.
```Java
@RestController
public class HelloController {

    @GetMapping("/home")
    public String home() {
        return "Hello";
    }

}
```

 - HTTP 요청 테스트
```Bash
$ curl -u user:비밀번호 http://localhost:8080/home
```

<br/>

## 요약

 - AuthenticationProvider 구성 요소를 이용하면 맞춤형 인증 논리를 구현할 수 있다.
 - 맞춤형 인증 논리를 구현할 때는 책임을 분리하는 것이 좋다. AuthenticationProvider는 사용자 관리는 UserDetailsService에 위임하고 암호 검증 책임은 PasswordEncoder에 위임한다.
 - SecurityContext는 인증이 성공한 후 인증된 엔티티에 대한 세부 정보를 유지한다.
 - 보안 컨텍스트를 관리하는 데는 MODE_THREADLOCAL, MODE_INHERITABLETHREADLOCAL, MODE_GLOBA 세 전략을 이용할 수 있고, 선택한 전략에 따라 다른 쓰레드에서 보안 컨텍스트 세부 정보에 접근하는 방법이 달라진다.
 - 공유 쓰레드 로컬 전략을 사용할 떄는 스프링이 관리하는 쓰레드에만 전략이 적용된다. 프레임워크가 관리하지 않는 쓰레드에는 보안 컨텍스트를 복사하지 않는다.
 - 스프링 시큐리티 코드에서 생성했지만 프레임워크가 인식한 쓰레드를 관리할 수 있는 우수한 유틸리티 클래스를 제공한다. 코드에서 생성한 쓰레드의 SecurityContext 관리를 위해 아래 클래스 이용이 가능하다.
    - DelegatingSecurityContextRunnable
    - DelegatingSecurityContextCallable
    - DelegatingSecurityContextExecutor
 - 스프링 시큐리티는 양식 기반 로그인 인증 메서드인 formLogin()으로 로그인 양식과 로그아웃하는 옵션을 자동으로 구성한다. 작은 웹 애플리케이션의 경우 직관적으로 이용할 수 있다.
 - formLogin 인증 메서드는 세부적으로 맞춤 구성이 가능하며 HTTP Basic 방식과 함께 이용해 두 인증 유형을 모두 지원할 수도 있다.

