# 9장. 필터 구현

스플이 시큐리티의 HTTP 필터는 일반적으로 요청에 적용해야 하는 각 책임을 관리하며 책임의 체인을 형성한다. 필터는 요청을 수신하고 그 논리를 실행하며 최종적으로 체인의 다음 필터에 요청을 위임한다.  

<br/>

## 스프링 시큐리티 아키텍처의 필터 구현

인증 필터는 요청을 가로채고 인증 책임을 권한 부여 관리자에게 위임한다.  
인증 이전에 특정 논리를 실행하려면 인증 필터 앞에 필터를 추가하면 된다.  
필터를 만들려면 javax.servlet 패키지의 Filter 인터페이스를 구현한다.  

 - ServletRequest: HTTP 요청을 나타낸다. ServletRequest 객체를 이용해 요청에 대한 세부 정보를 얻는다.
 - ServletResponse: HTTP 응답을 나타낸다. ServletResponse 객체를 이용해 응답을 클라이언트로 다시 보내기 전에 또는 더 나아가 필터 체인에서 응답을 변경한다.
 - FilterChain: 필터 체인을 나타낸다. FilterChain 객체는 체인의 다음 필터로 요청을 전달한다.

<br/>

스프링 시큐리티에 있는 필터는 미리 정의된 순서 번호를 가진다.  
각 필터에는 순서 번호가 있다. 이 순서 번호에 따라 요청에 필터가 적용되는 순서가 결정된다. 스프링 시큐리티가 제공하는 필터와 함께 맞춤형 필터를 추가할 수 있다.  
주의할 점으로는 필터 체인에서 여러 필터가 같은 순서 값을 가질 수 있는데, 이러한 경우 필터가 호출되는 순서가 보장되지 않는다.  
 - CorsFilter(Order: 100): CORS(교차 출처 리소스 공유) 권한 부여 규칙을 처리한다.
 - CsrfFilter(Order: 200): CSRF(사이트 간 요청 위조)를 처리한다.
 - BasicAuthenticationFilter(Order: 300): HTTP Basic 인증을 처리한다.

<br/>

## 체인에서 기존 필터 앞과 뒤에 필터 추가

모든 요청에 Request-Id 헤더가 있다고 가정한다. 이 애플리케이션은 이 헤더로 요청을 추적하므로 헤더는 필수이며 인증을 수행하기 전에 헤더가 있는지 검증하려 한다. 인증 프로세스에는 데이터베이스 쿼리나 다른 리소스를 소비하는 작업이 포함될 수 있으므로 요청의 형식이 유효하지 않으면 이런 작업을 실행할 필요가 없다.  
1. 요청에 필요한 헤더가 있는지 확인하는 RequestValidationFilter 클래스를 만든다. (필터 구현)  
2. 구성 클래스에서 configure() 메서드를 재정의해 필터 체인에 필터를 추가한다. (필터 등록)  

 - RequestValidationFilter
    - Request-Id 헤더가 있는지 확인하고 헤더가 있으면 doFilter() 메서드를 호출해 체인의 다음 필터로 요청을 전달한다.
    - 헤더가 없으면 필터 체인의 다음 필터로 요청을 전달하지 않고 응답으로 HTTP 상태 '400 잘못된 요청'을 반환한다.
```Java
public class RequestValidationFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain filterChain) throws IOException, ServletException {
        var httpRequest = (HttpServletRequest) request;
        var httpResponse = (HttpServletResponse) response;

        String requestId = httpRequest.getHeader("Request-Id");

        if (requestId == null || requestId.isBlank()) {
            httpResponse.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }

        filterChain.doFilter(request, response);
    }
}
```

 - AuthenticationLoggingFilter
    - 인증 프로세스 다음에 간단한 로깅과 추적 목적을 위해 특정한 인증 이벤트 이후 다른 시스템에 알림을 전달하는 사례
    - 인증 필터 뒤에 성공한 인증 이벤트를 모두 기록하는 필터
```Java
public class AuthenticationLoggingFilter implements Filter {

    private final Logger logger =
            Logger.getLogger(AuthenticationLoggingFilter.class.getName());

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain filterChain) throws IOException, ServletException {
        var httpRequest = (HttpServletRequest) request;

        String requestId = httpRequest.getHeader("Request-Id");

        logger.info("Successfully authenticated request with id " +  requestId);

        filterChain.doFilter(request, response);
    }
}
```

 - ProjectConfig
    - addFilterBefore(필터, 기준필터): 기준 필터 앞에 필터를 추가한다. (해당 필터 이후에 기준 필터 실행)
    - addFilterAfter(필터, 기준필터): 기준 필터 뒤에 필터를 추가한다. (기준 필터 이후에 해당 필터가 실행)
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.addFilterBefore(
                new RequestValidationFilter(),
                BasicAuthenticationFilter.class)
            .addFilterAfter(
                new AuthenticationLoggingFilter(),
                BasicAuthenticationFilter.class)
            .authorizeRequests()
                .anyRequest()
                    .permitAll();
    }
}
```

<br/>

## 필터 체인의 다른 필터 위치에 필터 추가

HTTP Basic 인증 흐름 대신 조금 다른 인증을 구현해서 애플리케이션이 사용자를 인증하기 위한 자격 증명으로 사용자 이름과 암호 대신 다른 접근법을 원한다고 가정한다.  
 - 인증을 위한 정적 헤더 값에 기반을 둔 식별
    - 정적 키에 기반을 둔 식별에서 클라이언트는 HTTP 요청의 헤더에 항상 동일한 문자열 하나를 앱으로 전달한다. 애플리케이션은 이러한 값을 DB나 비밀 볼트에 저장하고, 애플리케이션은 이 정적 값을 바탕으로 클라이언트를 식별한다.
    - 이 방식은 인증의 보안 수준이 낮지만 단순하다는 장점이 있다. 암호화 서명을 적용하는 것처럼 복잡한 계산을 수행할 필요가 없기 때문에 구현도 빠르게 실행된다.
 - 대칭 키를 이용해 인증 요청 서명
    - 대칭 키로 요청에 서명하고 검증하며 클라이언트와 서버가 모두 키의 값을 안다. 즉, 클라이언트와 서버가 키를 공유한다. 클라이언트는 이 키로 요청의 일부에 서명하고 서버는 같은 키로 서명이 유효한지 확인한다. 서버는 각 클라이언트의 개별 키를 DB나 비밀 볼트에 저장할 수 있다.
 - 인증 프로세스에 OTP 이용
    - OTP를 이용하여 사용자는 문자 메시지나 Google Authenticator 같은 인증 공급자 앱으로 OTP를 받는다.

<br/>

 - StaticKeyAuthenticationFilter
    - Filter 인터페이스를 구현하고 doFilter() 메서드를 재정의해 인증 논리 구현
    - doFilter() 에서 요청의 Authentication 헤더 값을 얻고 정적 헤더와 비교한다.
```Java
@Component
public class StaticKeyAuthenticationFilter implements Filter {

    @Value("${authorization.key}")
    private String authorizationKey;

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain filterChain) throws IOException, ServletException {
        var httpRequest = (HttpServletRequest) request;
        var httpResponse = (HttpServletResponse) response;

        String authentication = httpRequest.getHeader("Authorization");

        if (authorizationKey.equals(authentication)) {
            filterChain.doFilter(request, response);
        } else {
            httpResponse.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        }
    }
}
```

 - ProjectConfig
    - BasicAuthenticationFilter 필터 위치에 추가한다.
    - httpBasic() 메서드를 호출하지 않으므로 BasicAuthenticationFilter 인스턴스가 추가되지 않는다.
    - 체인의 같은 위치에 여러 필터를 추가하면, 대체되는 것이 아니라 순서가 보장되지 않는 필터로 서로 동작하게 된다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private StaticKeyAuthenticationFilter filter;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.addFilterAt(filter,
                BasicAuthenticationFilter.class)
                .authorizeRequests()
                .anyRequest()
                    .permitAll();
    }

}
```

 - Main
    - UserDetailsService 자동 구성을 제외한다.
```Java
@SpringBootApplication(exclude = {UserDetailsServiceAutoConfiguration.class })
public class Main {

    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }

}
```

<br/>

## 스프링 시큐리티가 제공하는 필터 구현

스프링 시큐리티에는 Filter 인터페이스를 구현하는 여러 추상 클래스가 있다.  
GenericFilterBean 클래스를 확장하면 필요할 때 web.xml 설명자 파일에 정의하여 초기화 매개 변수를 이용할 수 있다.  
OncePerRequestFilter는 GenericFilterBean을 확장하는 더 유용한 클래스로, 프레임워크는 필터 체인에 추가한 필터를 요청당 한 번만 실행하도록 보장하지는 않는다. OncePerRequestFiler는 필터의 doFilter() 메서드가 요청당 한 번만 실해되도록 논리를 구현한다.

 - AuthenticationLoggingFilter
    - OncePerRequestFilter를 구현하여 같은 요청이 여러 번 기록되지 않게 한다.
    - HttpServletRequest 및 HttpServletResponse로 요청을 수신하여 형변환할 필요가 없다.
    - 필터가 적용될지 결정하는 논리를 구현할 수 있다. 필터 체인에 추가한 필터가 특정 요청에는 적용되지 않는다고 결정할 수 있다. 이 경우 shouldNotFilter() 메서드를 재정의하면 된다.
    - OncePerRequestFilter는 기본적으로 비동기 요청이나 오류 발송 요청에는 적용되지 않는다. 이 동작을 변경하려면 shouldNotFilterAsyncDispatch() 및 shouldNotFilterErrorDispatch() 메서드를 재정의하면 된다.
```Java
public class AuthenticationLoggingFilter extends OncePerRequestFilter {

    private final Logger logger =
            Logger.getLogger(AuthenticationLoggingFilter.class.getName());


    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {

        String requestId = request.getHeader("Request-Id");

        logger.info("Successfully authenticated request with id " +  requestId);

        filterChain.doFilter(request, response);
    }
}
```
