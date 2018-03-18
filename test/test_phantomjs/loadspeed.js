/*
* 测速脚本
*/

// variables
var page = require('webpage').create(),
    system = require('system'),
    t, address;

// functions
// system.args[] --> 入参
function pageload(status) {
    console.log("Status: " + status);
    if(status !== "success") {
        console.log("FAIL to load the address");
    } else {
        t = Date.now() - t;
        console.log("Loading " + system.args[1]);
        console.log("Loading time " + t + " msec");
    }
    phantom.exit();
}

// main
if (system.args.length === 1) {
    console.log("Usage: loadspeed.js [some URL]");
    phantom.exit();
}
t = Date.now();
address = system.args[1];

page.open(address, pageload);