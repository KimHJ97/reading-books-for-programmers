# CORS 필터

CORS란 Cross-Stie HTTP Requests의 약자로 한 도메인이 다른 도메인의 자원을 사용하는 것을 의미한다.  
CORS 기본 정책은 strict-origin-when-cross-origin으로 Same Origin에 대해서만 자원을 사용하도록 제한되어 있다.  
여기서 Same-Origin이란 호스트명, 프로토콜, 포트가 같은 도메인을 말한다.  
 - 클라이언트 서버와 백엔드 서버가 나뉜 경우 포트가 달라서 CORS 에러가 발생한다.
 - 때문에, 서버에서는 특정 Origin을 허용할 수 있도록 CORS 설정을 추가해주어야 한다.

<br/>

## CORS 정책 적용

### @CrossOrigin 어노테이션 이용

@CrossOrigin 어노테이션은 CORS(Cross-Origin Resource Sharing) 문제를 해결하기 위해 컨트롤러 메소드에 적용할 수 있습니다.  
이 어노테이션을 사용하면 Spring 웹 애플리케이션에서 다른 출처(도메인)로부터의 HTTP 요청을 허용하고, 필요한 CORS 헤더를 응답에 추가할 수 있습니다.  

단점으로는 CORS 정책을 적용할 컨트롤러에 반복적으로 정의해주어야 한다.  

 - MainController
```Java
@CrossOrigin(origins = "https://example.com", methods = {RequestMethod.GET, RequestMethod.POST})
@RestController
public class MainController {

    private Logger logger = Logger.getLogger(MainController.class.getName());

    @PostMapping("/post")
    public String post() {
        logger.info("Post method called");
        return "HELLO";
    }
}
```

<br/>

### Spring Boot 2.x 설정

WebSecurityConfigurerAdapter을 구현한다.  

 - SecurityConfig
```Java
@RequiredArgsConstructor
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    private final JwtTokenProvider jwtTokenProvider;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .httpBasic().disable() // Http Basic 비활성화
            .cors().configurationSource(corsConfigurationSource())
            .and()
                .csrf().disable() // CSRF 비활성화
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            .and()
                .authorizeRequests()
                    .antMatchers("/api/v1/shops/**").hasRole("OWNER")
                    .antMatchers(HttpMethod.PUT, "/api/v1/users/**").hasAnyRole("USER", "OWNER")
                    .antMatchers(HttpMethod.DELETE, "/api/v1/users/**").hasAnyRole("USER", "OWNER")
                    .antMatchers(HttpMethod.GET, "/api/v1/users/").hasAnyRole("USER", "OWNER")
                    .anyRequest().permitAll()
            .and()
                .addFilterBefore(new JwtAuthenticationFilter(jwtTokenProvider),
                        UsernamePasswordAuthenticationFilter.class);
    }
    
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();

        configuration.addAllowedOrigin("*"); // 허용 URL
        configuration.addAllowedHeader("*"); // 허용 Header
        configuration.addAllowedMethod("*"); // 허용 Method
        configuration.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
 }
```

<br/>

### Spring Boot 3.x 이상 설정

WebSecurityConfigurerAdapter를 구현하는 대신 SecurityFilterChain을 스프링 빈으로 등록한다.  

 - SecurityConfig
```Java
@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.httpBasic().disable(); // Http Basic 비활성화
        http.csrf().disable(); // CSRF 비활성화
        http.cors();
        http.sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);

        http.authorizeHttpRequests()
                .requestMatchers("/**").permitAll()
                .anyRequest().authenticated();

        return http.build();
    }
}
```

 - CorsConfig
```Java
@Configuration
public class CorsConfig {

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();

        config.setAllowCredentials(true);
        config.setAllowedOrigins(List.of("http://localhost:3000"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        config.setExposedHeaders(List.of("*"));

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }

}
```

<br/>

## 참고

 - https://gowoonsori.com/error/springsecurity-cors/
