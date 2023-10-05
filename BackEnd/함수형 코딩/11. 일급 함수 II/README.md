# CHAPTER 11. 일급 함수 II

## 배열에 대한 카피-온-라이트 리팩토링

함수 본문을 콜백으로 바꾸기를 배열에 대한 카피-온-라이트 함수에 적용해본다.  

 - 예제 코드
    - 앞부분과 뒷부분 모두 복사본을 만들고, 반환하는 내용으로 동일하다.
    - 다른 부분은 본문에 한 라인뿐이다.
```JS
function arraySet(array, idx, value) {
  var copy = array.slice(); // 앞부분
  copy[idx] = value; // 본문
  return copy; // 뒷부분
}
function push(array, elem) {
  var copy = array.slice();
  copy.push(elem);
  return copy;
}
function drop_last(array) {
  var array_copy = array.slice();
  array_copy.pop();
  return array_copy;
}
function drop_first(array) {
  var array_copy = array.slice();
  array_copy.shift();
  return array_copy;
}
```

 - 리팩토링
```JS
// 1. 함수 빼내기
function arraySet(array, idx, value) {
  return withArrayCopy(array);
}

function withArrayCopy(array) {
  var copy = array.slice();
  copy[idx] = value;
  return copy;
}

// 2. 콜백 빼내기
function arraySet(array, idx, value) {
  return withArrayCopy(array, function(copy) {
    copy[idx] = value;
  });
}

function withArrayCopy(array, modify) {
  var copy = array.slice();
  modify(copy);
  return copy;
}

// 그 외
function push(array, elem) {
  return withArrayCopy(array, function(copy) {
    copy.push(elem);
  });
}
function drop_last(array) {
  return withArrayCopy(array, function(copy) {
    copy.pop();
  });
}
function drop_first(array) {
  return withArrayCopy(array, function(copy) {
    copy.shift();
  });
}
```

 - 객체 리팩토링 예제
```JS
// Before
function objectSet(object, key, value) {
  var copy = Object.assign({}, object);
  copy[key] = value;
  return copy;
}
function objectDelete(object, key) {
  var copy = Object.assign({}, object);
  delete copy[key];
  return copy;
}

/// After
function withObjectCopy(object, modify) {
  var copy = Object.assign({}, object);
  modify(copy);
  return copy;
}
function objectSet(object, key, value) {
  return withObjectCopy(object, function(copy) {
    copy[key] = value;
  });
}
function objectDelete(object, key) {
  return withObjectCopy(object, function(copy) {
    delete copy[key];
  });
}
```

 - 조건문 콜백 리팩토링 만들어보기
```JS
// if 문
function when(test, then) {
  if(test)
    return then();
}

when(hasItem(cart, "shoes"), function() {
  return setPriceByName(cart, "shoes", 0);
});

// if else 문
function IF(test, then, ELSE) {
  if(test)
    return then();
  else
    return ELSE();
}

IF(array.length === 0, function() {
  console.log("Array is empty");
}, function() {
  console.log("Array has something in it.");
});

IF(hasItem(cart, "shoes"), function() {
  return setPriceByName(cart, "shoes", 0);
}, function() {
  return cart; // unchanged
});
```
