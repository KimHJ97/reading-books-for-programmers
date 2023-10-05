# CHAPTER 10. 일급 함수 I

 - 일급은 인자로 전달할 수 있다를 의미한다.
 - 고차 함수는 인자로 함수를 받거나 리턴값으로 함수를 리턴할 수 있는 함수를 말한다.

## 코드의 냄새: 함수 이름에 있는 암묵적 인자

함수 본문에서 사용하는 어떤 값이 함수 이름에 나타난다면 함수 이름에 있는 암묵적 인자는 코드의 냄새가 된다.  
 - setXxxByName의 이름을 갖는 함수들의 로직은 동일하다.
```JS
function setPriceByName(cart, name, price) {
  var item = cart[name];
  var newItem = objectSet(item, 'price', price);
  var newCart = objectSet(cart, name, newItem);
  return newCart;
}

function setShippingByName(cart, name, ship) {
  var item = cart[name];
  var newItem = objectSet(item, 'shipping', ship);
  var newCart = objectSet(cart, name, newItem);
  return newCart;
}

function setQuantityByName(cart, name, quant) {
  var item = cart[name];
  var newItem = objectSet(item, 'quantity', quant);
  var newCart = objectSet(cart, name, newItem);
  return newCart;
}

function setTaxByName(cart, name, tax) {
  var item = cart[name];
  var newItem = objectSet(item, 'tax', tax);
  var newCart = objectSet(cart, name, newItem);
  return newCart;
}

function objectSet(object, key, value) {
  var copy = Object.assign({}, object);
  copy[key] = value;
  return copy;
}
```

<br/>

## 리팩토링: 암묵적 인자 드러내기
암묵적 인자 드러내기는 암묵적 인자가 일급 값이 되도록 함수에 인자를 추가한다.  
이렇게 하면 잠재적 중복을 없애고 코드의 목적을 더 잘 표현할 수 있다.  

```JS
/// Before
function setPriceByName(cart, name, price) {
  var item = cart[name];
  var newItem = objectSet(item, 'price', price);
  var newCart = objectSet(cart, name, newItem);
  return newCart;
}

cart = setPriceByName(cart, "shoe", 13);
cart = setQuantityByName(cart, "shoe", 3);
cart = setShippingByName(cart, "shoe", 0);
cart = setTaxByName(cart, "shoe", 2.34);

/// After
function setFieldByName(cart, name, field, value) {
  var item = cart[name];
  var newItem = objectSet(item, field, value);
  var newCart = objectSet(cart, name, newItem);
  return newCart;
}

cart = setFieldByName(cart, "shoe", 'price', 13);
cart = setFieldByName(cart, "shoe", 'quantity', 3);
cart = setFieldByName(cart, "shoe", 'shipping', 0);
cart = setFieldByName(cart, "shoe", 'tax', 2.34);

// After 2
// 전달한 문자열이 올바른 문자열인지 검증한다.
var validItemFields = ['price', 'quantity', 'shipping', 'tax'];

function setFieldByName(cart, name, field, value) {
  if(!validItemFields.includes(field))
    throw "Not a valid item field: " + "'" + field + "'.";
  var item = cart[name];
  var newItem = objectSet(item, field, value);
  var newCart = objectSet(cart, name, newItem);
  return newCart;
}

// After 3
// 내부에서 정의한 필드명이 변경된 경우
var validItemFields = ['price', 'quantity', 'shipping', 'tax', 'number'];
var translations = { 'quantity': 'number' };

function setFieldByName(cart, name, field, value) {
  if(!validItemFields.includes(field))
    throw "Not a valid item field: '" + field + "'.";
  if(translations.hasOwnProperty(field))
    field = translations[field];
  var item = cart[name];
  var newItem = objectSet(item, field, value);
  var newCart = objectSet(cart, name, newItem);
  return newCart;
}
```

<br/>

## 리팩토링: 함수 본문을 콜백으로 바꾸기

함수 본문을 콜백으로 바꾸기는 함수 본문에 어떤 부분을 콜백으로 바꾼다.  
이렇게 하면 일급 함수로 어떤 함수에 동작을 전달할 수 있다.  

 - 코드가 비슷하지만 두 반복문이 하는 일이 다르다.
```JS
function cookAndEatFoods() {
  for(var i = 0; i < foods.length; i++) {
    var food = foods[i];
    cook(food);
    eat(food);
  }
}

cookAndEatFoods();

function cleanDishes() {
  for(var i = 0; i < dishes.length; i++) {
    var dish = dishes[i];
    wash(dish);
    dry(dish);
    putAway(dish);
  }
}

cleanDishes();
```

 - 함수 본문 콜백으로 변경
    - A. 코드를 함수로 감싸기
    - B. 더 일반적인 이름으로 바꾸기
    - C. 암묵적 인자 드러내기
    - D. 함수 추출하기
    - E. 암묵적 인자 드러내기
```JS
// 1. 지역 변수의 이름을 일반적인 이름으로 변경한다.
// 2. 암묵적 인자를 드러낸다.
function cookAndEatArray(array) {
  for(var i = 0; i < array.length; i++) {
    var item = array[i];
    cook(item);
    eat(item);
  }
}

cookAndEatFoods(foods);

function cleanArray(array) {
  for(var i = 0; i < array.length; i++) {
    var item = array[i];
    wash(item);
    dry(item);
    putAway(item);
  }
}

cleanDishes(dishes);


// 3. 반복문 안에 있는 본문을 분리한다.
// cookAndEatArray, cleanArray 호출하는 함수만 다르고 내용이 동일하다. (암묵적 인자)
function cookAndEatArray(array) {
  for(var i = 0; i < array.length; i++) {
    var item = array[i];
    cookAndEat(item);
  }
}

function cookAndEat(food) {
  cook(food);
  eat(food);
}

cookAndEatFoods(foods);

function cleanArray(array) {
  for(var i = 0; i < array.length; i++) {
    var item = array[i];
    clean(item);
  }
}

function clean(dish) {
  wash(dish);
  dry(dish);
  putAway(dish);
}

cleanDishes(dishes);


// 4. 암묵적 인자를 명시적인 인자로 표현한다.
function operateOnArray(array, f) {
  for(var i = 0; i < array.length; i++) {
    var item = array[i];
    f(item);
  }
}

function cookAndEat(food) {
  cook(food);
  eat(food);
}

function clean(dish) {
  wash(dish);
  dry(dish);
  putAway(dish);
}

cookAndEatFoods(foods, cookAndEat);

cleanDishes(dishes, clean);


// 5. 함수명 변경
function forEach(array, f) {
  for(var i = 0; i < array.length; i++) {
    var item = array[i];
    f(item);
  }
}

function cookAndEat(food) {
  cook(food);
  eat(food);
}

function clean(dish) {
  wash(dish);
  dry(dish);
  putAway(dish);
}

forEach(foods, cookAndEat);

forEach(dishes, clean);


// 6. 익명 함수 사용
function forEach(array, f) {
  for(var i = 0; i < array.length; i++) {
    var item = array[i];
    f(item);
  }
}

forEach(foods, function(food) {
  cook(food);
  eat(food);
});

forEach(dishes, function(dish) {
  wash(dish);
  dry(dish);
  putAway(dish);
});
```
