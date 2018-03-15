/*
* 获取网页并截图
* 保存pdf 截取一部分
*/

// variables
var url = 'http://www.cnblogs.com/ac2sherry/';

// functions
function pageload(status) {
    console.log("Status: " + status);
    if(status === "success") {
        page.render('page.jpg');
    }
    phantom.exit();
}

// main
var page = require('webpage').create();

//视窗大小
page.viewportSize = { width: 1024, height: 768 };
//视窗中截取部分
page.clipRect = { top: 0, left: 0, width: 512, height: 256 };

page.open(url, pageload);