/*
* 获取网页并截图 -- 用匿名函数
*/
var page = require('webpage').create();
page.open('http://www.cnblogs.com/ac2sherry/', function(status) {
    console.log("Status: " + status);
    if(status === "success") {
        page.render('page.png');
    }
    phantom.exit();
});