# 8장. 권한 부여 구성: 제한 적용

운영 단계 애플리케이션에서 모든 요청에 동일한 규칙을 적용하는 경우는 많지 않고, 일부 엔드포인트는 특정 사용자만 호출할 수 있고 나머지 엔드포인트는 모든 사용자가 호출할 수 있는 경우가 많다.  
 - MVC 선택기: 경로에 MVC 식을 이용해 엔드포인트를 선택
 - 엔트 선택기: 경로에 앤트 식을 이용해 엔드포인트를 선택
 - 정규식 선택기: 경로에 정규식(regex)을 이용해 엔드포인트를 선택

<br/>

## MVC 선택기 메서드

선택기로 요청을 참조할 때는 특정한 규칙부터 일반적인 규칙의 순서로 지정해야 한다.  

 - HelloController
```Java
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello!";
    }

    @GetMapping("/ciao")
    public String ciao() {
        return "Ciao!";
    }


    @GetMapping("/hola")
    public String hola() {
        return "Hola!";
    }

}
```

 - ProjectConifg
    - mvcMatchers(String... patterns): 경로만을 기준으로 권한 부여 제한을 적용할 때 더 쉽고 간단하게 이용할 수 있따. 이 메서드를 이용하면 자동으로 해당 경로의 모든 HTTP 방식에 제한이 적용된다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    ..

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();

        http.authorizeRequests()
                .mvcMatchers("/hello").hasRole("ADMIN")
                .mvcMatchers("/ciao").hasRole("MANAGER")
                .anyRequest().permitAll(); // 나머지 모든 엔드포인트에 대해 모든 요청 허용
                //.anyRequest().denyAll(); // 나머지 모든 엔드포인트에 대해 모든 요청 거부
                //.anyRequest().authenticated(); // 나머지 모든 엔드포인트에 대해 인증된 사용자만 허용
    }
}
```

 - ProjectConfig
    - mvcMatchers(HttpMethod method, String ... patterns): 제한을 적용할 HTTP 방식과 경로를 모두 지정할 수 있다. 같은 경로에 대해 HTTP 방식별로 다른 제한을 적용할 때 유용하다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    ..

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();

        http.authorizeRequests()
                .mvcMatchers( "/product/{code:^[0-9]*$}").permitAll() // 숫자가 포함된 호출만 허가
                .mvcMatchers( "/a/b/**").authenticated()
                .mvcMatchers(HttpMethod.GET, "/a").authenticated()
                .mvcMatchers(HttpMethod.POST, "/a").permitAll()
                .anyRequest().denyAll();

        http.csrf().disable();
    }
}
```

 - MVC 선택기 예시
```
식: /a
설명: /a 경로만

식: /a/*
설명: * 연산자는 한 경로 이름만 대체한다. /a/b 또는 a/c 와는 일치하지만, a/b/c 와는 일치하지 않는다.

식: /a/**
설명: ** 연산자는 여러 경로 이름을 대체한다. /a, /a/b, /a/b/c 모두 일치한다.

식: /a/{param}
설명: 주어진 경로 매개 변수를 포함한 /a 경로에 적용된다.

식: /a/{param:regex}
설명: 매개 변숙 값과 주어진 정규식이 일치할 때만 주어진 경로 매개 변수를 포함한 /a 경로에 적용된다.
```

<br/>

## 앤트 선택기로 권한을 부여할 요청 선택

 - antMatchers(HttpMethod method, String patterns): 제한을 적용할 HTTP 방식과 경로를 참조할 앤드 패턴을 모두 지정할 수 있다. 같은 경로 그룹에 대해 HTTP 방식별로 다른 제한을 적용할 때 유용하다.
 - antMatchers(String patterns): 경로만을 기준으로 권한 부여 제한을 적용할 때 더 쉽고 간단하게 이용할 수 있다. 모든 HTTP 방식에 자동으로 제한이 적용된다.
 - antMatchers(HttpMethod method): antMatchers(httpMethod, "/**") 와 같은 의미이며 경로와 관계없이 특정 HTTP 방식을 지정할 수 있다.

<br/>

## 정규식 선택기로 권한을 부여할 요청 선택

정규식은 어떤 문자열 형식이든지 나타낼 수 있으므로 무한의 가능성을 제공한다. 하지만 간단한 시나리오에 적용하더라도 읽기 어렵다는 단점이 있다. 따라서 MVC나 앤트 선택기를 우선적으로 이용하고 다른 대안이 없을 때만 정규식을 이용한다.  

 - 정규식 사이트: https://regexr.com/
 - regexMatchers(HttpMethod method, String regex): 제한을 적용할 HTTP 방식과 경로를 참조할 정규식을 모두 지정한다. 같은 경로 그룹에 대해 HTTP 방식별로 다른 제한을 적용할 떄 유용하다.
 - regexMatchers(String regex): 경로만을 기준으로 권한 부여 제한을 적용할 때 더 쉽고 간단하게 이용할 수 있다. 모든 HTTP 방식에 자동으로 제한이 적용된다.

<br/>

 - VideoController
    - /video/{국가}/{언어} 엔드포인트를 호출하여 동영상 콘텐츠를 가져온다.
```Java
@RestController
public class VideoController {

    @GetMapping("/video/{country}/{language}")
    public String video(@PathVariable String country,
                        @PathVariable String language) {
        return "Video allowed for " + country + " " + language;
    }

}
```

 - ProjectConfig
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    ..

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();

        http.authorizeRequests()
                .regexMatchers(".*/(us|uk|ca)+/(en|fr).*")
                    .authenticated()
            .anyRequest().hasAuthority("premium");
    }
}
```

<br/>

## MVC 선택기 경로 변수

한 경로 변수를 이용하는 조건에서는 앤트나 MVC 식 안에 정규식을 작성할 수 있다.  

 - TestController
```Java
@RestController
public class TestController {

    @GetMapping("/email/{email}")
    public String video(@PathVariable String email) {
        return "Allowed for email " + email;
    }

}
```

 - ProjectConfig
    - /email/{이메일} 엔드포인트가 있고, .com 으로 끝나는 주소를 email 매개 변수의 값으로 보내는 요청에만 선택기를 이용해 규칙을 적용한다.
```Java
@Configuration
public class ProjectConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic();

        http.authorizeRequests()
            .mvcMatchers("/email/{email:.*(.+@.+\\.com)}")
                .permitAll()
            .anyRequest()
                .denyAll();
    }
}
```
