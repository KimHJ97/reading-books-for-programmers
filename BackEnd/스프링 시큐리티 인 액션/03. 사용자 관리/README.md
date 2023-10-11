# 3장. 사용자 관리

 - 스프링 시큐리티에서 사용자를 기술하는 UserDetails
 - 사용자가 실행할 수 있는 작업을 정의하는 GrantedAuthority
 - UserDetailsService 계약을 확장하는 UserDetailsManager. 상속된 동작 외에 사용자 만들기, 사용자의 암호 수정이나 삭제 등의 작업 지원

<br/>

## 스프링 시큐리티의 인증 구현

 - 스프링 시큐리티 인증 프로세스
```
1. 인증 필터가 요청을 가로챈다.
 - AuthenticationFilter는 요청을 가로챈다.

2. 인증 책임이 인증 관리자에 위임된다.
 - 인증 책임을 AuthenticationManager에 위임한다.

3. 인증 관리자는 인증 논리를 구현하는 인증 공급자를 이용한다.
 - AuthenticationManager는 인증 논리를 구현하기 위해 인증 공급자를 이용한다.

4. 인증 공급자는 사용자 세부 정보 서비스로 사용자를 찾고 암호 인코더로 암호를 검증한다.
 - AuthenticationProvider는 사용자 이름과 암호를 확인하기 위해 UserDetailsService 및 PasswordEncoder를 이용한다.

5. 인증 결과가 필터에 반환된다.
 - 인증 결과가 AuthenticationManager에게 전달된다.

6. 인증된 엔티티에 관한 세부 정보가 보안 컨텍스트에 저장된다.
```

<br/>

## 사용자 기술하기

애플리케이션은 사용자가 누구인지에 따라 특정 기능을 호출할 수 있는지 여부를 결정한다.  
스프링 시큐리티에서 사용자 정의는 UserDetails 계약을 준수해야 한다. UserDetails 계약은 스프링 시큐리티가 이해하는 방식으로 사용자를 나타낸다.  

### UserDetails 계약의 정의 이해하기

 - UserDetails 인터페이스
    - getUsername() 및 getPassword() 메서드는 각각 사용자 이름과 암호를 반환한다.
    - 나머지 메서드는 모두 사용자가 애플리케이션의 리소스에 접근할 수 있도록 권한을 부여하기 위한 것이다.
```
public interface UserDetails extends Serializable {
    String getUsername();
    String getPassword();
    Collection<? extends GrantedAuthority> get Authorities();
    boolean isAccountNonExpired(); // 계정 만료
    boolean isAccountNonLocked(); // 계정 잠금
    boolean isCredentialsNonExpired(); // 자격 증명 만료
    boolean isEnabled(); // 계장 비활성화
}
```

<br/>

### GrantedAuthority 계약 살펴보기

사용자에게 허가된 작업을 권한(Authority)이라고 한다. 권한은 사용자가 애플리케이션에서 수행할 수 있는 작업을 나타낸다.  
애플리케이션은 사용자가 필요로 하는 권한인 애플리케이션의 기능 요구 사항에 따라 다른 유형의 사용자를 구분해야 한다. 스프링 시큐리티에서는 GrantedAuthority 인터페이스로 권한을 나타낸다.  

 - GrantedAuthority 인터페이스
    - 사용자 세부 정보의 정의에 이용되며 사용자에게 허가된 이용 권리를 나타낸다.
    - 사용자는 권한이 하나도 없거나 여러 권한을 가질 수 있지만, 일반적으로 하나 이상의 권한을 가진다.
```Java
public interface GrantedAuthority extends Serializable {
    String getAuthority();
}
```
 - 권한 만들기
```Java
GrantedAuthority g1 = () -> "READ";
GrantedAuthority g2 = new SimpleGrantedAuthority("READ");
```

<br/>

### 최소한의 UserDetails 구현 작성

 - User
```Java
public class User implements UserDetails {

    private final String username;
    private final String password;
    private final String authority;

    public User(String username, String password, String authority) {
        this.username = username;
        this.password = password;
        this.authority = authority;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(() -> authority);
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return username;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
```

<br/>

## 스프링 시큐리티가 사용자를 관리하는 방법 지정

UserDetailsService라는 특정 구성 요소로 인증 프로세스가 사용자 관리를 위임한다.

<br/>

### UserDetailsService 계약의 이해

AuthenticationProvider는 인증 논리에서 UserDetailsService를 이용해 사용자 세부 정보를 로드한다.  
UserDetailsService의 loadUserByUsername(String username) 메서드에서 데이터베이스, 외부 시스템, 볼트 등에서 사용자를 로드하도록 구현한다.  

 - UserDetailsService 인터페이스
    - 인증 구현은 loadUserByUsername(String username) 메서드를 호출해 주어진 사용자 이름을 가진 사용자의 세부 정보를 얻는다.
    - 이 메서드가 반환하는 사용자는 UserDetails 계약의 구현이다.
```Java
public interface UserDetailsService {
    UserDetails loadUserByUsername(String username) throws UsernameNotFoundException;
}
```

<br/>

### UserDetailsService 계약 구현

애플리케이션은 사용자의 자격 증명과 다른 측면의 세부 정보를 관리한다. 이러한 정보는 데이터베이스에 저장하거나 웹 서비스 또는 기타 방법으로 접근하는 다른 시스템에서 관리할 수 있다.  

 - InMemoryUserDetailsService
    - loadUserByUsername(String username) 메서드는 주어진 사용자 이름으로 사용자의 목록을 검색하고 원하는 UserDetails 인터페이스를 반환한다.
    - 만약, 주어진 사용자 이름이 발견되지 않으면 UsernameNotFoundException 예외를 발생시킨다.
```Java
public class InMemoryUserDetailsService implements UserDetailsService {

    private final List<UserDetails> users;

    public InMemoryUserDetailsService(List<UserDetails> users) {
        this.users = users;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return users.stream()
                .filter(u -> u.getUsername().equals(username))
                .findFirst()
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
    }
}

// 사용자 등록
@Configuration
public class ProjectConfig {

    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails u = new User("john", "12345", "read");
        List<UserDetails> users = List.of(u);
        return new InMemoryUserDetailsService(users);
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }
}
```

<br/>

### UserDetailsManager 계약 구현

UserDetailsManager 인터페이스는 UserDetailsService를 확장하고 개발자가 구현할 작업을 좀 더 포함하고 있다.  

 - UserDetailsManager 인터페이스
```Java
public interface UserDetailsManager extends UserDetailsService {
    void createUser(UserDetails user);
    void updateUser(UserDetails user);
    void deleteUser(String username);
    void changePassword(String oldPassword, String newPassword);
    boolean userExists(String username);
}
```

<br/>

#### 사용자 관리에 JdbcUserDetailsManager 이용

JdbcUserDetailsManager는 SQL 데이터베이스에 저장된 사용자를 관리하며 JDBC를 통해 데이터베이스에 직접 연결한다.

 - pom.xml
```XML
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
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
</dependency>
```

 - application.properties
```properties
spring.datasource.url=jdbc:h2:mem:ssia
spring.datasource.username=sa
spring.datasource.password=
spring.datasource.initialization-mode=always
```

 - create.sql
```SQL
create schema spring;

CREATE TABLE IF NOT EXISTS `spring`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `enabled` INT NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE IF NOT EXISTS `spring`.`authorities` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `authority` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
```

 - data.sql
```SQL
INSERT INTO `spring`.`authorities` VALUES (NULL, 'john', 'write');
INSERT INTO `spring`.`users` VALUES (NULL, 'john', '12345', '1');
```

 - ProjectConfig
    - UserDetailsService 및 PasswordEncoder를 정의한다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

  @Bean
  public UserDetailsService userDetailsService(DataSource dataSource) {
    String usersByUsernameQuery = "select username, password, enabled from spring.users where username = ?";
    String authsByUserQuery = "select username, authority from spring.authorities where username = ?";

    var userDetailsManager = new JdbcUserDetailsManager(dataSource);
    userDetailsManager.setUsersByUsernameQuery(usersByUsernameQuery);
    userDetailsManager.setAuthoritiesByUsernameQuery(authsByUserQuery);
    return userDetailsManager;

  }

  @Bean
  public PasswordEncoder passwordEncoder() {
    return NoOpPasswordEncoder.getInstance();
  }

}
```
