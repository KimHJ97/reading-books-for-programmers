# 13장. OAuth 2: 권한 부여 서버 구현

권한 부여 서버의 역할은 사용자를 인증하고 클라이언트에 토큰을 제공하는 것이다.  
액세스 토큰이 만료되면 클라이언트는 새 토큰을 얻어야 하는데 이를 위해 사용자 자격 증명으로 다시 인증하거나 갱신 토큰을 이용할 수 있다.  
한 동안 스프링 시큐리티를 이용한 권한 부여 서버 개발이 더 이상 지원되지 않는다고 했다.(https://spring.io/projects/spring-security-oauth#overview)  
이후 스프링 시큐리티 팀은 새로운 권한 부여 서버를 개발 중이라는 소식을 전했다.(https://spring.io/blog/2020/04/15/announcing-the-spring-authorization-server)  
 - 스프링 시큐리티 기능 확인: https://github.com/spring-projects/spring-security/wiki/OAuth-2.0-Features-Matrix

<br/>

## 맞춤형 권한 부여 서버 구현

만약, 깃허브를 인증 서버로 이용한다면 클라이언트 앱을 알리기 위해 깃허브에 애플리케이션을 등록하고 클라이언트 자격 증명인 클라이언트 ID와 클라이언트 비밀을 받았다.  
이러한 자격 증명을 구성하고 앱에서 권한 부여 서버로 깃허브에 인증하는데 이용할 수 있다.  
권한 부여 서버를 직접 구현할 때에도 클라이언트를 알려주어야 한다.  

권한 부여 서버 에서 클라이언트를 정의하는 일은 ClientDetails가 담당하고, 해당 ID로 ClientDetails를 검색하는 객체는 ClientDetailsService이다.  
InMemoryClientDetailsService는 ClientDetailsService의 구현체이며, 메모리 안에서 ClientDetails를 관리한다. (UserDetails와 InMemoryUserDetailsManager와 비슷하다.)  

UserDetails는 사용자를 위한 것이고, ClientDetails는 클라이언트를 위한 것이다.  
UserDetailsService는 사용자를 위한 것이고, ClientDetailsService는 클라이언트를 위한 것이다.  
InMemoryUserDetailsManager는 사용자를 위한 것이고, InMemoryClientDetailsService는 클라이언트를 위한 것이다.  
JdbcUserDetailsManager는 사용자를 위한 것이고, JdbcClientDetailsService는 클라이언트를 위한 것이다.  

 - pom.xml
```XML
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
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-oauth2</artifactId>
        </dependency>
        ..
    </dependencies>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
```

 - AuthServerConfig
```Java
@Configuration
@EnableAuthorizationServer // OAuth 2 권한 부여 구성 활성화
public class AuthServerConfig extends AuthorizationServerConfigurerAdapter {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory() // 메모리에 저장된 ClientDetails 관리
                .withClient("client")
                .secret("secret")
                .authorizedGrantTypes("password", "refresh_token")
                .scopes("read");
    }
/*
    // ClientDetailsService 등록
    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        var service = new InMemoryClientDetailsService();

        // ClientDetails 생성 (클라이언트에 대한 필수 세부 정보 설정)
        var cd = new BaseClientDetails();
        cd.setClientId("client");
        cd.setClientSecret("secret");
        cd.setScope(List.of("read"));
        cd.setAuthorizedGrantTypes(List.of("password"));

        service.setClientDetailsStore(Map.of("client", cd)); // ClientDetailsService에 ClientDetails 정보 추가

        clients.withClientDetails(service);
    }
*/

    // AuthenticationManager 등록
    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints.authenticationManager(authenticationManager);
    }

    @Override
    public void configure(AuthorizationServerSecurityConfigurer security) {
        security.checkTokenAccess("isAuthenticated()");
    }
}
```

<br/>

### 사용자 관리 정의

사용자 관리를 구현하는 방법은 UserDetails, UserDetailsService, UserDetailsManager를 이용해 자격 증명을 관리하면 된다.  
또, 암호를 관리하는 데는 PasswordEncoder를 이용한다.  

 - WebSecurityConfig
    - OAuth2 측면에 집중하기 위해 InMemoryUserDetailsManager로 메모리에 계정을 하나 만든다.
    - NoOpPasswordEncoder로 비밀번호 인코딩을 하지 않고 평문으로 저장한다.
```Java
@Configuration
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public UserDetailsService uds() {
        var uds = new InMemoryUserDetailsManager();

        var u = User.withUsername("john")
                .password("12345")
                .authorities("read")
                .build();

        uds.createUser(u);

        return uds;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }

    @Override
    @Bean
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

}
```

 - HTTP 요청 테스트
    - 스프링 시큐리티는 /oauth/token 엔드퐁니트에서 토큰을 요청할 수 있도록 자동으로 구성해준다.
    - grant_type: password 값을 가진다.
    - username 및 password: 사용자 자격 증명
    - scope: 허가된 권한
```Bash
$ curl -v -XPOST -u client:secret http://localhost:8080/oauth/token?grant_type=password&username=john&password=12345&scope=read
```

<br/>

## 승인 코드 그랜트 유형 이용

승인 코드 그랜트 유형에서 클라이언트는 사용자를 권한 부여로 리다이렉션해 인증하게 한다.  
사용자가 권한 부여 서버와 직접 상호 작용해 인증하면 권한 부여 서버는 클라이언트에 리다이렉션 URI를 반환하며 이때 승인 코드를 제공한다.  
클라이언트는 승인 코드로 액세스 토큰을 얻는다.  

 - WebSecurityConfig
    - InMemoryUserDetailsManager를 이용해 메모리 사용자 자격 증명을 생성한다.
```Java
@Configuration
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public UserDetailsService uds() {
        var uds = new InMemoryUserDetailsManager();

        var u = User.withUsername("john")
                .password("12345")
                .authorities("read")
                .build();

        uds.createUser(u);

        return uds;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }

    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.formLogin();
    }
}
```

 - AuthServerConfig
```Java
@Configuration
@EnableAuthorizationServer
public class AuthServerConfig extends AuthorizationServerConfigurerAdapter {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory()
                .withClient("client") // ID가 client인 클라이언트는 승인 코드, 갱신 토큰 허가 이용 가능
                .secret("secret")
                .authorizedGrantTypes("authorization_code", "refresh_token")
                .scopes("read")
                .redirectUris("http://localhost:9090/home")
                    .and()
                .withClient("client2") // ID가 client2인 클라이언트는 승인 코드, 암호, 갱신 토큰 허가 모두 이용 가능
                .secret("secret2")
                .authorizedGrantTypes("authorization_code", "password", "refresh_token")
                .scopes("read")
                .redirectUris("http://localhost:9090/home")
    }

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints.authenticationManager(authenticationManager);
    }

}
```

 - HTTP 요청 테스트
```
1. 브라우저 접속
 - 애플리케이션에 접속하면 로그인 페이지로 리다이렉션된다.
 - http://localhost:8080/oauth/authorize?response_type=code&client_id=client&scope=read

2. 로그인 인증
 - 권한 부여 서버는 리다이렉션 URI로 사용자를 리다이렉션하고 액세스 토큰을 제공한다.
 - 클라이언트는 요청의 쿼리 매개 변수를 통해 액세스 코드를 받게 된다.
 - http://localhost:9090/home?code=qeSLSt

3. 승인 코드를 이용해 토큰 얻기
 - curl -v -XPOST -u client:secret "http://localhost:8080/oauth/token?grant_type=authorization_code&scoep=read&code=qeSLSt"
```

<br/>

## 클라이언트 자격 증명 그랜트 유형 이용

클라이언트 자격 증명 그랜트 유형에는 사용자가 관여하지 않는다.  
일반적으로 이 그랜트 유형은 두 백엔드 솔루션 간의 인증에 이용된다.  
클라이언트는 자체 자격 증명만으로 인증하고 액세스 토큰을 얻는다.  

 - WebSecurityConfig
```Java
@Configuration
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public UserDetailsService uds() {
        var uds = new InMemoryUserDetailsManager();

        var u = User.withUsername("john")
                .password("12345")
                .authorities("read")
                .build();

        uds.createUser(u);

        return uds;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }

    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }
}
```

 - AuthServerConfig
```Java
@Configuration
@EnableAuthorizationServer
public class AuthServerConfig extends AuthorizationServerConfigurerAdapter {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory()
                .withClient("client")
                .secret("secret")
                .authorizedGrantTypes("client_credentials")
                .scopes("info");
    }

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints.authenticationManager(authenticationManager);
    }

}
```

 - HTTP 요청 테스트
```Bash
$ curl -v -XPOST -u client:secret "http://localhost:8080/oauth/token?grant_type=client_credentials&scope=info"
```

<br/>

## 갱신 토큰 그랜트 유형 이용

권한 부여 서버가 갱신 토큰을 지원하게 하려면 클라이언트의 허가 목록에 갱신 토큰 허가를 추가해야 한다.  

 - WebSecurityConfig
```Java
@Configuration
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public UserDetailsService uds() {
        var uds = new InMemoryUserDetailsManager();

        var u = User.withUsername("john")
                .password("12345")
                .authorities("read")
                .build();

        uds.createUser(u);

        return uds;
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }

    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }
}
```

 - AuthServerConfig
```Java
@Configuration
@EnableAuthorizationServer
public class AuthServerConfig extends AuthorizationServerConfigurerAdapter {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory()
                .withClient("client")
                .secret("secret")
                .authorizedGrantTypes("password", "refresh_token") // refresh_token 추가
                .scopes("read");
    }

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints.authenticationManager(authenticationManager);
    }

}
```

 - HTTP 요청 테스트
```Bash
$ curl -v -XPOST -u client:secret http://localhost:8080/oauth/token?grant_type=password&username=john&password=12345&scope=read
{
    "access_token": "액세스 토큰값",
    "token_type": "bearer",
    "refresh_token": "갱신 토큰값",
    "expires_in": 43199,
    "scope": "read"
}
```
