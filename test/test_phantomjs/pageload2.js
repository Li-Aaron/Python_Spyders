/*
* 获取网页并截图 -- 函数拿出来了
*/
function pageload(status) {
    console.log("Status: " + status);
    if(status === "success") {
        page.render('page.png');
    }
    phantom.exit();
}

var page = require('webpage').create();
page.open('http://www.cnblogs.com/ac2sherry/', pageload);