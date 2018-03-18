/*
* fs test
*/


var fs = require('fs');
var path = 'test.txt';

// touch --> create a new file
fs.touch(path);

// exists
if (fs.exists(path))
    console.log("'"+path+"' exists.");
else
    console.log("'"+path+"' not exists.");

// write
var content = 'Hello World!';
fs.write(path, content, 'w');

// read
content = fs.read(path);
console.log('read data:'+ content);

phantom.exit(0);