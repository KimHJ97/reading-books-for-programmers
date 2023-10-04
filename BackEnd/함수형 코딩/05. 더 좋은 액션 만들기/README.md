# CHAPTER 5. 더 좋은 액션 만들기

액션은 필요하기 때문에, 모든 액션을 없앨 수는 없다.  
액션에서 암묵적 입력과 출력을 줄여 설계를 개선하는 방법을 알아본다.  

<br/>

## 비즈니스 요구 사항과 설계 맞추기

액션에서 계산으로 리팩토링하는 과정은 단순하고 기계적이다.  
gets_free_shipping() 함수는 비즈니스 요구 사항으로 봤을 때 맞지 않는 부분이 있다.  
요구 사항은 장바구니에 담긴 제품을 주문할 때 무료 배송인지 확인하는 것이지만, 함수를 보면 장바구니로 무료 배송을 확인하지 않고, 제품의 합계와 가격으로 확인하고 있다.  

 - 함수의 인자를 cart로 변경하여 함수 시그니처로 장바구니가 무료 배송인지 알 수 있도록 한다.
 - 별도의 계산 함수를 사용해 금액 합계를 구한다.
 - 추가적으로 함수 시그니처가 바뀌었기 때문에 이 함수를 호출하는 부분도 고쳐야 한다.
```JS
// Original
function gets_free_shipping(total, item_price) {
  return item_price + total >= 20;
}

// With new signature
function gets_free_shipping(cart) {
  return calc_total(cart) >= 20;
}

// Original
function update_shipping_icons() {
  var buttons = get_buy_buttons_dom();
  for(var i = 0; i < buttons.length; i++) {
    var button = buttons[i];
    var item = button.item;
    if(gets_free_shipping(shopping_cart_total, item.price))
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}

// With new signature
function update_shipping_icons() {
  var buttons = get_buy_buttons_dom();
  for(var i = 0; i < buttons.length; i++) {
    var button = buttons[i];
    var item = button.item;
    var new_cart = add_item(shopping_cart, item.name, item.price);
    if(gets_free_shipping(new_cart))
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}
```

<br/>

## 암묵적 입력과 출력은 적을수록 좋다.

어떤 함수에 암묵적 입력과 출력이 있다면 다른 컴포넌트와 강하게 연결된 컴포넌트라고 할 수 있다. 즉, 다른 곳에서 재사용할 수 없기 때문에 모듈이 아니고, 이런 함수의 동작은 연결된 부분의 동작에 의존한다.  

암묵적 입력과 출력이 있는 함수는 조심해서 사용해야 한다. 만약, 전역변수를 사용하는 암묵적 입력이 있을 때 값을 변경하면 다른 곳에서 해당 전역변수를 사용하는 곳에서 정상적으로 동작하지 않을 수 있다.  

```JS
// Original
function update_shipping_icons() {
  var buttons = get_buy_buttons_dom();
  for(var i = 0; i < buttons.length; i++) {
    var button = buttons[i];
    var item = button.item;
    var new_cart = add_item(shopping_cart, item.name, item.price); // shopping_cart 전역 변수를 읽고 있다.
    if(gets_free_shipping(new_cart))
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}

// With explicit argument
function update_shipping_icons(cart) { // 전역변수 대신 인자를 추가한다.
  var buttons = get_buy_buttons_dom();
  for(var i = 0; i < buttons.length; i++) {
    var button = buttons[i];
    var item = button.item;
    var new_cart = add_item(cart, item.name, item.price);
    if(gets_free_shipping(new_cart))
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}

// Original
function calc_cart_total() {
  shopping_cart_total = calc_total(shopping_cart);
  set_cart_total_dom();
  update_shipping_icons();
  update_tax_dom();
}

// Passing argument
function calc_cart_total() {
  shopping_cart_total = calc_total(shopping_cart);
  set_cart_total_dom();
  update_shipping_icons(shopping_cart); // 함수의 시그니처가 달라졌기 때문에 호출하는 곳도 변경한다.
  update_tax_dom();
}
```

<br/>

## 연습 문제

 - 전역변수 읽는 곳을 찾아 인자로 바꾸기
```JS
// Original
function add_item_to_cart(name, price) {
  shopping_cart = add_item(shopping_cart, name, price);
  calc_cart_total();
}

function calc_cart_total() {
  shopping_cart_total = calc_total(shopping_cart);
  set_cart_total_dom();
  update_shipping_icons(shopping_cart);
  update_tax_dom();
}

function set_cart_total_dom() {
  // ...
  shopping_cart_total
  //...
}

function update_shipping_icons(cart) {
  var buy_buttons = get_buy_buttons_dom();
  for(var i = 0; i < buy_buttons.length; i++) {
    var button = buy_buttons[i];
    var item = button.item;
    var new_cart = add_item(cart, item.name, item.price);
    if(gets_free_shipping(new_cart))
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}
    
function update_tax_dom() {
  set_tax_dom(calc_tax(shopping_cart_total));
}

// Eliminating reads to globals
function add_item_to_cart(name, price) {
  shopping_cart = add_item(shopping_cart, name, price); // shopping_cart 전역변수는 여기서만 읽는다.
  calc_cart_total(shopping_cart);
}

function calc_cart_total(cart) { // 해당 함수는 조금 과해보인다.
  var total = calc_total(cart);
  set_cart_total_dom(total);
  update_shipping_icons(cart);
  update_tax_dom(total);
  shopping_cart_total = total; // shopping_cart_total을 변경하지만, 어디서도 읽지 않는다.
}

function set_cart_total_dom(total) {
  //...
  total
  //...
}

function update_shipping_icons(cart) {
  var buttons = get_buy_buttons_dom();
  for(var i = 0; i < buttons.length; i++) {
    var button = buttons[i];
    var item = button.item;
    var new_cart = add_item(cart, item.name, item.price);
    if(gets_free_shipping(new_cart))
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}

function update_tax_dom(total) {
  set_tax_dom(calc_tax(total));
}
```

 - 코드 다시 살펴보기
    - 사용하지 않는 shopping_cart_total 전역변수와 과해 보이는 calc_cart_total() 함수를 정리한다.
```JS
// Before
function add_item_to_cart(name, price) {
  shopping_cart = add_item(shopping_cart, name, price);
  calc_cart_total(shopping_cart);
}

function calc_cart_total(cart) { // add_item_to_cart() 함수에 있어도 될 것 같다.
  var total = calc_total(cart);
  set_cart_total_dom(total);
  update_shipping_icons(cart);
  update_tax_dom(total);
  shopping_cart_total = total; // shopping_cart_total을 변경하지만, 어디서도 읽지 않는다.
}

// After
function add_item_to_cart(name, price) {
  shopping_cart = add_item(shopping_cart, name, price);
  var total = calc_total(shopping_cart);
  set_cart_total_dom(total);
  update_shipping_icons(shopping_cart);
  update_tax_dom(total);
}
```

<br/>

## 설계는 엉켜있는 코드를 푸는 것이다.

함수는 작으면 작을수록 재사용하기 쉽다.  
작은 함수는 쉽게 이해할 수 있고 유지보수하기 쉽다.  
작은 함수는 테스트하기 좋다. 한 가지 일만 하기 때문에 한 가지만 테스트하면 된다.  

 - 계산 분류하기
    - C: 장바구니(cart)에 대한 동작
    - I: 제품(item)에 대한 동작
    - B: 비즈니스 규칙
```JS
function add_item(cart, name, price) { // C I
  var new_cart = cart.slice();
  new_cart.push({
    name: name,
    price: price
  });
  return new_cart;
}

function calc_total(cart) { // C I B
  var total = 0;
  for(var i = 0; i < cart.length; i++) {
    var item = cart[i];
    total += item.price;
  }
  return total;
}

function gets_free_shipping(total, item_price) { // B
    return item_price + total >= 20;
}

function calc_tax(amount) { // B
  return amount * 0.10;
}
```

<br/>

 - add_item()을 분리해 더 좋은 설계 만들기
    - add_item() 함수를 자세히 살펴보면 네 부분으로 나눌 수 있다.
        - A. 배열을 복사한다.
        - B. item 객체를 만든다.
        - C. 복사본에 item을 추가한다.
        - D. 복사본을 리턴한다.
    - add_item() 함수는 cart와 item 구조를 모두 알고 있다. item에 관한 코드를 별도의 함수로 분리할 수 있다.
    - item 구조만 알고 있는 함수(make_cart_item)와 cart 구조만 알고 있는 함수(add_item)로 나눠 분리하면 cart와 item을 독립적으로 확장할 수 있다.
    - add_item() 함수는 이제 cart와 item에 특화된 함수가 아닌, 일반적인 배열과 항목을 넘겨도 잘 동작하게 된다.
```JS
/// Original
function add_item(cart, name, price) {
  var new_cart = cart.slice(); // 1. 배열을 복사한다.
  new_cart.push({ // 2. item 객체를 만든다. 3. 복사본에 item을 추가한다.
    name: name,
    price: price
  });
  return new_cart; // 4. 복사본을 리턴한다.
}

add_item(shopping_cart, "shoes", 3.45);

/// Pulled apart
function make_cart_item(name, price) {
  return {
    name: name,
    price: price
  };
}

function add_item(cart, item) {
  var new_cart = cart.slice();
  new_cart.push(item);
  return new_cart;
}

add_item(shopping_cart, make_cart_item("shoes", 3.45));
```

<br/>

 - 카피-온-라이트 패턴 빼내기
    - add_item() 함수는 이제 크기가 작고 괜찮은 함수이다.
    - 해당 함수는 이제 일반적인 배열과 항목에 쓸 수 있지만 이름이 일반적이지 않다.
    - __장바구니와 제품에만 쓸 수 있는 함수가 아닌 어떤 배열이나 항목에도 쓸 수 있는 이름으로 변경한다.__
```JS
/// Original
function add_item(cart, item) {
  var new_cart = cart.slice();
  new_cart.push(item);
  return new_cart;
}

/// General
function add_element_last(array, elem) {
  var new_array = array.slice();
  new_array.push(elem);
  return new_array;
}

function add_item(cart, item) {
  return add_element_last(cart, item);
}
```

<br/>

 - add_item() 사용하는 곳 변경
    - add_item()은 기존에 cart, name, price 인자가 필요했지만 시그니처가 변경되었다. 때문에, 해당 함수를 호출하던 곳도 변경하여야 한다.
```JS
/// Original
function add_item_to_cart(name, price) {
  shopping_cart = add_item(shopping_cart, name, price);
  var total = calc_total(shopping_cart);
  set_cart_total_dom(total);
  update_shipping_icons(shopping_cart);
  update_tax_dom(total);
}

/// Using new version
function add_item_to_cart(name, price) {
  var item = make_cart_item(name, price);
  shopping_cart = add_item(shopping_cart, item);
  var total = calc_total(shopping_cart);
  set_cart_total_dom(total);
  update_shipping_icons(shopping_cart);
  update_tax_dom(total);
}
```

<br/>

 - 계산 분류하기
    - C: 장바구니(cart)에 대한 동작
    - I: 제품(item)에 대한 동작
    - B: 비즈니스 규칙
    - A: 배열 유틸리티
```JS
function add_element_last(array, elem) { // A
  var new_array = array.slice();
  new_array.push(elem);
  return new_array;
}

function add_item(cart, item) { // C
  return add_element_last(cart, item);
}

function make_cart_item(name, price) { // I
  return {
    name: name,
    price: price
  };
}

function calc_total(cart) { // C I B
  var total = 0;
  for(var i = 0; i < cart.length; i++) {
    var item = cart[i];
    total += item.price;
  }
  return total;
}

function gets_free_shipping(total, item_price) { // B
    return item_price + total >= 20;
}

function calc_tax(amount) { // B
  return amount * 0.10;
}
```

<br/>

### 연습 문제

 - update_shipping_icons() 함수
    - 해당 함수는 크기 떄문에 많은 일을 하고 있다.
        - 모든 버튼 가져오기 (구매하기 버튼 관련 동작)
        - 버튼 가지고 반복하기 (구매하기 버튼 관련 동작)
        - 버튼에 관련된 제품 가져오기 (구매하기 버튼 관련 동작)
        - 가져온 제품을 가지고 새 장바구니 만들기 (cart와 item 관련 동작)
        - 장바구니가 무료 배송이 필요한지 확인하기 (cart와 item 관련 동작)
        - 아이콘 표시하거나 감추기 (DOM 관련 동작)
```JS
// Before
function update_shipping_icons(cart) {
  var buy_buttons = get_buy_buttons_dom(); // 1. 모든 버튼 가져오기
  for(var i = 0; i < buy_buttons.length; i++) { // 2. 버튼 가지고 반복하기
    var button = buy_buttons[i];
    var item = button.item; // 3. 버튼에 관련된 제품 가져오기
    var new_cart = add_item(cart, item); // 4. 가져온 제품을 가지고 새 장바구니 만들기 (cart, item)
    if(gets_free_shipping(new_cart)) // 5. 장바구니가 무료 배송이 필요한지 확인하기 (cart, item)
      button.show_free_shipping_icon(); // 6. 아이콘 표시 (DOM)
    else
      button.hide_free_shipping_icon(); // 6. 아이콘 감추기 (DOM)
  }
}

// After
function update_shipping_icons(cart) { // 구매하기 버튼 관련 동작
  var buy_buttons = get_buy_buttons_dom(); // 1. 모든 버튼 가져오기
  for(var i = 0; i < buy_buttons.length; i++) { // 2. 버튼 가지고 반복하기
    var button = buy_buttons[i];
    var item = button.item; // 3. 버튼에 관련된 제품 가져오기
    var hasFreeShipping = gets_free_shipping_with_item(cart, item);
    set_free_shipping_icon(button, hasFreeShipping);
  }
}

function gets_free_shipping_with_item(cart, item) { // cart, item 관련 동작
  var new_cart = add_item(cart, item); // 4. 가져온 제품을 가지고 새 장바구니 만들기 (cart, item)
  return gets_free_shipping(new_cart); // 5. 장바구니가 무료 배송이 필요한지 확인하기 (cart, item)
}

function set_free_shipping_icon(button, isShown) { // DOM 관련 동작
  if(isShown)
    button.show_free_shipping_icon(); // 6. 아이콘 표시 (DOM)
  else
    button.hide_free_shipping_icon(); // 6. 아이콘 감추기 (DOM)
}
```

<br/>

## 정리

 - 일반적으로 암묵적 입력과 출력은 인자와 리턴값으로 바꿔 없애는 것이 좋다.
 - 설계는 엉켜있는 것을 푸는 것이다. 풀려있는 것은 언제든 다시 합칠 수 있다.
 - 엉켜있는 것을 풀어 각 함수가 하나의 일만 하도록 하면, 개념을 중심으로 쉽게 구성할 수 있다.
```JS
var shopping_cart = []; // A: 전역변수는 액션

function add_item_to_cart(name, price) { // A
  var item = make_cart_item(name, price);
  shopping_cart = add_item(shopping_cart, item); // 전역변수 읽기는 액션
  var total = calc_total(shopping_cart);
  set_cart_total_dom(total);
  update_shipping_icons(shopping_cart);
  update_tax_dom(total);
}

function update_shipping_icons(cart) {
  var buy_buttons = get_buy_buttons_dom();
  for(var i = 0; i < buy_buttons.length; i++) {
    var button = buy_buttons[i];
    var item = button.item;
    var new_cart = add_item(cart, item);
    if(gets_free_shipping(new_cart))
      button.show_free_shipping_icon(); // DOM 수정은 액션
    else
      button.hide_free_shipping_icon();
  }
}

function update_tax_dom(total) { // A
  set_tax_dom(calc_tax(total)); // DOM 수정은 액션
}

function add_element_last(array, elem) { // C
  var new_array = array.slice();
  new_array.push(elem);
  return new_array;
}

function add_item(cart, item) { // C
  return add_element_last(cart, item);
}

function make_cart_item(name, price) { // C
  return {
    name: name,
    price: price
  };
}

function calc_total(cart) { // C
  var total = 0;
  for(var i = 0; i < cart.length; i++) {
    var item = cart[i];
    total += item.price;
  }
  return total;
}

function gets_free_shipping(total, item_price) { // C
    return item_price + total >= 20;
}

function calc_tax(amount) { // C
  return amount * 0.10;
}
```
