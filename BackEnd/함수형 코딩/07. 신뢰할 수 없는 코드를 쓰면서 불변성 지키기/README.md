# CHAPTER 7. 신뢰할 수 없는 코드를 쓰면서 불변성 지키기

바꿀 수 없는 라이브러리나 레거시 코드가 데이터를 변경한다면 카피-온-라이트를 적용할 수 없다.  
이러한 경우 내 코드를 보호하기 위해 방어적 복사를 하는 방법과 불변성을 지키는 방법에 대해 배운다.  

<br/>

## 방어적 복사는 원본이 바뀌는 것을 막아준다.

들어오고 나가는 데이터의 복사본을 만드는 것이 방어적 복사가 동작하는 방식이다.  
안전지대에 불변성을 유지하고, 바뀔 수도 있는 데이터가 안전지대로 들어오지 못하도록 하는 것이 방어적 복사의 목적이다.  

<br/>

 - 예제 코드
    - MegaMart 코드에 블랙 프라이데이 세일을 적용하도록 한다.
```JS
function add_item_to_cart(name, price) {
  var item = make_cart_item(name, price);
  shopping_cart = add_item(shopping_cart, item);
  var total = calc_total(shopping_cart);
  set_cart_total_dom(total);
  update_shipping_icons(shopping_cart);
  update_tax_dom(total);
  black_friday_promotion(shopping_cart); // 블랙 프라이데이 세일
}
```

 - 방어적 복사 구현
    - black_friday_promotion() 함수는 인자로 받은 장바구니 값을 바꾼다. 때문에, 값을 넘기기 전에 깊은 복사를 해서 함수에 넘긴다. 이렇게 하면 인자로 넘긴 원본이 바뀌지 않는다.
    - black_friday_promotion() 함수에 결과를 받아야 하는데, 복사본을 전달해 해당 함수가 변경한 cart_copy가 결과값이 된다.
    - 하지만, 이러한 cart_copy의 값도 바뀌지 않는다는 보장이 없다. 때문에, 들어오는 데이터에 방어적 복사를 적용한다.
```JS
function add_item_to_cart(name, price) {
  var item = make_cart_item(name, price);
  shopping_cart = add_item(shopping_cart, item);
  var total = calc_total(shopping_cart);
  set_cart_total_dom(total);
  update_shipping_icons(shopping_cart);
  update_tax_dom(total);
  var cart_copy = deepCopy(shopping_cart); // 넘기기 전에 복사
  black_friday_promotion(cart_copy); // 복사본으로 함수 실행
  shopping_cart = deepCopy(cart_copy); // 들어오는 데이터를 위한 복사
}
```

 - 신뢰할 수 없는 코드 감싸기
    - add_item_to_cart() 함수에 복사본을 만들어 사용하는 것에 대해서 가독성이 좋지 않을 수 있다. 때문에, 해당 블랙 프라이데이 세일 함수를 분리함으로써 더 좋은 코드를 작성할 수 있다.
```JS
function add_item_to_cart(name, price) {
  var item = make_cart_item(name, price);
  shopping_cart = add_item(shopping_cart, item);
  var total = calc_total(shopping_cart);
  set_cart_total_dom(total);
  update_shipping_icons(shopping_cart);
  update_tax_dom(total);
  shopping_cart = black_friday_promotion_safe(shopping_cart);
}

function black_friday_promotion_safe(cart) {
  var cart_copy = deepCopy(cart); // 넘기기 전에 복사
  black_friday_promotion(cart_copy); // 복사본으로 함수 실행
  return deepCopy(cart_copy); // 들어오는 데이터를 위한 복사
}
```

<br/>

### 방어적 복사 규칙

방어적 복사는 데이터를 변경할 수도 있는 코드와 불변성 코드 사이에 데이터를 주고받기 위한 원칙이다.  
 - 규칙1: 데이터가 안전한 코드에서 나갈 떄 복사하기
    - 변경 불가능한 데이터가 신뢰할 수 없는 코드로 나갈 때 원본 데이터를 복사하여 보호한다.
        - 불변성 데이터를 위한 깊은 복사본을 만든다.
        - 신뢰할 수 없는 코드로 복사본을 전달한다.
 - 규칙 2: 안전한 코드로 데이터가 들어올 떄 복사하기
    - 신뢰할 수 없는 코드에서 변경될 수도 있는 데이터가 들어올 때에도 복사하여 보호한다.
        - 변경될 수도 있는 데이터가 들어오면 바로 깊은 복사본을 만들어 안전한 코드로 전달한다.
        - 복사본을 안전한 코드에서 사용한다.

<br/>

### 카피-온-라이트와 방어적 복사 비교

 - 카피-온-라이트
    - 안전지대에서 사용 가능
    - 얕은 복사
 - 방어적 복사
    - 안전지대의 경계에서 데이터가 오고 갈 때 사용
    - 깊은 복사

<br/>

### 깊은 복사 구현

자바스크립트레서 잘 동작하는 깊은 복사를 구현하기에는 쉽지 않다.  
때문에, Lodash 라이브러리에 있는 깊은 복사 함수를 쓰는 것을 추천한다.  
Lodash에 .cloneDepp() 함수는 중첩된 데이터에 깊은 복사를 한다.  

 - 깊은 복사 동작 예제 코드
    - 아래는 깊은 복사를 이해하기 위한 예제 코드로 몇몇 타입에서 실패할 것이다.
    - 배열과 객체에 복사가 필요하기 때문에 모든 항목을 재귀적으로 반복한다.
```JS
function deepCopy(thing) {
  if(Array.isArray(thing)) {
    var copy = [];
    for(var i = 0; i < thing.length; i++)
      copy.push(deepCopy(thing[i]));
    return copy;
  } else if (thing === null) {
    return null;
  } else if(typeof thing === "object") {
    var copy = {};
    var keys = Object.keys(thing);
    for(var i = 0; i < keys.length; i++) {
      var key = keys[i];
      copy[key] = deepCopy(thing[key]);
    }
    return copy;
  } else {
    return thing;
  }
}
```

