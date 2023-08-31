class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    sayHello() {
        console.log('Hello!');
    }
}

class Developer extends Person {
    constructor(name, age, skill) {
        super(name, age);
        this.skill = skill;
    }

    coding() {
        console.log(`${this.skill}을 이용하여 코딩중입니다.`);
    }
}

var log = new Developer('로그', 20, 'Typescript');
log.coding(); // 코딩중입니다.
log.sayHello();