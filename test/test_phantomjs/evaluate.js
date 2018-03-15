/*
* 评估脚本
*/

// variables
var url = 'http://www.cnblogs.com/ac2sherry/';


// functions
function pageload(status) {
    console.log("Status: " + status);
    var title = page.evaluate(function () {
        return document.title;
    });
    console.log("Page Title is " + title);
    phantom.exit();
}

// main
var page = require('webpage').create();
page.open(url, pageload);