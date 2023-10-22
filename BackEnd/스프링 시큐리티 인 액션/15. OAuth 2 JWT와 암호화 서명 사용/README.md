# 15장. OAuth 2: JWT와 암호화 서명 사용

암호화 서명으로 토큰을 검증하면 권한 부여 서버를 호출하거나 공유된 데이터베이스를 이용하지 않아도 리소스 서버가 토큰을 검증할 수 있다는 이점이 있다.  
이러한 토큰 검증 방식은 OAuth 2로 인증과 권한 부여를 구현하는 시스템에서 일반적으로 이용된다.  

<br/>

## JWT의 대칭키로 서명된 토큰 이용

JWT는 헤더, 본문, 서명의 세 부분으로 구성된다.  
헤더와 본문에는 JSON으로 나타내는 세부 정보가 들어있다.  
이러한 부분은 Base64로 인코딩된 후 서명된다.  
토큰은 이러한 세 부분이 마침표(.)로 구분된 문자열이다.  

<br/>

### 권한 부여 서버 구현

클라이언트가 권한 부여를 수행할 수 있도록 JWT를 발행하는 권한 부여 서버를 구현한다.  
스프링 시큐리티는 TokenStore의 구현체로 JWT를 관리하는 JwtTokenStore를 제공한다.  

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
```

 - application.properties
```
jwt.key=ymLTU8rq83j4fmJZj60wh4OrMNuntIj4fmJ
```

 - WebSecurityConfig
```Java
@Configuration
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public UserDetailsService uds() {
        var user = User.withUsername("john")
                .password("12345")
                .authorities("read")
                .build();

        return new InMemoryUserDetailsManager(user);
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

    @Value("${jwt.key}")
    private String jwtKey;

    @Autowired
    private AuthenticationManager authenticationManager;

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
          .authenticationManager(authenticationManager) // 토큰 저장소와 액세스 토큰 컨버터 객체 구성
          .tokenStore(tokenStore())
          .accessTokenConverter(jwtAccessTokenConverter());
    }

    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(jwtAccessTokenConverter()); // 액세스 토큰 컨버터를 연결하고 토큰 저장소 생성
    }

    @Bean
    public JwtAccessTokenConverter jwtAccessTokenConverter() {
        var converter = new JwtAccessTokenConverter();
        converter.setSigningKey(jwtKey); // 액세스 토큰 컨버터를 위해 대칭 키의 값 설정
        return converter;
    }
}
```

 - HTTP 요청 테스트
```Bash
$ curl -v -XPOST -u client:secret "http://localhost:8080/oauth/token?grant_type=password&username=john&password=12345&scope=read"
{
    "access_token": "액세스 토큰(JWT) 값",
    "token_type": "bearer",
    "refresh_token": "리프레쉬 토큰(JWT) 값",
    "expires_in": 43199,
    "scope": "read",
    "jti": ".." # 토큰의 고유 식별자
}
```

<br/>

### 리소스 서버 구현

권한 부여 서버가 발행한 토큰을 대칭 키로 검증하는 리소스 서버를 구현한다.  

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
        ..
    </dependencies>
```

 - application.properties
```
server.port=9090

jwt.key=ymLTU8rq83j4fmJZj60wh4OrMNuntIj4fmJ
```

 - HelloController
    - 인증된 사용자만 받을 수 있는 보호된 엔드포인트 하나를 정의한다.
```Java
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello!";
    }
}
```

 - ResourceServerConfig
```Java
// 권한 부여 서버와 리소스 서버가 같은 키를 공유하는 경우 (대칭키)
@Configuration
@EnableResourceServer
public class ResourceServerConfig extends ResourceServerConfigurerAdapter {

    @Value("${jwt.key}")
    private String jwtKey;

    @Override
    public void configure(ResourceServerSecurityConfigurer resources) {
        resources.tokenStore(tokenStore()); // TokenStore 구성 등록
    }

    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(jwtAccessTokenConverter()); // 액세스 토큰 컨버터를 연결하고 토큰 저장소 생성
    }

    @Bean
    public JwtAccessTokenConverter jwtAccessTokenConverter() {
        var converter = new JwtAccessTokenConverter();
        converter.setSigningKey(jwtKey); // 액세스 토큰을 만들고 토큰 서명을 검증하는 데 이용할 대칭 키 설정
        return converter;
    }
}

// 직접 Decoder 등록
@Configuration
public class ResourceServerConfig extends WebSecurityConfigurerAdapter {

    @Value("${jwt.key}")
    private String jwtKey;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .anyRequest().authenticated()
            .and()
                .oauth2ResourceServer(c -> c.jwt( jwt -> {
                    jwt.decoder(jwtDecoder());
                }));
    }

    @Bean
    public JwtDecoder jwtDecoder() {
        byte [] key = jwtKey.getBytes();
        SecretKey originalKey = new SecretKeySpec(key, 0, key.length, "AES");

        NimbusJwtDecoder jwtDecoder =
                NimbusJwtDecoder.withSecretKey(originalKey)
                .build();

        return jwtDecoder;
    }
}
```

 - HTTP 요청 테스트
    - Authorization HTTP 헤더에 'Bearer' 단어 접두사를 붙이고 토큰값을 입력한다.
```Bash
$ curl -H "Authorization:Bearer 토큰값" http://localhost:9090/hello
```

<br/>

## JWT를 이용한 비대칭키로 서명된 토큰 이용

권한 부여 서버와 리소스 서버가 비대칭 키 쌍으로 토큰에 서명하고 서명을 검증하는 OAuth 2 인증 예제를 구현한다.  
권한 부여 서버와 리소스 서버가 비밀키와 공개키를 사용하는 비대칭 키를 이용하여 보안을 더 높일 수 있다.  

### 키 쌍 생성

권한 부여 서버가 토큰을 서명하는 데 사용할 비밀 키와 리소스 서버가 서명을 검증하는 데 사용할 공개 키로 구성된 비대칭 키 쌍을 만들어주어야 한다.  
비대칭 키 쌍을 생성하기 위해서 간단한 명령줄 툴인 keytool과 OpenSSL을 이용할 수 있다.  

 - keytool을 이용하여 비대칭키 만들기
    - 비밀키 생성
        - -genkeypair: 이 옵션을 사용하여 공개 키 및 개인 키 쌍을 생성합니다. 이 키 쌍은 새로운 인증서에 저장됩니다.
        - -alias: 인증서 또는 키 저장소 내에서 사용할 고유한 별칭(alias)을 지정합니다. 이 별칭은 생성된 키 쌍 또는 인증서를 식별하는 데 사용됩니다.
        - -keyalg: 생성할 키 쌍의 알고리즘을 지정합니다. 일반적으로 RSA 또는 DSA를 사용합니다. 예를 들어, -keyalg RSA를 사용하면 RSA 키 쌍이 생성됩니다.
        - -keypass: 개인 키를 보호하는 비밀번호를 지정합니다. 이 비밀번호는 개인 키에 대한 액세스를 제한하는 데 사용됩니다.
        - -keystore: 생성된 키 쌍과 인증서를 저장할 키 저장소 파일의 경로와 이름을 지정합니다. 키 저장소는 주로 JKS(Java KeyStore) 또는 PKCS12 형식을 사용합니다.
        - -storepass: 키 저장소를 보호하는 비밀번호를 지정합니다. 이 비밀번호는 키 저장소 파일 자체를 보호하는 데 사용됩니다.
```Bash
# 비밀 키 생성
$ keytool -genkeypair -alias hjkim97 -keyalg RSA -keypass 1234 -keystore private.jks -storepass 1234

# 공개 키 얻기
$ keytool -list -rfc --keystore private.jks | openssl x509 -inform pem -pubkey
```

<br/>

### 권한 부여 서버 구현

 - application.properties
```
password=1234
privateKey=private.jks
alias=hjkim97
```

 - WebSecurityConfig
```Java
@Configuration
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public UserDetailsService uds() {
        var user = User.withUsername("john")
                .password("12345")
                .authorities("read")
                .build();

        return new InMemoryUserDetailsManager(user)
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

    @Value("${password}")
    private String password;

    @Value("${privateKey}")
    private String privateKey;

    @Value("${alias}")
    private String alias;

    @Autowired
    private AuthenticationManager authenticationManager;

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
          .tokenStore(tokenStore())
          .accessTokenConverter(jwtAccessTokenConverter());
    }

    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(jwtAccessTokenConverter()); // JwtTokenStore 등록
    }

    @Bean
    public JwtAccessTokenConverter jwtAccessTokenConverter() {
        var converter = new JwtAccessTokenConverter();

        // classpath에서 비밀키 파일을 읽을 KeyStoreKeyFactory 객체 생성
        KeyStoreKeyFactory keyStoreKeyFactory = new KeyStoreKeyFactory(
                        new ClassPathResource(privateKey), password.toCharArray());

        // KeyStoreKeyFactory 객체를 이용해 키 쌍을 가져오고 키 쌍을 JwtAccessTokenConverter 객체에 설정
        converter.setKeyPair(keyStoreKeyFactory.getKeyPair(alias));

        return converter;
    }
}
```

 - HTTP 요청 테스트
```Bash
$ curl -v -XPOST -u client:secret "http://localhost:8080/oauth/token?grant_type=password&username=john&password=12345&scope=read"
```

<br/>

### 리소스 서버 구현

공개 키를 이용해 토큰의 서명을 검증하는 리소스 서버를 구현한다.  


 - application.properties
```
server.port=9090

publicKey=-----BEGIN PUBLIC KEY-----키 내용-----END PUBLIC KEY-----
```

 - ResourceServerConfig
```Java
@Configuration
@EnableResourceServer
public class ResourceServerConfig extends ResourceServerConfigurerAdapter {

    @Value("${publicKey}")
    private String publicKey;

    @Override
    public void configure(ResourceServerSecurityConfigurer resources) {
        resources.tokenStore(tokenStore());
    }

    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(jwtAccessTokenConverter());
    }

    @Bean
    public JwtAccessTokenConverter jwtAccessTokenConverter() {
        var converter = new JwtAccessTokenConverter();
        converter.setVerifierKey(publicKey); // 컨버터로 비대칭키를 이용하고, 공개키를 등록한다.
        return converter;
    }
}

// 직접 JwtDecoder 등록시
@Configuration
public class ResourceServerConfig extends WebSecurityConfigurerAdapter {

    @Value("${publicKey}")
    private String publicKey;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.oauth2ResourceServer(
                c -> c.jwt(
                        j -> j.decoder(jwtDecoder())
                )
        );

        http.authorizeRequests()
                .anyRequest().authenticated();
    }

    @Bean
    public JwtDecoder jwtDecoder() {
        try {
            KeyFactory keyFactory = KeyFactory.getInstance("RSA");
            var key = Base64.getDecoder().decode(publicKey);

            var x509 = new X509EncodedKeySpec(key);
            var rsaKey = (RSAPublicKey) keyFactory.generatePublic(x509);
            return NimbusJwtDecoder.withPublicKey(rsaKey).build();
        } catch (Exception e) {
            throw new RuntimeException("Wrong public key");
        }
    }
}
```

<br/>

## 공개키를 노출하는 엔드포인트 이용

현재 시스템은 비밀-공개 키 쌍으로 토큰에 서명하고 서명을 검증한다.  
권한 부여 서버에서 비밀키를 구성하고, 리소스 서버에서 공개키를 구성한다.  
이렇게 두 곳에서 키를 설정하면 관리하기 어렵기 때문에 한 곳에서만 키를 구성하는 것이 좋다.  
해결책으로는 권한 부여 서버에 전체 키 쌍을 관리하는 책임을 옮기고 공개 키를 노출하는 엔드포인트를 추가하는 것이다.  

<br/>

### 권한 부여 서버

 - AuthServerConfig
```Java
@Configuration
@EnableAuthorizationServer
public class AuthServerConfig extends AuthorizationServerConfigurerAdapter {

    @Value("${password}")
    private String password;

    @Value("${privateKey}")
    private String privateKey;

    @Value("${alias}")
    private String alias;

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
                .withClient("resourceserver") // 공개키를 노출하는 엔드포이트를 호출할 때 리소스 서버가 이용하는 클라이언트 자격 증명 추가
                .secret("resourceserversecret");
    }

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints
          .authenticationManager(authenticationManager)
          .tokenStore(tokenStore())
          .tokenEnhancer(jwtAccessTokenConverter());
    }

    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(jwtAccessTokenConverter());
    }

    @Bean
    public JwtAccessTokenConverter jwtAccessTokenConverter() {
        var converter = new JwtAccessTokenConverter();

        KeyStoreKeyFactory keyStoreKeyFactory =
                new KeyStoreKeyFactory(
                        new ClassPathResource(privateKey),
                        password.toCharArray());
        converter.setKeyPair(keyStoreKeyFactory.getKeyPair(alias));

        return converter;
    }

    @Override
    public void configure(AuthorizationServerSecurityConfigurer security) {
        security.tokenKeyAccess("isAuthenticated()");
    }
}
```

 - HTTP 요청 테스트
    - 권한 부여 서버를 시작하고 /oauth/token_key 엔드포인트를 호출하여 확인할 수 있다.
```Bash
$ curl -u resourceserver:resourceserversecret http://localhost:8080/oauth/token_key
{
    "alg": "SHA256withRSA",
    "value": "-----BEGIN PUBLIC KEY-----키 내용-----END PUBLIC KEY-----"
}
```

<br/>

### 리소스 서버

 - application.properties
    - 공개키를 얻을 수 있는 엔드포인트와 클라이언트 자격 증명을 구성한다.
```
server.port=9090

security.oauth2.resource.jwt.key-uri=http://localhost:8080/oauth/token_key

security.oauth2.client.client-id=resourceserver
security.oauth2.client.client-secret=resourceserversecret
```

 - ResourceServerConfig
    - 리소스 서버의 구성 클래스에서 공개 키를 구성할 필요가 없다.
```Java
@Configuration
@EnableResourceServer
public class ResourceServerConfig extends ResourceServerConfigurerAdapter {
}
```

<br/>

## JWT에 맞춤형 세부 정보 추가

### 권한 부여 서버 구현

 - CustomTokenEnhancer
    - 토큰의 세부 정보를 추가하는 토큰 인핸서를 만든다.
    - 추가한 세부 정보는 토큰의 본문에 들어간다.
```Java
public class CustomTokenEnhancer implements TokenEnhancer {

    @Override
    public OAuth2AccessToken enhance(OAuth2AccessToken oAuth2AccessToken,
                                     OAuth2Authentication oAuth2Authentication) {

        var token = new DefaultOAuth2AccessToken(oAuth2AccessToken);

        // 토큰에 추가할 세부 정보를 맵으로 정의
        Map<String, Object> info = Map.of("generatedInZone", ZoneId.systemDefault().toString());
        token.setAdditionalInformation(info); // 토큰에 세부 정보 추가

        return token; // 세부 정보가 추가된 토큰 반환
    }
}
```

 - AuthServerConfig
```Java
@Configuration
@EnableAuthorizationServer
public class AuthServerConfig extends AuthorizationServerConfigurerAdapter {

    @Value("${password}")
    private String password;

    @Value("${privateKey}")
    private String privateKey;

    @Value("${alias}")
    private String alias;

    @Autowired
    private AuthenticationManager authenticationManager;

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
        TokenEnhancerChain tokenEnhancerChain = new TokenEnhancerChain();

        var tokenEnhancers = List.of(new CustomTokenEnhancer(), jwtAccessTokenConverter());

        tokenEnhancerChain.setTokenEnhancers(tokenEnhancers); // 체인에 토큰 인핸서 목록 추가

        endpoints
          .authenticationManager(authenticationManager)
          .tokenStore(tokenStore())
          .tokenEnhancer(tokenEnhancerChain); // 토큰 인핸서 체인 등록
    }

    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(jwtAccessTokenConverter());
    }

    @Bean
    public JwtAccessTokenConverter jwtAccessTokenConverter() {
        var converter = new JwtAccessTokenConverter();

        KeyStoreKeyFactory keyStoreKeyFactory =
                new KeyStoreKeyFactory(
                        new ClassPathResource(privateKey),
                        password.toCharArray());
        converter.setKeyPair(keyStoreKeyFactory.getKeyPair(alias));

        return converter;
    }
}
```

<br/>

### 리소스 서버 구현

JWT에 추가한 세부 정보를 읽을 수 있도록 리소스 서버를 변경한다.  

 - application.properties
```
server.port=9090

publicKey=-----BEGIN PUBLIC KEY-----키 내용-----END PUBLIC KEY-----
```

 - AdditionalClaimsAccessTokenConverter
    - AccessTokenConverter는 토큰을 Authentication으로 변환한다.
```Java
public class AdditionalClaimsAccessTokenConverter extends JwtAccessTokenConverter {

    @Override
    public OAuth2Authentication extractAuthentication(Map<String, ?> map) {
        var authentication = super.extractAuthentication(map); // Authentication(인증 객체) 변환
        authentication.setDetails(map); // Authentication에 세부 정보 추가
        return authentication; // Authentication 반환
    }
}
```

 - ResourceServerConfig
```Java
@Configuration
@EnableResourceServer
public class ResourceServerConfig extends ResourceServerConfigurerAdapter {

    @Value("${publicKey}")
    private String publicKey;

    @Override
    public void configure(ResourceServerSecurityConfigurer resources) {
        resources.tokenStore(tokenStore());
    }

    @Bean
    public TokenStore tokenStore() {
        return new JwtTokenStore(jwtAccessTokenConverter());
    }

    @Bean
    public JwtAccessTokenConverter jwtAccessTokenConverter() {
        var converter = new AdditionalClaimsAccessTokenConverter();
        converter.setVerifierKey(publicKey);
        return converter;
    }
}
```

 - HelloController
```Java
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello(OAuth2Authentication authentication) {
        // Authentication 객체에 추가된 세부 정보를 얻는다.
        OAuth2AuthenticationDetails details = (OAuth2AuthenticationDetails) authentication.getDetails();

        return "Hello! " + details.getDecodedDetails();
    }
}
```
