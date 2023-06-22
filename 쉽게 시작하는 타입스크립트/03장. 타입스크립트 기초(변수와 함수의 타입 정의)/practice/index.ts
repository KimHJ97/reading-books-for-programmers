// 3.2.1 문자열 타입: string
const name: string = 'log';

// 3.2.2 숫자 타입: number
const age: number = 100;

// 3.2.3 진위 타입: boolean
const isLogin: boolean = false;

// 3.2.4 객체 타입: object
const person: object = {
    name: 'log',
    age: 100
};

// 3.2.5 배열 타입: Array
var companies: Array<string> = ['네이버', '삼성', '인프런'];
var companies: string[] = ['네이버', '삼성', '인프런'];
var cards: Array<number> = [1, 2, 3, 4];
var cards: number[] = [1, 2, 3, 4];

// 3.2.6 튜플 타입: tuple
var items: [string, number] = ['hi', 100];

// 3.2.7 any
var myName: any = 'log';
myName = 100;

// 3.2.8 null과 undefined
// null 타입 지정하고, null 값 할당
var empty: null = null;
// undefined 지정하고, 아무 값도 할당하지 않음 (초깃값 undefined)
var nothingAssigned: undefined;

export {};