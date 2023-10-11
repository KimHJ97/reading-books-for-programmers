# 2장. 안녕! 스프링 시큐리티

## 프로젝트 만들기

스프링 부트는 프로젝트에 추가한 종속성을 바탕으로 스프링 컨텍스트의 기본 구성을 적용해준다.

 - pom.xml
```XML
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.3.0.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.laurentiuspilca</groupId>
    <artifactId>ssia-ch2-ex1</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>ssia-ch2-ex1</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>11</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
            <exclusions>
                <exclusion>
                    <groupId>org.junit.vintage</groupId>
                    <artifactId>junit-vintage-engine</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

 - HelloController
    - 엔드포인트 하나를 정의한다.
```Java
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello!";
    }
}
```

<br/>

### 엔드포인트 호출 테스트

 - curl http://localhost:8080/hello
    - 인증을 위한 올바른 자격 증명을 제공하지 않았기 때문에 응답 상태로 HTTP 401 권한 없음이 반환된다.
    - 기본적으로 스프링 시큐리티는 기본 사용자 이름(user)과 암호가 제공된다.
```JSON
{
    "status": 401,
    "error": "Unauthorized",
    "message": "Unauthorized",
    "path": "/hello"
}
```

 - curl -u user:비밀번호 http://localhost:8080/hello
    - -u 옵션을 통해 HTTP Basic 사용자 이름과 암호를 설정할 수 있다.
    - username:password 문자열을 Base64로 인코딩하고, 결과를 접두사 Basic이 붙은 Authorization 헤더 값으로 보낸다.
    - curl -H "Authorization: Basic 인코딩값" http://localhost:8080/hello
```JSON
Hello!
```

<br/>

## 기본 구성

사용자에 관한 세부 정보는 스프링 시큐리티로 UserDetailsService 계약을 구현하는 객체가 관리한다.  
AuthenticationProvider는 인증 논리를 정의하고 사용자와 암호의 관리를 위임한다. AuthenticationProvider의 기본 구현은 UserDetailsService 및 PasswordEncoder에 제공된 기본 구현을 이용한다.


 - HTTP Basic 접근 인증
    - 가장 직관적인 접근 인증 방식으로 Basic 인증에서는 클라이언트가 사용자 이름과 암호를 HTTP Authorization 헤더를 통해 보내기만 하면 된다.
    - 클라이언트는 헤더 값에 접두사 Basic을 붙이고 그 뒤에 콜론(:)으로 구분된 사용자 이름과 암호가 포함된 문자열을 Base64 인코딩하고 붙인다.
    - __HTTP Basic 인증은 자격 증명의 기밀성을 보장하지 않는다. 단순히 전송의 편의를 위한 Base64 인코딩을 진행하며, 전송 중에 자격 증명을 가로채면 누구든지 볼 수 있다.__
    - RFC 7617: https://tools.ietf.org/html/rfc7617

<br/>

## 기본 구성 재정의

### UserDetailsService 구성 요소 재정의

InMemoryUserDetailsManager는 메모리에 자격 증명을 저장해서 스프링 시큐리티가 요청을 인증할 때 이용할 수 있게 한다.  
NoOpPasswordEncoder 인스턴스는 암호에 암호화나 해시를 적용하지 않고 일반 텍스트처럼 처리한다.  

 - ProjectConfig
    - 더 이상 콘솔에 자동 생성된 암호가 출력되지 않는다. 자동 구성된 기본 구성 요소 대신 컨텍스트에 추가한 UserDetailsService 형식의 인스턴스를 이용하게 된다.
    - curl -u john:12345 http://localhost:8080/hello
```Java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.password.NoOpPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;

@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Override
    @Bean
    public UserDetailsService userDetailsService() {
        var userDetailsService = new InMemoryUserDetailsManager();

        var user = User.withUsername("john")
                .password("12345")
                .authorities("read")
                .build();

        userDetailsService.createUser(user);

        return userDetailsService;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();
        http.authorizeRequests().anyRequest().authenticated();
    }
}
```

 - ProjectConfig
    - 이전과 동일하지만, 다른 구성
    - UserDetailsService, PasswordEncoder를 빈으로 등록하지 않고, AuthenticationManagerBuilder에 등록해준다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        var userDetailsService = new InMemoryUserDetailsManager();

        var user = User.withUsername("john")
                .password("12345")
                .authorities("read")
                .build();

        userDetailsService.createUser(user);

        auth.userDetailsService(userDetailsService)
            .passwordEncoder(NoOpPasswordEncoder.getInstance());
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();
        http.authorizeRequests().anyRequest().authenticated();
    }
}
```

 - ProjectConfig
    - 이전과 동일하지만, 다른 구성
    - 가능하면 애플리케이션의 책임을 분리해서 작성하는 것이 좋기 때문에 일반적으로 이 접근 방식은 권장하지 않는다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.inMemoryAuthentication()
                .withUser("john")
                .password("12345")
                .authorities("read")
        .and()
            .passwordEncoder(NoOpPasswordEncoder.getInstance());
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();
        http.authorizeRequests().anyRequest().authenticated();
    }
}
```

<br/>

### AuthenticationProvider 구현 재정의

AuthenticationProvider는 인증 논리를 구현하고 사용자 관리와 암호 관리를 각각 UserDetailsService 및 PasswordEncoder에 위임한다.  

 - CustomAuthenticationProvider
    - AuthenticationProvider를 재정의하여 UserDetailsService나 PasswordEncoder가 더는 필요 없도록 재정의할 수 있다.
```Java
@Component
public class CustomAuthenticationProvider implements AuthenticationProvider {

    @Override
    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
        String username = authentication.getName();
        String password = String.valueOf(authentication.getCredentials());

        if ("john".equals(username) && "12345".equals(password)) {
            return new UsernamePasswordAuthenticationToken(username, password, Arrays.asList());
        } else {
            throw new AuthenticationCredentialsNotFoundException("Error!");
        }
    }

    @Override
    public boolean supports(Class<?> authenticationType) {
        return UsernamePasswordAuthenticationToken.class.isAssignableFrom(authenticationType);
    }
}
```

 - ProjectConfig
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private CustomAuthenticationProvider authenticationProvider;

    @Override
    protected void configure(AuthenticationManagerBuilder auth) {
        auth.authenticationProvider(authenticationProvider);
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();
        http.authorizeRequests()
                .anyRequest().authenticated();
    }
}
```

<br/>

### 프로젝트에 여러 구성 클래스 이용

구성 클래스에 대해 책임을 분리하는 것이 좋다.  
항상 한 클래스가 하나의 책임을 맡도록 하는 것이 바람직하다.  

 - UserManagementConfig
    - 사용자 관리를 담당하는 UserDetailsService 및 PasswordEncoder 빈만 포함한다.
```Java
@Configuration
public class UserManagementConfig {

    @Bean
    public UserDetailsService userDetailsService() {
        var userDetailsService = new InMemoryUserDetailsManager();

        var user = User.withUsername("john")
                .password("12345")
                .authorities("read")
                .build();

        userDetailsService.createUser(user);
        return userDetailsService;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }
}
```

 - WebAuthorizationConfig
    - WebSecurityConfigurerAdapter를 확장하고 configure 메서드를 재정의한다.
```Java
@Configuration
public class WebAuthorizationConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();
        http.authorizeRequests().anyRequest().authenticated();
    }
}
```
