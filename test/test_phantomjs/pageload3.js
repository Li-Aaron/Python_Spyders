/*
* 获取网页并截图
* 保存pdf
*/

// variables
var url = 'http://www.cnblogs.com/ac2sherry/';

// functions
function pageload(status) {
    console.log("Status: " + status);
    if(status === "success") {
        page.render('page.pdf');
    }
    phantom.exit();
}

// main
var page = require('webpage').create();
page.open(url, pageload);