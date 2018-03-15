/*
* 网络监控
*/

// variables
var url = 'http://www.cnblogs.com/ac2sherry/';

// functions


// main
var page = require('webpage').create();
//Request嗅探
page.onResourceRequested = function (request) {
    console.log("Request " + JSON.stringify(request, undefined, 4));
};
//Response嗅探
page.onResourceRecieved = function (response) {
    console.log("Request " + JSON.stringify(response, undefined, 4));
};

page.open(url);
// phantom.exit();