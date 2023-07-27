/* __________Data Types__________ 
'let' is used for variables, 'const' for constants:
Using 'var' can lead to unexpected results because it is function-scoped - defined throughout the function in which it is declared.
'let' and 'const' are block-scoped, defined only within the code block in which they are declared.
*/
let variable; // Undefined
variable = 0; // Now defined (of type Number)

const nothing = null; // Null
const num = 10; // Number
const str = "Hello"; // String
const bool = true; // Boolean
let obj = {name: "John", age: 30}; // Object

/* A symbol is a unique identifier (like a key) used to access object properties.
No two symbols are the same even if they have the same description.
*/
const sym = Symbol(); // Symbol

// Declaring multiple variables in a single line:
let firstName = "John", lastName = "Doe", age = 35;


// String formatting:
console.log(`My name is ${firstName} ${lastName} and I am ${age} years old.`);




/* __________Conditions__________ */
if (age >= 18) {
    console.log("I am an adult.");
} else if (age >= 13) {
    console.log("I am a teenager.");
} else {
    console.log("I am a child.");
}


switch(age % 2) {
    case 0: 
        console.log("My age is even."); 
        break;
    case 1:
        console.log("My age is odd.");
        break;
    

    // 'default' runs if no case matches. No need for break since it's tested last:
    default:
        console.log("num1 is not a number");
}


// Ternary operator (variable = expression ? value_if_true : value_if_false):
let status = age >= 18 ? 'Adult' : 'Minor';
console.log(status); // Outputs: 'Adult'




/* __________Loops___________ */
for (let i=0; i<5; i++) {
    console.log(i);
}


let i = 0;
while (i < 5){
    console.log(i);
    i++;
}


i = 0;
// Do while loop, condition checked at the end so runs at least once:
do {
    console.log(i);
    i++;
} while (i < 5);


let names = ["John", "Rob", "Dan"];
names.forEach(function(name) { // 'name' parameter takes the value of each array element.
    console.log("Mr. " + name);
});

// Arrow notation can be used for functions with a single statement (like the one above):
names.forEach(name => console.log(name + " Smith"));

// For of loop can be used similarly to forEach:
for (let name of names) {
    console.log(name + "!");
}

// The map function creates a new array with the results of calling a function for every element:
names = names.map(function(name){return "Mr. " + name;});

// It can also be used with arrow notation:
names = names.map(name => name + " Smith!");
console.log(names); 




/* ___________Functions___________ 
In JavaScript, functions are first-class objects, meaning they can be:
    1) Assigned to a variable.
    2) Passed as an argument to another function.
    3) Returned from a function.
    (The final two make a function a higher-order function.)

*/
function add(x, y) {return x + y;}

// Arrow function equivalent:
add = (x, y) => x + y;

// Default parameter value syntax:
function add(x, y, z=0) {return x + y + z;}

/* Using the 'function' keyword is called a declaration.
Declarations are hoisted to the top of the file, so they can be called before they are defined.
Calling 'sayHello()' before it is defined (this works):
*/
sayHello()
function sayHello() {console.log("Hello");}

/* Creating a function expression is setting the value of a variable (or constant) as the function.
This is NOT hoisted, so it must be defined before it is called.
Generally, declarations should be used for global functions, and expressions should be used for local functions.
*/

// sayGoodbye(); This will throw an error since the function is not defined yet:
const sayGoodbye = function() {console.log("Goodbye");}
sayGoodbye(); // Now we can call the function.




/* __________Error Handling__________ */
try {
    // Some code that throws an error:
    throw new Error('Some Error');

} catch (error) {
    // Handling the error:
    console.log(error.message);
} finally {
    /* This code executes regardless of whether an error is thrown.
    It's useful for closing files, database connections, etc.
    The reason that finally is useful instead of just putting the code after the try-catch block is that
    variables declared in the try-catch block using 'let' or 'const' are not accessible outside of it, 
    due to the block-scope of these keywords.
    */
    console.log("This code runs no matter what");
}


// Throwing custom errors:
function divide(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b;
}

try {
    console.log(divide(10, 0));
} catch (error) {
    console.log(error.message);
}




/* __________Promises & Async / Await__________ 
A promise is an object that may produce a single value some time in the future, 
either a resolved value, or a reason that it’s not resolved (rejected).
*/

// Creating a promise:
let promise = new Promise((resolve, reject) => {
    let condition = true;

    // The promise can be resolved or rejected based on some condition:
    if(condition) {
        resolve("Promise is resolved");
    } else {
        reject("Promise is rejected");
    }
});


// If the promise is resolved, the then method is called, which takes a callback function as an argument:
promise.then(message => console.log(message))

// If the promise is rejected, the catch method is called, which also takes a callback function as an argument:
promise.catch(error => console.log(error));


/* Async/Await makes it easier to work with promises. 
An async function always returns a promise.
*/

// Declaring an async function:
async function asyncFunction() {
    try {
        // The await keyword can be used to wait for a promise to be resolved or rejected:
        let response = await promise;
        console.log(response);
    
    // If the promise is rejected, the catch block is executed:
    } catch (error) {
        console.log(error);
    }
}

// Calling the async function:
asyncFunction();




/* __________Classes__________ 
Classes are primarily syntactic sugar for the prototypal inheritance model.
There are no explicit access modifiers like public, private, protected (meaning attribute can be accessed from a subclass).
*/

class Rectangle {
    constructor(height, width){
        this.height = height;
        this.width = width;
    }
    // No 'function' keyword for methods:
    area() {return this.height * this.width;}
}

// Inheritance:
class Square extends Rectangle {
    // Polymorphism through overriding:
    constructor(side){super(side, side);}
}

// Instantiation:
const mySquare = new Square(10);
console.log(mySquare.area());

/* __________Prototypal Inheritance__________
Every non-primitive inherits from the Object class.
This is the typical syntax to define an object - a collection of key-value pairs which themselves can point to other objects or functions: 
*/
const animal = {
    dna: 123,
    legs: {front: 2, back: 2},
    // This is a method:
    sleep() {console.log("zzz");}
};

/* A prototype is like a parent class.
When the prototype of something is null, it is a primitive (we reached the end of the prototype chain).
*/
const animal_prototype = Object.getPrototypeOf(animal); // Object
const prototype_of_prototype_of_animal = Object.getPrototypeOf(animal_prototype); // null

const dog = {
    name: "Fido",
    color: "Brown",
    bark() {console.log("woof");}
};

// We can have the dog object inherit from animal by extending the prototype chain:
Object.setPrototypeOf(dog, animal);
const prototype_of_dog = Object.getPrototypeOf(dog); // animal




/* __________Destructuring__________ 
We can use the typical syntax to access the properties of an object:
const name = dog.name;
const color = dog.color;
*/

// Alternatively, we can use destructuring:
const {name, color} = dog; // This assigns the property values to the variables. The identifiers must match the property names.

// If we want different variable names, we can use this syntax:
const {name: dogName, age: dogAge} = dog;

const arr = [1, 2, 3];
// Obviously, there are no property names, so the variables are assigned the values in order:
//const [first, second, third] = arr; 

// If we do not want a variable for an item of a certain index, we can leave it blank:
let [first, , third] = arr; 

// If we only want a few items, it is better to access the array elements directly instead of using destructuring:
first = arr[0];




/* __________Spread Operator__________ 
The spread operator ('...') is used when we want to copy the properties of an object into another object:
*/
const firstHalf = {a: 1, b: 2, c: 3};
const secondHalf = {c: 4, d: 5};

// The last argument has the highest priority, so the c property will be 4:
const combined = Object.assign({}, firstHalf, secondHalf); 

// This can be implemented more concisely using the spread operator:
// Again, the last argument has the highest priority:
const combined2 = {...firstHalf, ...secondHalf};


/* Alternatively, we can have one object in the definition of the other object, which has the same effect.
If the object comes at the top, properties defined afterwards will be overridden.
If it comes at the bottom, it will override the properties defined before it.
*/
const combined3 = {...firstHalf, c: 4, d: 5}; // c: 4 overrides c: 3




/* __________Optional Chaining__________ 
A common problem is that we may want to access a property of an object,
but the object may be null or undefined, or the property may not exist, resulting in an error:
*/
obj = undefined;

// This syntax can be used to check if the object is null or undefined before trying to access the property:
if (obj) {obj.someProperty;}


// Using a question mark after the object name will check if the object is null or undefined before trying to access the property:
// In such a case, the expression will evaluate to undefined instead of throwing an error:
obj?.someProperty; 

// This syntax can also be used when accessing items of an array:
arr?.[0];

// It can also be used when calling a function:
function foo(a, b) {}
foo?.(1, 2); 




/* __________Nullish Coalescence__________ 
A value is truthy or falsy depending on whether it evaluates to true or false in a boolean context.

Truthy Values:
    1) true
    2) object (can be empty)
    3) array (can be empty)
    4) non-empty string
    5) any number except 0

Falsy Values:
    1) false
    2) null
    3) undefined
    4) empty string
    5) 0
*/

const x = ""; // falsy


/* The nullish coalescing operator (??) returns the right-hand side operand if the left-hand side operand is null or undefined:
variable = expression ?? value_if_null_or_undefined:
*/
const val = x ?? "default value"; // "default value" since x is falsy




/* __________Higher Order Functions__________ 
The following are higher order functions:
    1) Functions that take other functions as arguments.
    2) Functions that return functions.
*/

// This calls the function that is passed into the wrapper with the argument 'Hello':
function functionWrapper(func) {
    return func('Hello');
}
// This will call the sayHello function (defined above) with the argument 'Hello', outputting "Hello":
functionWrapper(sayHello); 

// In many cases, it is not necessary to name the function that is going in as the argument.
// We can use an arrow function (anonymous function, similar to lambda in Python):
functionWrapper(message => console.log(message)); // This will output "Hello".


// A function that returns another function:
function functionCreator() {
    return function() {console.log("Hello again");}
}
const created_function = functionCreator();
created_function(); // Outputs "Hello again".




/* __________Closures__________ 
A closure is a function that accesses a variable defined in the parent scope.
When there is a function that references an identifier in the parent scope,
it creates a closure to save the value in memory so that it can be accessed later.
*/

let b = 3; // This is captured by the closure.
// Value of b is saved in memory so that it can be accessed below:
function closure(a){return a + b;}
console.log(closure(2)); // Outputs 5.


/* __________Array Tricks__________ */
const array = [1, 2, 3, 4, 5, 4, 3, 2, 1]; // Literal syntax

// If we wanted an array with 100 0s, the Array class can be used:
const array2 = new Array(100).fill(0);

/* The map method creates a new array by applying a function to each element of an existing array:
Using map to obtain range functionality similar to Python.
The first parameter is the value, the second is the index (this is called an array entry):
*/
const array3 = Array(100).fill(0).map((_, i) => i + 1); // The value parameter is not used (similar syntax to Python).

/* This can also be done using the spread syntax. The keys method returns the indices of the array,
so we are replacing the array with its indices, resulting in a range of values.
We don't just use Array(100).keys directly because it returns an array iterator, which does not directly provide the values.
*/
const array4 = [...Array(100).keys()];

/* We can also use the spread syntax and set object to get all the unique values from an array.
This uses the fact that sets can only contain unique values.
*/
const set = [...new Set(array)];
console.log(`Original Array: ${array}`);
console.log(`Unique Array: ${set}`);

// Easiest way to loop over an array is the for of loop. The let or const keyword is optional but recommended:
for (let item of array) {console.log(item);}

/* If we also need the index, we can loop over the array entries. Each entry itself is also an array,
and contains the index and the value (this was used for the first 'range' implementation above).
*/
for (const [i, item] of array.entries()) {
    console.log(`Current index: ${i}, Current value: ${item}`);
}




/* __________Module System__________ 
Modules are a way of exporting code (making code available) from one module (file) for use in another module.
*/

/* Example code in module 1:
export const name = 'module';
export function sayHello() {
    console.log(`Hello from ${name}`); // This function happens to be a closure.
}
*/

/* Example code in module 2 (importing from module 1):
import {name, sayHello} from './module1.js';
console.log(name); // 'module'
sayHello(); // 'Hello from module'
*/




/* __________Default Exports__________
A module can choose to export one of its members as a default export. 
This is what will be imported if the module is imported without braces.
*/

/* Example code in module 1:
const name = 'module';
export default name;
*/

/* Example code in module 2 (importing from module 1):
import something from './module.js';
console.log(something); // 'module'
*/