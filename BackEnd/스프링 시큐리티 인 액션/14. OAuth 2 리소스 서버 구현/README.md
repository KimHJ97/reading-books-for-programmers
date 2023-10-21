# 13장. OAuth 2: 리소스 서버 구현

리소스 서버는 사용자 리소스를 관리하는 서버이다.  
클라이언트에 리소스에 대한 접근을 허용하려면 리소스 서버에 올바른 액세스 토큰이 필요하다.  
클라이언트는 권한 부여 서버에서 액세스 토큰을 얻고 이를 HTTP 요청 헤더에 추가해 리소스 서버의 리소스를 호출한다.  

리소스 서버는 토큰을 검증하기 위해 직접 권한 부여 서버를 호출한다.  
권한 부여 서버는 특정 토큰을 발행했는지 아닌지를 알고 있다.  
권한 부여 서버는 토큰을 발행한 후 해당 토큰을 데이터베이스에도 저장한다.  

<br/>

## 권한 부여 서버 구현 (1)

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

    @Override
    @Bean
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
                .authorizedGrantTypes("password", "refresh_token")
                .scopes("read")
        .and()
                .withClient("resourceserver") // 리소스 서버가 /oauth/check_token 엔드포인트를 호출할 때 이용할 자격 증명 추가
                .secret("resourceserversecret");
    }

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints.authenticationManager(authenticationManager);
    }

    @Override
    public void configure(AuthorizationServerSecurityConfigurer security) {
        security.checkTokenAccess("isAuthenticated()"); // /oauth/check_token 엔드포인트를 호출할 수 있는 조건 지정
    }
}
```

 - HTTP 요청 테스트
```Bash
$ curl -v -XPOST -u client:secret "http://localhost:8080/oauth/token?grant_type=password&username=john&password=12345&scope=read"
{
    "access_token": "액세스 토큰값",
    "token_type": "bearer",
    "refresh_token": "갱신 토큰값",
    "expires_in": 43199,
    "scope": "read"
}

$ curl -XPOST -u resourceserver:resourceserversecret "http://localhost:8080/oauth/check_token?token=토큰값"
{
    "active": true,
    "exp": 1581307166,
    "user_name": "john",
    "authorities": ["read"],
    "client_id": "client",
    "scope": ["read"]
}
```


## 리소스 서버 구현 (2) 원격으로 토큰 확인

리소스 서버가 직접 권한 부여 서버를 호출하는 토큰 검증을 구현한다.  

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

 - application.properties
    - 스프링 부트 속성을 통해 자동으로 권한 부여 서버에 토큰 검사를 수행할 수 있다.
```properties
server.port=9090

security.oauth2.resource.token-info-uri=http://localhost:8080/oauth/check_token

security.oauth2.client.client-id=resourceserver
security.oauth2.client.client-secret=resourceserversecret
```

 - ResourceServerConfig
```Java
@Configuration
@EnableResourceServer
public class ResourceServerConfig {
}
```

### 스프링 시큐리티 OAuth 없이 토큰 자체 검사

스프링 시큐리티에는 리소스 서버 인증 메서드를 활성화하는 oauth2ResourceServer() 메서드가 제공된다.  
그 외에도 토큰 자체 검사를 이용한 리소스 서버를 구현하는데 특화된 라이브러리 의존성을 추가하여 구현할 수도 있다.  

 - pom.xml
```XML
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-oauth2-resource-server</artifactId>
            <version>5.2.1.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>com.nimbusds</groupId>
            <artifactId>oauth2-oidc-sdk</artifactId>
            <version>8.4</version>
            <scope>runtime</scope>
        </dependency>
        ..
    </dependencies>
```

 - ResourceServerConfig
```Java
@Configuration
public class ResourceServerConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .anyRequest().authenticated()
            .and()
                .oauth2ResourceServer(
                    c -> c.opaqueToken(
                            o -> {
                                o.introspectionUri("http://localhost:8080/oauth/check_token");
                                o.introspectionClientCredentials("resourceserver", "resourceserversecret");
                            })
                );
    }
}
```

<br/>

## JdbcTokenStore로 데이터베이스 참조 구현

만약, 권한 부여 서버와 리소스 서버가 서로 같은 데이터베이스를 사용하는 경우에 토큰 검사에 대해 데이터베이스 참조 구현을 할 수 있다.  
권한 부여 서버에서는 토큰을 발행할 때 데이터베이스에 저장하고, 이후 리소스 서버에서는 토큰 검사를 위해 권한 부여 서버에 직접 통신하지 않고 데이터베이스에서 토큰 정보를 가져와 검증할 수 있다.  

TokenStore는 권한 부여 서버와 리소스 서버 양쪽에서 스프링 시큐리티로 토큰을 관리하는 객체를 나타낸다.  
권한 부여 서버에서 인증이 완료되면 TokenStore를 이용해 토큰을 생성한다.  
리소스 서버의 경우 인증 필터가 TokenStore를 이용해 토큰을 검증하고 나중에 권한 부여에 이용할 사용자 세부 정보를 얻는다.  

스프링 시큐리티는 TokenStore 인터페이스에 대해서 다양한 구현체를 제공하여 보통 직접 구현할 필요는 없다.  
기본적으로 InMemoryTokenStore 구현체가 제공된다. 해당 방식은 권한 부여 서버를 재시작하면 전에 발행한 토큰이 모두 무효가 된다.  
스프링 시큐리티에 데이터베이스 참조 방식의 토큰 관리를 구현하기 위해서는 JdbcTokenStore 구현체가 제공된다.  

<br/>

### 권한 부여 서버 구현

데이터베이스가 토큰을 지속하므로 리소스 서버는 군한 부여 서버가 중단되거나 재시작해도 발행된 토큰을 검증할 수 있다.  

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
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        ..
    </dependencies>
```

 - application.propertiese
```properties
spring.datasource.url=jdbc:mysql://localhost/spring?useLegacyDatetimeCode=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=
spring.datasource.initialization-mode=always
```

 - schema.sql
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

    @Override
    @Bean
    public AuthenticationManager authenticationManagerBean() throws Exception {
        return super.authenticationManagerBean();
    }

}
```

 - AuthServerConfig
    - application.properties 파일에 구성된 데이터 원본을 통해 데이터베이스에 대한 접근을 제공하는 JdbcTokenStore의 인스턴스 생성
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
                .withClient("client")
                .secret("secret")
                .authorizedGrantTypes("password", "refresh_token")
                .scopes("read");
    }

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints
                .authenticationManager(authenticationManager)
                .tokenStore(tokenStore());
    }

    @Bean
    public TokenStore tokenStore() {
        return new JdbcTokenStore(dataSource);
    }
}
```

<br/>

### 리소스 서버 구현

 - pom.xml
```XML
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-oauth2</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        ..
    </dependencies>
```

 - application.properties
```properties
server.port=9090

spring.datasource.url=jdbc:mysql://localhost/spring?useLegacyDatetimeCode=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=
```

 - ResourceServerConfig
```Java
@Configuration
@EnableResourceServer
public class ResourceServerConfig extends ResourceServerConfigurerAdapter {

    @Autowired
    private DataSource dataSource;

    @Override
    public void configure(ResourceServerSecurityConfigurer resources) {
        resources.tokenStore(tokenStore()); // 토큰 저장소 구성
    }

    @Bean
    public TokenStore tokenStore() {
        return new JdbcTokenStore(dataSource);
    }
}
```

<br/>

## 정리

 - 권한 부여 서버를 직접 호출하는 방식
    - 리소스 서버가 토큰을 검증해야 할 때 토큰을 발행한 권한 부여서 서버를 직접 호출한다.
    - 구현하기 쉬우며, 모든 토큰 구현에 적용할 수 있다. (장점)
    - 권한 부여 서버에 불필요한 부담이 생길 수 있고, 권한 부여 서버와 리소스 서버 간에 직접 종속성이 생긴다. (단점)
 - 공유된 데이터베이스를 이용한 방식
    - 권한 부여 서버와 리소스 서버가 공유된 데이터베이스로 작업한다. 권한 부여 서버는 발행한 토큰을 데이터베이스에 저장하고 리소스 서버는 이 토큰을 읽어 검증한다.
    - 권한 부여 서버와 리소스 서바가 직접 통신할 필요가 없으며, 모든 토큰 구현에 적용할 수 있다. 또한, 토큰을 지속하므로 권한 부여 서버가 재시작하거나 중단되어도 권한 부여가 동작한다. (장점)
    - 권한 부여 서버를 직접 호출하는 것보다 구현이 어려우며, 공유된 데이터베이스가 병목 지점이 되고 시스템 성능에 영향을 미칠 수 있다. (단점)
