# 7장. 권한 부여 구성: 액세스 제한

스프링 시큐리티에서 애플리케이션은 인증 흐름을 완료한 후 요청을 권한 부여 필터에 위임한다. 필터는 구성된 권한 부여 규칙에 따라 요청을 허용하거나 거부한다.  

<br/>

## 권한과 역할에 따라 접근 제한

한 사용자는 하나 이상의 권한을 가진다. 인증 프로세스 도중 UserDetailsService는 사용자의 권한을 포함한 모든 세부 정보를 얻는다. 애플리케이션은 사용자를 성공적으로 인증한 후 GrantedAuthority 인터페이스로 나타내는 권한으로 권한 부여를 수행한다.  

권한은 사용자가 수행할 수 있는 작업이며, 이를 기반으로 권한 부여 규칙이 구현된다. 특정 권한이 있는 사용자만 엔드포인트에 특정 요청을 할 수 있다.  

 - hasAuthority(): 애플리케이션이 제한을 구성하는 하나의 권한만 매개 변수로 받는다. 해당 권한이 있는 사용자만 엔드포인트를 호출할 수 있다.
 - hasAnyAuthority(): 애플리케이션이 제한을 구성하는 권한을 하나 이상 받을 수 있다. 사용자는 요청하려면 지정된 권한 중 하나라도 있어야 한다.
 - access(): SpEL을 기반으로 권한 부여 규칙을 구축하므로 액세스를 구성하는 데 무한한 가능성이 있지만 코드를 읽고 디버그하기 어려운 단점이 있다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Override
    @Bean
    public UserDetailsService userDetailsService() {
        var manager = new InMemoryUserDetailsManager();

        // READ 권한을 가지는 john 계정 생성
        var user1 = User.withUsername("john")
                        .password("12345")
                        .authorities("READ")
                        .build();

        // WRITE 권한을 가지는 jane 계정 생성
        var user2 = User.withUsername("jane")
                        .password("12345")
                        .authorities("READ", "WRITE", "DELETE")
                        .build();

        manager.createUser(user1);
        manager.createUser(user2);

        return manager;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();


        // 모든 요청에 대해 액세스 허용
        // http.authorizeRequests().anyRequest().permitAll();

        // WRITE 권한이 있는 사람만 액세스 허용 (jane)
        // http.authorizeRequests().anyRequest().hasAuthority("WRITE");

        // WRITE 혹은 READ 권한이 있는 사람은 액세스 허용 (john, jane)
        // http.authorizeRequests().anyRequest().hasAnyAuthority("WRITE", "READ");
        
        // WRITE 권한이 있는 사람만 액세스 허용 (jane)
        // http.authorizeRequests().anyRequest().access("hasAuthority('WRITE')");

        // READ 권한이 있는 사람은 액세스를 허용하지만, DELETE 권한이 있는 사람은 접근 불가 (john)
        String expression = "hasAuthority('READ') and !hasAuthority('DELETE')";
        http.authorizeRequests().anyRequest().access(expression);
    }
}
```

 - HTTP 요청 테스트
    - CURL을 이용하여 HTTP Basic 요청 테스트를 할 수 있다.
```Bash
$ curl -u john:12345 http://localhost:8080/hello
$ curl -u jane:12345 http://localhost:8080/hello
```

<br/>

### 사용자 역할을 기준으로 모든 엔드포인트에 대한 접근 제한

역할은 사용자가 수행할 수 있는 작업을 나타내는 다른 방법이다. 실제 애플리케이션에서는 권한과 함꼐 역할도 이용된다.  
 - 운영자 역할: WRITE(쓰기), READ(읽기)
 - 개발자 역할: WRITE(쓰기), READ(읽기), DELETE(삭제), UPDATE(수정)
 - 애플리케이션에서 역할을 이용하면 더는 권한을 정의할 필요가 없다. 이때 권한은 개념상으로 존재하고 구현 요구 사항에도 나올 수 있지만 애플리케이션에서는 사용자가 이용 권리를 가진 하나 이상의 작업을 포함하는 역할만 정의하면 된다.

<br/>

 - `ProjectConfig`
    - 역할을 정의할 대 역할 이름은 ROLE_ 접두사로 시작해야 한다. (이 접두사는 역할과 권한 간의 차이를 나타낸다.)
    - hasRole(): 애플리케이션이 요청을 승인할 하나의 역할 이름을 매개 변수로 받는다.
    - hasAnyRole(): 애플리케이션이 요청을 승인할 여러 역할 이름을 매개 변수로 받는다.
    - access(): 애플리케이션이 요청을 승인할 역할을 스프링 식으로 지정한다. 역할을 지정하는 데는 hasRole() 또는 hasAnyRole()을 SpEL 식으로 이용할 수 있다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Override
    @Bean
    public UserDetailsService userDetailsService() {
        var manager = new InMemoryUserDetailsManager();

        var user1 = User.withUsername("john")
                        .password("12345")
                        //.authorities("ROLE_ADMIN")
                        .roles("ADMIN")
                        .build();

        var user2 = User.withUsername("jane")
                        .password("12345")
                        //.authorities("ROLE_MANAGER")
                        .roles("MANAGER")
                        .build();

        manager.createUser(user1);
        manager.createUser(user2);

        return manager;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();

        http.authorizeRequests().anyRequest().hasRole("ADMIN");

        // 정오 이후에만 엔드포인트 접근을 허용
        // access() 메서드를 이용하면 어떤 규칙이라도 구현할 수 있고 가능성이 무한해진다.
        //http.authorizeRequests().anyRequest().access("T(java.time.LocalTime).now().isAfter(T(java.time.LocalTime).of(12, 0))");
    }
}
```
