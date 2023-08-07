/* __________Testing (using Vitest)__________ 
Install vitest from the terminal using the command: npm install vitest
Test files should end with ".test.js".
All the functions that need to be tested need be exported from the relevant file,
using the 'export' keyword before the function declaration.
Then, they would be imported in the test file using the 'import' keyword.
*/


// Importing Vitest:
import {expect, test} from "vitest";
import {add} from "syntax.js";


/* Using the 'test' function to define a test:
The first argument is the name of the test.
The second argument is a callback function that contains the test cases.
*/
test("Addition", () => {
    // The 'expect(valueFromFunction).toBe(correctValue)' syntax is used:
    expect(add(1, 2)).toBe(3);
    expect(add(-1, 7)).toBe(6);
    expect(add(-4.3, 5.3)).toBe(1);
});


/* To run the tests, first add the following test script to the 'scripts' section of the package.json file:
"scripts": {
    "test": "vitest"
}

If this file isn't present, run the following command in the terminal within the project directory:
    npm init -y

Then, run the following command in the terminal within the project directory: 
    npm test


While the terminal session is open, every time the code is saved, the tests will be run again.
*/