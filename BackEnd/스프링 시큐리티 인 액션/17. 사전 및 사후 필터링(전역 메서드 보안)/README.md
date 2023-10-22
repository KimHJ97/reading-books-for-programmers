# 17장. 전역 메서드 보안: 사전 및 사후 필터링

@PreAuthorize, @PostAuthorize 어노테이션으로 애플리케이션이 메서드 호출을 허용하거나 거부하는 접근 방식을 구현할 수 있다.  
하지만, 메서드를 호출한 후 호출자가 반환된 값의 승인된 부분만 받을 수 있게 해야할 수도 있다.  

사전 권한 부여는 주어진 규칙을 준수하지 않으면 메서드가 아예 호출되지 않는다.  
사전 필터링은 메서드가 호출되지만, 규칙을 준수하는 값만 메서드에 매개 변수로 전달된다.  

이러한 기능을 필터링이라고 하며, 사전 필터링과 사후 필터링 두 범주로 분류한다.  
 - 사전 필터링: 프레임워크가 메서드를 호출하기 전에 매개 변수의 값을 필터링한다.
 - 사후 필터링: 프레임워크가 메서드를 호출한 후 반환된 값을 필터링한다.

필터링은 컬렉션과 배열에만 사용할 수 있다.  
사전 필터링은 매개변수로 배열이나 컬렉션을 받아야 하고, 사후 필터링은 반환값이 컬렉션이나 배열을 반환해야 한다.  

<br/>

## 사전 필터링 적용

필터링은 @PreFilter, @PostFilter 어노테이션으로 규칙을 설정할 수 있다.  
SpEL 식으로 제공하는 규칙에서 filterObject로 메서드의 매개 변수로 제공하는 컬렉션 또는 배열 내의 모든 요소를 참조한다.  

 - 
```Java
@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class ProjectConfig {

    @Bean
    public UserDetailsService userDetailsService() {
        var user1 = User.withUsername("nikolai")
                .password("12345")
                .authorities("read")
                .build();

        var user1 = User.withUsername("julien")
                .password("12345")
                .authorities("write")
                .build();

        return new InMemoryUserDetailsManager(user1, user2);
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }
}
```

 - Product
```Java
@Settger
@Getter
@EqualsAndHashCode
@AllArgsConstructor
public class Product {
    private String name;
    private String owner;
}
```

 - ProductService
    - Product의 owner 필드가 로그인한 사용자의 이름과 같은 값만 허용
```Java
@Service
public class ProductService {

    @PreFilter("filterObject.owner == authentication.name")
    public List<Product> sellProducts(List<Product> products) {
        return products;
    }
}
```

 - ProductController
```Java
@RestController
public class ProductController {

    @Autowired
    private ProductService productService;

    @GetMapping("/sell")
    public List<Product> sellProduct() {
        List<Product> products = new ArrayList<>();

        products.add(new Product("beer", "nikolai"));
        products.add(new Product("candy", "nikolai"));
        products.add(new Product("chocolate", "julien"));

        return productService.sellProducts(products);
    }
}
```

<br/>

## 사후 필터링 적용

사후 필터링 애스펙트는 메서드를 호출하도록 허용하지만, 메서드가 반환되면 반환된 값이 정의된 규칙을 준수하는지 확인한다.  
사후 필터링도 사전 필터링과 마찬가지로 메서드가 반환하는 컬렉션이나 배열을 변경하며 반환된 컬렉션의 요소가 따라야 하는 기준을 지정할 수 있다.  

 - ProductService
```Java
@Service
public class ProductService {

    @PostFilter("filterObject.owner == authentication.principal.username")
    public List<Product> findProducts() {
        List<Product> products = new ArrayList<>();

        products.add(new Product("beer", "nikolai"));
        products.add(new Product("candy", "nikolai"));
        products.add(new Product("chocolate", "julien"));

        return products;
    }
}
```

 - ProductController
```Java
@RestController
public class ProductController {

    @Autowired
    private ProductService productService;

    @GetMapping("/find")
    public List<Product> findProducts() {
        return productService.findProducts();
    }
}
```
