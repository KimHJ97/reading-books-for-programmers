# OAuth 2 권한 부여 서버

권한 부여 서버는 사용자를 인증하고 클라이언트에 토큰을 제공하는 역할을 한다.  
즉, 사용자 자격 증명 혹은 리프레쉬 토큰을 받아 토큰을 제공해준다.  

<br/>

## OAuth 2 주요 구성 요소

기본적으로 ClientDetailsService의 경우 InMemoryClientDetailsService 구현체가 등록되어 메모리에 저장된다.  
때문에, 권한 부여 서버가 재기동을 하면 발행했던 토큰이 무효가 된다.  
JdbcClientDetailsService 구현체를 이용해 데이터베이스에 토큰을 저장하여 관리할 수 있다.  

 - __ClientDetails__
    - ClientDetails는 OAuth 2.0 클라이언트 애플리케이션의 세부 정보를 나타내는 인터페이스입니다. 이 인터페이스를 구현하여 클라이언트 애플리케이션의 다양한 속성을 정의할 수 있습니다.
    - getClientId(): 클라이언트 ID를 반환합니다. 이는 클라이언트 애플리케이션을 고유하게 식별하는 값입니다.
    - getClientSecret(): 클라이언트 비밀번호(시크릿)를 반환합니다. 이는 클라이언트 인증에 사용됩니다.
    - getScope(): 클라이언트의 스코프(권한 범위)를 반환합니다.
    - getAuthorizedGrantTypes(): 클라이언트가 지원하는 인증 그랜트 유형을 반환합니다.
    - getRegisteredRedirectUri(): 클라이언트의 등록된 리다이렉트 URI를 반환합니다.
 - __ClientDetailsService__
    - ClientDetailsService는 ClientDetails 객체를 검색하는 데 사용되는 서비스 인터페이스입니다.
    - 이 인터페이스를 구현하여 클라이언트 애플리케이션의 정보를 데이터베이스, 메모리, 또는 다른 데이터 저장소에서 검색할 수 있습니다.
    - ClientDetailsService는 OAuth 2.0 프로토콜의 일부로 클라이언트 애플리케이션을 식별하고 인증 서버에 등록된 클라이언트 정보를 제공합니다.
 - __AuthorizationServerConfigurer__
    - AuthorizationServerConfigurer 인터페이스는 OAuth 2.0 인증 서버의 구성을 정의하는 데 사용됩니다.
    - 이를 구현하여 클라이언트의 권한 부여 및 인증 관련 설정을 할 수 있습니다.
    - 예를 들어, 허용된 그랜트 유형, 토큰 저장 방식, 토큰 만료 시간 등을 설정할 수 있습니다.
 - __TokenStore__
    - TokenStore는 발급된 OAuth 2.0 토큰을 저장하고 관리하는 인터페이스입니다.
    - 기본적으로 토큰은 메모리에 저장되지만, 데이터베이스에 저장하거나 다른 저장 방식을 사용할 수 있습니다.
    - 대표적인 구현체로는 InMemoryTokenStore와 JdbcTokenStore 등이 있습니다.

<br/>

## 권한 부여 서버 구현 방법

Spring Security를 사용하여 권한 부여 서버(Authorization Server)를 구현하려면 OAuth 2.0 프로토콜을 사용하여 클라이언트 애플리케이션에 접근 권한을 부여하는 인증 서버를 구축해야 한다.  
 - 권한 관리 서버에 필요한 의존성을 추가한다. (OAuth 2.0 및 Spring Security 관련 라이브러리)
 - @EnableAuthorizationServer 어노테이션을 정의하여 인증 서버를 활성화한다.
 - AuthorizationServerConfigurerAdapter를 확장하여 OAuth 2.0 인증 서버의 구성을 정의한다.
    - configure(ClientDetailsServiceConfigurer clients): 클라이언트 정보를 설정하고 클라이언트 애플리케이션의 권한과 인증 방식을 정의합니다. 클라이언트 ID, 비밀번호, 스코프, 그랜트 유형 등을 설정합니다.
    - configure(AuthorizationServerEndpointsConfigurer endpoints): 인증 서버의 엔드포인트를 설정하고, 인증 관리자(AuthenticationManager)를 연결합니다. 엔드포인트는 OAuth 2.0 프로토콜에서 사용되는 엔드포인트로서, 토큰 발급 및 검증을 처리합니다.
    - configure(AuthorizationServerSecurityConfigurer security): 보안 설정을 정의합니다. 예를 들어, 토큰 엔드포인트에 접근 권한을 제한할 수 있습니다.

<br/>

## 토큰 저장소 구현(데이터베이스 저장)

 - 의존성 추가
```gradle
implementation 'org.springframework.boot:spring-boot-starter-web'
implementation 'org.springframework.boot:spring-boot-starter-security'
implementation 'org.springframework.cloud:spring-cloud-starter-oauth2'
implementation 'org.springframework.boot:spring-boot-starter-data-jdbc'
implementation 'mysql:mysql-connector-java'
```

 - 설정 파일
    - DB 연결 정보 설정
```YML
spring:
    datasource:
        url: jdbc:mysql://localhost/spring?useLegacyDatetimeCode=false&serverTimezone=UTC
        username: root
        password:
        initialization-mode: always
```

 - schema.sql
    - 토큰 저장소로 사용할 스키마 정보를 정의한다.
```SQL
CREATE TABLE IF NOT EXISTS `oauth_access_token` (
    `token_id` varchar(255) NOT NULL,
    `token` blob,
    `authentication_id` varchar(255) DEFAULT NULL,
    `user_name` varchar(255) DEFAULT NULL,
    `client_id` varchar(255) DEFAULT NULL,
    `authentication` blob,
    `refresh_token` varchar(255) DEFAULT NULL,
     PRIMARY KEY (`token_id`));

CREATE TABLE IF NOT EXISTS `oauth_refresh_token` (
    `token_id` varchar(255) NOT NULL,
    `token` blob,
    `authentication` blob,
    PRIMARY KEY (`token_id`));
```

 - AuthServerConfig
    - JdbcTokenStore 등록한다.
```Java
@Configuration
@EnableAuthorizationServer
public class AuthServerConfig extends AuthorizationServerConfigurerAdapter {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private DataSource dataSource;

    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory()
                .withClient("your_client_id")
                .secret("your_client_secret")
                .authorizedGrantTypes("password", "refresh_token") // 리프레시 토큰을 지원하도록 설정
                .scopes("read", "write")
                .accessTokenValiditySeconds(3600) // 엑세스 토큰 만료 시간 (초)
                .refreshTokenValiditySeconds(86400); // 리프레시 토큰 만료 시간 (초)
    }

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints
                .authenticationManager(authenticationManager)
                .tokenStore(tokenStore())
                .reuseRefreshTokens(true);
    }

    @Bean
    public TokenStore tokenStore() {
        return new JdbcTokenStore(dataSource);
    }
}
```

 - SecurityConfig
```Java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private AuthenticationProvider authenticationProvider;

    @Override
    protected void configure(AuthenticationManagerBuilder auth) {
        auth.authenticationProvider(authenticationProvider);
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/oauth/token").permitAll() // 인증 토큰 엔드포인트는 모든 사용자에게 허용
                .antMatchers("/oauth/authorize").permitAll() // 승인 엔드포인트는 모든 사용자에게 허용
                .anyRequest().authenticated();
    }

}
```

 - 사용자 인증 정보 구현
    - UserDetailsService, AuthenticationProvider
    - AuthenticationProvider를 등록하지 않으면 기본적으로 DaoAuthenticationProvider가 등록된다.
    - DaoAuthenticationProvider는 UserDetailsSerivce의 loadUserByUsername() 메서드를 호출하고, PasswordEncoder로 입력받은 패스워드와 DB의 패스워드를 PasswordEncoder를 이용하여 검증한다.
```Java
// UserDetailsService 구현체
@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public CustomUserDetails loadUserByUsername(String username) {
        Supplier<UsernameNotFoundException> s =
                () -> new UsernameNotFoundException("Problem during authentication!");

        User u = userRepository.findUserByUsername(username).orElseThrow(s);

        return new CustomUserDetails(u);
    }
}

// AuthenticationProvider 구현체
public class CustomAuthenticationProvider implements AuthenticationProvider {

    @Autowired
    private CustomUserDetailsService userDetailsService;

    @Override
    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
        String username = authentication.getName();
        String password = authentication.getCredentials().toString();

        CustomUserDetails user = userDetailsService.loadUserByUsername(username);

        switch (user.getUser().getAlgorithm()) {
            case BCRYPT:
                return checkPassword(user, password, bCryptPasswordEncoder);
            case SCRYPT:
                return checkPassword(user, password, sCryptPasswordEncoder);
        }

        throw new BadCredentialsException("Bad credentials");
    }

    @Override
    public boolean supports(Class<?> aClass) {
        return UsernamePasswordAuthenticationToken.class.isAssignableFrom(aClass);
    }

    private Authentication checkPassword(CustomUserDetails user, String rawPassword, PasswordEncoder encoder) {
        if (encoder.matches(rawPassword, user.getPassword())) {
            return new UsernamePasswordAuthenticationToken(user.getUsername(), user.getPassword(), user.getAuthorities());
        } else {
            throw new BadCredentialsException("Bad credentials");
        }
    }
}
```

 - 사용자 인증 요청
    - 클라이언트 애플리케이션에서 권한 부여 서버로 사용자 인증 요청을 보낸다.
        - your_client_id: 클라이언트 아이디
        - your_client_secret: 클라이언트 시크릿
        - your_username: 사용자명
        - your_password: 사용자 패스워드
    - 권한 부여 서버는 UserDetailsService를 이용하여 사용자명과 패스워드를 사용하여 사용자 인증을 시도한다. 유효한 클라이언트 및 자격 증명이 확인되면 권한 부여 서버는 액세스 토큰 및 옵션으로 리프레시 토큰을 발급한다.
    - Spring Security는 기본적으로 httpBasic 인증이 활성화되어있다. (formLogin(), httpBasic())
```Bash
curl -X POST -u "your_client_id:your_client_secret" -d "grant_type=password&username=your_username&password=your_password" http://localhost:8080/oauth/token
```
