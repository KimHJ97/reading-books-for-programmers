# CHAPTER 4. 액션에서 계산 빼내기

테스트하기 쉽고 재사용 하기 좋은 코드를 만들기 위해 리팩토링한다.  
예제 코드에 기능을 조금 추가하고, 액션에서 계산을 빼낸다.  

<br/>

## MegaMart

MegaMart는 온라인 쇼핑몰로 경쟁력을 유지하고 있는 중요한 기능 중 하나는 쇼핑 중에 장바구니에 담겨 있는 제품의 금액 합계를 볼 수 있는 기능이 있다.  

 - 예제 코드
```JS
// 장바구니 제품과 금액 합계를 담고 있는 전역 변수
var shopping_cart = [];
var shopping_cart_total = 0;


function add_item_to_cart(name, price) {
  shopping_cart.push({ // 장바구니에 제품을 담기 위해 cart 배열에 레코드를 추가
    name: name,
    price: price
  });
  calc_cart_total(); // 장바구니 제품이 바뀌었기 때문에 금액 합계 업데이트
}

function calc_cart_total() {
  shopping_cart_total = 0;
  for(var i = 0; i < shopping_cart.length; i++) {
    var item = shopping_cart[i];
    shopping_cart_total += item.price;
  }
  set_cart_total_dom(); // 금액 합계를 반영하기 위해 DOM 업데이트
}
```

<br/>

 - 새로운 요구 사항
    - MegaMart는 구매 합계가 20 달러 이상이면 무료 배송을 해주려고 한다. 때문에, 장바구니에 넣으면 합계가 20달러가 넘는 제품의 구매 버튼 옆에 무료 배송 아이콘을 표시해준다.
```JS
function update_shipping_icons() {
  var buy_buttons = get_buy_buttons_dom(); // 페이지에 있는 모든 구매 버튼을 가져와 반복문 적용
  for(var i = 0; i < buy_buttons.length; i++) {
    var button = buy_buttons[i];
    var item = button.item;
    if(item.price + shopping_cart_total >= 20) // 무료 배송이 가능한지 확인
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}

function calc_cart_total() {
  shopping_cart_total = 0;
  for(var i = 0; i < shopping_cart.length; i++) {
    var item = shopping_cart[i];
    shopping_cart_total += item.price;
  }
  set_cart_total_dom();
  update_shipping_icons(); // 합계 금액이 바뀔 때마다 모든 아이콘을 업데이트 하기 위해 함수 추가
}
```

<br/>

 - 새로운 요구 사항
    - 장바구니의 금액 합계가 바뀔 때마다 세금을 다시 계산해야 한다.
```JS
function update_tax_dom() {
  set_tax_dom(shopping_cart_total * 0.10); // 금액 합계의 10%를 곱하고, DOM을 업데이트한다.
}

function calc_cart_total() {
  shopping_cart_total = 0;
  for(var i = 0; i < shopping_cart.length; i++) {
    var item = shopping_cart[i];
    shopping_cart_total += item.price;
  }
  set_cart_total_dom();
  update_shipping_icons();
  update_tax_dom(); // 페이지에 세금을 업데이트하기 위해 함수 추가
}
```

<br/>

### 테스트하기 쉽게 만들기

현재 코드는 비즈니스 규칙을 테스트하기 어렵고, 다른 곳에서 현재 코드를 재사용하기가 어렵다.  
장바구니 정보를 전역변수에서 읽어오고 있지만, 다른 곳에서는 데이터베이스에서 장바구니 정보를 읽어올 수도 있다.  
결과를 보여주기 위해 DOM을 직접 바꾸고 있지만, 다른 곳에서는 영수증 혹은 운송장을 출력해야 할 수 있다.  
 - DOM 업데이트와 비즈니스 규칙은 분리되어야 한다.
 - 전역 변수에 의존하지 않아야 한다.
 - 함수가 결과값을 리턴해야 한다.
```JS
function update_shipping_icons() {
  var buy_buttons = get_buy_buttons_dom();
  for(var i = 0; i < buy_buttons.length; i++) {
    var button = buy_buttons[i];
    var item = button.item;
    if(item.price + shopping_cart_total >= 20) // 무료 배송이 가능한지 확인
      button.show_free_shipping_icon(); // ❌ 해당 함수는 DOM이 있어야 실행이 가능하다.
    else
      button.hide_free_shipping_icon(); // ❌ 해당 함수는 DOM이 있어야 실행이 가능하다.
  }
} // ❌ 리턴값이 없기 떄문에 결과를 받을 방법이 없다.
```

<br/>

### 액션과 계산, 데이터 구분하기

먼저 해야 할 일은 각 함수가 액션과 계산, 데이터 중 어떤 것인지 구분하는 것이다.  

 - 현재 모든 변수와 함수는 액션이다.
```JS
var shopping_cart = []; // A: 전역변수는 변경 가능하기 떄문에 액션이다.
var shopping_cart_total = 0; // A: 전역변수는 변경 가능하기 떄문에 액션이다.

function add_item_to_cart(name, price) { // A
  shopping_cart.push({ // 전역 변수를 바꾸는 것은 액션이다.
    name: name,
    price: price
  });
  calc_cart_total();
}

function update_shipping_icons() { // A
  var buy_buttons = get_buy_buttons_dom(); // DOM 에서 읽는 것은 액션이다.
  for(var i = 0; i < buy_buttons.length; i++) {
    var button = buy_buttons[i];
    var item = button.item;
    if(item.price + shopping_cart_total >= 20)
      button.show_free_shipping_icon(); // DOM 을 바꾸는 것은 액션이다.
    else
      button.hide_free_shipping_icon(); // DOM 을 바꾸는 것은 액션이다.
  }
}

function update_tax_dom() { // A
  set_tax_dom(shopping_cart_total * 0.10); // DOM 을 바꾸는 것은 액션이다.
}

function calc_cart_total() { // A
  shopping_cart_total = 0; // 전역 변수를 바꾸는 것은 액션이다.
  for(var i = 0; i < shopping_cart.length; i++) {
    var item = shopping_cart[i];
    shopping_cart_total += item.price;
  }
  set_cart_total_dom();
  update_shipping_icons();
}
```

<br/>

### 함수에는 입력과 출력이 있다.

모든 함수에는 입력과 출력이 있다.  
입력은 함수가 계산을 하기 위한 외부 정보이고, 출력은 함수 밖으로 나오는 정보나 어떤 동작이다.  

 - 입력과 출력은 명시적 혹은 암묵적일 수 있다.
    - 함수에 암묵적 입력과 출력이 있으면 액션이 된다. 즉, 암묵적 입력과 출력을 없애면 계산이 된다.
    - 명시적 입력: 인자
    - 암묵적 입력: 인자 외 다른 입력
    - 명시적 출력: 리턴값
    - 암묵적 출력: 리턴값 외 다른 출력
```JS
var total = 0;

function add_to_total(amount) { // 인자는 명시적 입력이다.
  console.log("Old total: " + total); // 전역변수를 읽는 것은 암묵적 입력이다. 또, 콘솔에 출력하는 것은 암묵적 출력이다.
  total += amount; // 전역변수를 바꾸는 것은 암묵적 출력이다.
  return total; // 리턴값은 명시적 출력이다.
}
```

<br/>

### 액션에서 계산 빼내기

 - 장바구니 합계 함수
```JS
/* 1. 서브루틴 추출하기 */

/// Original
function calc_cart_total() {
  shopping_cart_total = 0;
  for(var i = 0; i < shopping_cart.length; i++) {
    var item = shopping_cart[i];
    shopping_cart_total += item.price;
  }

  set_cart_total_dom();
  update_shipping_icons();
  update_tax_dom();
}

/// Extracted
function calc_cart_total() {
  calc_total();
  set_cart_total_dom();
  update_shipping_icons();
  update_tax_dom();
}

function calc_total() {
  shopping_cart_total = 0; // 출력 (암묵적)
  for(var i = 0; i < shopping_cart.length; i++) { // 입력 (암묵적)
    var item = shopping_cart[i];
    shopping_cart_total += item.price; // 출력 (암묵적)
  }
}

/* 2. 명시적 입출력으로 변경하기 */
// 현재, calc_total()은 shopping_cart_total 전역변수값을 바꾸는 출력 2개와 shopping_cart 값을 읽는 입력 1개가 있다.

/// Eliminated outputs (암묵적 출력 2개 없애기)
function calc_cart_total() {
  shopping_cart_total = calc_total(); // 리턴값을 받아 전역변수에 할당한다.
  set_cart_total_dom();
  update_shipping_icons();
  update_tax_dom();
}

function calc_total() {
  var total = 0; // 지역변수로 변경한다.
  for(var i = 0; i < shopping_cart.length; i++) {
    var item = shopping_cart[i];
    total += item.price;
  }
  return total; // 지역변수를 리턴한다. (출력: 명시적)
}

/// Eliminated inputs (암묵적 입력 없애기)
function calc_cart_total() {
  shopping_cart_total = calc_total(shopping_cart);
  set_cart_total_dom();
  update_shipping_icons();
  update_tax_dom();
}

function calc_total(cart) { // 전역변수 대신 인자를 받는다. (입력: 명시적)
  var total = 0;
  for(var i = 0; i < cart.length; i++) {
    var item = cart[i];
    total += item.price;
  }
  return total;
}
```

<br/>

 - 장바구니 추가 함수
```JS
/* 1. 함수 추출하기 */

/// Original
function add_item_to_cart(name, price) {
  shopping_cart.push({
    name: name,
    price: price
  });

  calc_cart_total();
}

/// Extracted
function add_item_to_cart(name, price) {
  add_item(name, price);
  calc_cart_total();
}

function add_item(name, price) {
  shopping_cart.push({ // 전역변수 shopping_cart를 읽고, push() 함수로 전역변수 배열을 바꾸고 있다.
    name: name,
    price: price
  });
}

/* 2. 명시적 입출력으로 변경하기 */
// 현재, add_item()은 shopping_cart를 전역변수값을 가져와 쓰고 있다.

/// Eliminated input (암묵적 입력 없애기)
function add_item_to_cart(name, price) {
  add_item(shopping_cart, name, price); // 아직, 전역변수를 인자로 넘기고, push()로 암묵적 출력이 되고 있다.
  calc_cart_total();
}

function add_item(cart, name, price) { // 전역변수 대신 인자를 사용하도록 한다.
  cart.push({
    name: name,
    price: price
  });
}

/// Eliminated output (암묵적 출력 없애기)
function add_item_to_cart(name, price) {
  shopping_cart = add_item(shopping_cart, name, price);
  calc_cart_total();
}

function add_item(cart, name, price) {
  var new_cart = cart.slice(); // 전달받은 전역변수 shopping_cart를 바꾸는 대신 복사본을 만들고, 
  new_cart.push({ // 복사본에 추가하고,
    name: name,
    price: price
  });
  return new_cart; // 복사본을 리턴한다.
}
```

<br/>

### 연습 문제

 - 세금 계산 함수
```JS
// 원본 코드
function update_tax_dom() {
  set_tax_dom(shopping_cart_total * 0.10);
}

// 1. 함수 추출
function update_tax_dom() {
  set_tax_dom(calc_tax());
}

function calc_tax() {
  return shopping_cart_total * 0.10;
}

// 2. 암묵적 입력 없애기
function update_tax_dom() {
  set_tax_dom(calc_tax(shopping_cart_total));
}

function calc_tax(amount) {
  return amount * 0.10;
}
```

 - 무료 배송인지 확인 함수
```JS
// 원본 코드
function update_shipping_icons() {
  var buy_buttons = get_buy_buttons_dom();
  for(var i = 0; i < buy_buttons.length; i++) {
    var button = buy_buttons[i];
    var item = button.item;
    if(item.price + shopping_cart_total >= 20)
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}

// 1. 함수 추출
function update_shipping_icons() {
  var buy_buttons = get_buy_buttons_dom();
  for(var i = 0; i < buy_buttons.length; i++) {
    var button = buy_buttons[i];
    var item = button.item;
    if(gets_free_shipping(item.price))
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}

function gets_free_shipping(item_price) {
    return item_price + shopping_cart_total >= 20;
}

// 2. 암묵적 입력 없애기
function update_shipping_icons() {
  var buy_buttons = get_buy_buttons_dom();
  for(var i = 0; i < buy_buttons.length; i++) {
    var button = buy_buttons[i];
    var item = button.item;
    if(gets_free_shipping(shopping_cart_total, item.price))
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}

function gets_free_shipping(total, item_price) {
    return item_price + total >= 20;
}
```

<br/>

## 전체 코드 비교

 - 액션은 암묵적인 입력 또는 출력을 가지고 있다.
 - 계산은 암묵적인 입력이나 출력이 없어야 한다.
 - 공유 변수(전역변수같은)는 일반적으로 암묵적 입력 또는 출력이다.
 - 암묵적 입력은 인자로 바꿀 수 있다.
 - 암묵적 출력은 리턴값으로 바꿀 수 있다.
 - 함수형 원칙을 적용하면 액션은 줄어들고 계산은 늘어난다.
```JS
var shopping_cart = []; // A
var shopping_cart_total = 0; // A

function add_item_to_cart(name, price) { // A
  shopping_cart = add_item(shopping_cart, name, price); // 전역 변수를 읽는 것은 액션이다.
  calc_cart_total();
}
function update_shipping_icons() { // A
  var buy_buttons = get_buy_buttons_dom();
  for(var i = 0; i < buy_buttons.length; i++) {
    var button = buy_buttons[i];
    var item = button.item;
    if(gets_free_shipping(shopping_cart_total, item.price)) // 전역 변수를 읽는 것은 액션이다.
      button.show_free_shipping_icon();
    else
      button.hide_free_shipping_icon();
  }
}
function update_tax_dom() { // A
  set_tax_dom(calc_tax(shopping_cart_total)); // 전역 변수를 읽는 것은 액션이다.
}

function add_item(cart, name, price) { // C
  var new_cart = cart.slice(); // 배열의 복사본을 만들어 사용한다.
  new_cart.push({
    name: name,
    price: price
  });
  return new_cart;
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
