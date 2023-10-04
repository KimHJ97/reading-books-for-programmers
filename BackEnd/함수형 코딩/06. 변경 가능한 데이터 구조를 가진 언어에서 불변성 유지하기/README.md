# CHAPTER 6. 변경 가능한 데이터 구조를 가진 언어에서 불변성 유지하기

데이터가 바뀌지 않도록 하기 위해 카피-온-라이트를 적용하며, 불변성에 대해 더 자세히 알아본다.  

<br/>

## 동작을 읽기, 쓰기 또는 둘 다로 분류하기

동작을 읽기 또는 쓰기 또는 둘 다 하는 것으로 분류할 수 있다.  
읽기 동작은 데이터를 바꾸지 않고 정보를 꺼내는 것이다. 데이터가 바뀌지 않기 때문에 다루기 쉽다. 특별히 해야 할 일이 없다.  
쓰기 동작은 데이터를 변경한다. 바뀌는 값은 어디서 사용될지 모르기 때문에 바뀌지 않도록 원칙이 필요하다.  

```
 - 장바구니 동작
1. 제품 개수 가져오기 [읽기]
2. 제품 이름으로 제품 가져오기 [읽기]
3. 제품 추가하기 [쓰기]
4. 제품 이름으로 제품 빼기 [쓰기]
5. 제품 이름으로 제품 구매 수량 바꾸기 [쓰기]

 - 제품에 대한 동작
1. 가격 설정하기 [쓰기]
2. 가격 가져오기 [읽기]
3. 이름 가져오기 [읽기]
```

<br/>

## 카피-온-라이트 원칙 세 단계

카피-온-라이트는 세 단계로 되어있다.  
카피-온-라이트는 데이터를 바꾸지 않고 정보를 리턴한다. 즉, 쓰기를 읽기로 바꾼다.  
 - A. 복사본 만들기
 - B. 복사본 변경하기
 - C. 복사본 리턴하기
```JS
function add_element_last(array, elem) {
    var new_array = array.slice(); // 1. 복사본 만들기
    new_array.push(elem); // 2. 복사본 바꾸기
    return new_array; // 3. 복사본 리턴하기
}
```

### 카피-온-라이트로 쓰기를 읽기로 바꾸기

 - 제품 이름으로 장바구니에서 제품 빼는 함수
    - 함수에 전역변수 shopping_cart를 넘기면 전역변수인 장바구니가 변경된다.
```JS
function remove_item_by_name(cart, name) {
  var idx = null;
  for(var i = 0; i < cart.length; i++) {
    if(cart[i].name === name)
      idx = i;
  }
  if(idx !== null)
    cart.splice(idx, 1);
}
```

<br/>

 - 카피-온-라이트 적용하기
```JS
// 1. 복사본 만들기
function remove_item_by_name(cart, name) {
  var new_cart = cart.slice();
  var idx = null;
  for(var i = 0; i < cart.length; i++) {
    if(cart[i].name === name)
      idx = i;
  }
  if(idx !== null)
    cart.splice(idx, 1);
}

// 2. 복사본 변경하기
function remove_item_by_name(cart, name) {
  var new_cart = cart.slice();
  var idx = null;
  for(var i = 0; i < new_cart.length; i++) {
    if(new_cart[i].name === name)
      idx = i;
  }
  if(idx !== null)
    new_cart.splice(idx, 1);
}

// 3. 복사본 리턴하기
function remove_item_by_name(cart, name) {
  var new_cart = cart.slice();
  var idx = null;
  for(var i = 0; i < new_cart.length; i++) {
    if(new_cart[i].name === name)
      idx = i;
  }
  if(idx !== null)
    new_cart.splice(idx, 1);
  return new_cart;
}

// 4. 호출하는 곳 변경하기
// 전역변수인 장바구니를 직접 바꾸지 않는다. 때문에, 전역변수에 할당해 줘야 한다.
    // Before
function delete_handler(name) {
  remove_item_by_name(shopping_cart, name);
  var total = calc_total(shopping_cart);
  set_cart_total_dom(total);
  update_shipping_icons(shopping_cart);
  update_tax_dom(total);
}
    // After
function delete_handler(name) {
  shopping_cart = remove_item_by_name(shopping_cart, name);
  var total = calc_total(shopping_cart);
  set_cart_total_dom(total);
  update_shipping_icons(shopping_cart);
  update_tax_dom(total);
}
```

<br/>

 - 재사용하기 쉽도록 일반화하기
```JS
/// Before
function removeItems(array, idx, count) {
  array.splice(idx, count);
}

/// After: Copy-on-write
function removeItems(array, idx, count) {
  var copy = array.slice();
  copy.splice(idx, count);
  return copy;
}

// Before
function remove_item_by_name(cart, name) {
  var new_cart = cart.slice();
  var idx = null;
  for(var i = 0; i < new_cart.length; i++) {
    if(new_cart[i].name === name)
      idx = i;
  }
  if(idx !== null)
    removeItems(new_cart, idx, 1);
  return new_cart;
}

// After
function remove_item_by_name(cart, name) {
  var idx = null;
  for(var i = 0; i < cart.length; i++) {
    if(cart[i].name === name)
      idx = i;
  }
  if(idx !== null)
    return removeItems(cart, idx, 1);
  return cart;
}
```

<br/>

## 연습 문제

메일링 리스트에 연락처를 추가한다. 이메일 주소를 전역변수인 리스트에 추가한다.  

 - add_contact()가 전역변수에 접근하면 안 된다. mailing_list를 인자로 받아 복사하고 변경한 다음 리턴해야 한다.
 - add_contact() 함수의 리턴값을 mailing_list 전역변수에 할당해야 한다.
```JS
// Before
var mailing_list = [];

function add_contact(email) {
  mailing_list.push(email);
}

function submit_form_handler(event) {
  var form = event.target;
  var email = form.elements["email"].value;
  add_contact(email);
}

// After
var mailing_list = [];

function add_contact(mailing_list, email) {
  var list_copy = mailing_list.slice(); // 1. 복사본 만들기
  list_copy.push(email); // 2. 복사본 변경하기
  return list_copy; // 3. 복사본 리턴하기
}

function submit_form_handler(event) {
  var form = event.target;
  var email = form.elements["email"].value;
  mailing_list = add_contact(mailing_list, email); // 4. 호출하는 곳 변경하기
}
```

<br/>

## 쓰기와 읽기를 하는 동작 처리

어떤 동작은 읽고 변경하는 일을 동시에 한다.  
카피-온-라이트에서는 쓰기를 읽기오 바꾸었다.  
쓰기와 읽기를 동시에 하는 동작에 대해서는 두 가지 접근 방법이 있다.  
첫 번째는 읽기와 쓰기 함수로 각각 분리하는 함수 분리 방법이 있고,  
두 번째는 함수에서 값을 두 개 리턴하는 방법이 있다.  

 - 예제 코드
    - shift() 메서드는 값을 바꾸는 동시에 배열에 첫 번째 항목을 리턴한다.
    - 즉, 변경하면서 읽는 동작을 한다.
```JS
var a = [1, 2, 3, 4];
var b = a.shift();
console.log(b); // 1
console.log(a); // [2, 3, 4]
```

 - 읽기와 쓰기 동작으로 분리하기
    - first_element(): shift() 메서드의 읽기 동작은 값을 단순히 리턴하는 동작이다. 즉, 배열에 첫 번째 항목을 리턴한다.
    - drop_first(): 전형적인 카피-온-라이트 방식으로 복사본을 만들고 변경하고 리턴한다.
```JS
function first_element(array) {
  return array[0];
}

function drop_first(array) {
  var array_copy = array.slice();
  array_copy.shift();
  return array_copy;
}
```

 - 값을 두 개 리턴하는 함수로 만들기
```JS
function shift(array) {
  return array.shift();
}

/// Copy-on-write
function shift(array) {
  var array_copy = array.slice();
  var first = array_copy.shift();
  return {
    first : first,
    array : array_copy
  };
}

/// Another option
function shift(array) {
  return {
    first : first_element(array),
    array : drop_first(array)
  };
}
```

<br/>

## 연습 문제

 - 카피-온-라이트 함수 만들기
```JS
/* Array.shift() */
// 1. 읽기와 쓰기 함수 분리
function first_element(array) { // 읽기
  return array[0];
}
function drop_first(array) { // 쓰기
  var array_copy = array.slice();
  array_copy.shift();
  return array_copy;
}

// 2. 값 두 개를 리턴하는 함수로 분리
function shift(array) {
  var array_copy = array.slice();
  var first = array_copy.shift();
  return {
    first : first,
    array : array_copy
  };
}

/* Array.pop() */
// 1. 읽기와 쓰기 함수 분리
function last_element(array) { // 읽기
  return array[array.length - 1];
}
function drop_last(array) { // 쓰기
  var array_copy = array.slice();
  array_copy.pop();
  return array_copy;
}

// 2. 값 두 개를 리턴하는 함수로 분리
function pop(array) {
  var array_copy = array.slice();
  var first = array_copy.pop();
  return {
    first : first,
    array : array_copy
  };
}

/* Array.push(elem) */
function push(array, elem) {
  var copy = array.slice();
  copy.push(elem);
  return copy;
}
```

<br/>

## 객체에 대한 카피-온-라이트

배열은 slice() 메서드로 복사본을 만들 수 있었다. 하지만, 자바스크립트 객체에는 slice() 메서드가 없다.  
자바스크립트 객체에는 Object.assign() 메서드가 있는데 해당 메서드를 이용할 수 있다.  

 - 객체에 대한 카피-온-라이트 동작도 배열과 동일하게 복사본을 만들고, 변경하고 리턴하면 된다.
```JS
// Before
function setPrice(item, new_price) {
  item.price = new_price;
}

// After
function setPrice(item, new_price) {
  var item_copy = Object.assign({}, item);
  item_copy.price = new_price;
  return item_copy;
}
```

<br/>

## 연습 문제

 - 카피-온-라이트 함수 만들기
```JS
// objectSet()
function objectSet(object, key, value) {
  var copy = Object.assign({}, object);
  copy[key] = value;
  return copy;
}

// 객체의 키로 키/값 쌍을 지우는 delete 연산
function objectDelete(object, key) {
  var copy = Object.assign({}, object);
  delete copy[key];
  return copy;
}
```

 - 중첩된 쓰기를 읽기로 바꾸기
    - 중첩 데이터: 데이터 구조 안에 데이터 구조가 있는 것을 말한다.
    - 얕은 복사: 중첩 데이터에서 최상위 데이터 구조만 복사한다.
    - 구조적 공유: 두 중첩된 데이터 구조에서 안쪽 데이터가 같은 데이터를 참조한다.
    - [Object, Object, ..]을 slice()로 복사하면 얕은 복사가 된다. 즉, 원본 배열과 복사된 배열안에 가리키는 Object는 모두 동일하다.
```JS
// Before
function setPriceByName(cart, name, price) {
  for(var i = 0; i < cart.length; i++) {
    if(cart[i].name === name)
      cart[i].price = price;
  }
}

// After
function setPriceByName(cart, name, price) {
  var cartCopy = cart.slice(); // 배열 복사
  for(var i = 0; i < cartCopy.length; i++) {
    if(cartCopy[i].name === name)
      cartCopy[i].price = setPrice(cartCopy[i], price);
  }
  return cartCopy;
}

function setPrice(item, new_price) {
  var item_copy = Object.assign({}, item); // 객체 복사
  item_copy.price = new_price;
  return item_copy;
}
```

<br/>

## 요점 정리

 - 함수형 프로그래밍에서 불변 데이터가 필요하다. 계산에서는 변경 가능한 데이터에 쓰기를 할 수 없다.
 - 카피-온-라이트는 데이터를 불변형으로 유지할 수 있는 원칙이다. 복사본을 만들고 원본 대신 복사본을 변경하는 것을 말한다.
 - 카피-온-라이트는 값을 변경하기 전에 얕은 복사를 한다. 그리고 리턴한다. 이렇게 하면 통제할 수 있는 범위에서 불변성을 구현할 수 있다.
 - 보일러 플레이트 코드를 줄이기 위해 기본적인 배열과 객체 동작에 대한 카피-온-라이트 버전을 만들어 두는 것이 좋다.
