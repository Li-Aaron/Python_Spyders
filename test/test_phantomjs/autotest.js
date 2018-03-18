/*
* 测试自动处理
*/

/* variables */
var url = 'http://movie.mtime.com/108737/';
phantom.outputEncoding="gbk";
console.log("["+phantom.outputEncoding+"]测试中文输出");
/* functions */
function pageload(status) {
    console.log("Status: " + status);
    if (status !== 'success') {
        console.log("Unable to access network");
    } else {
        console.log("Accessed network");
        var ua = page.evaluate(function () {
            return document.getElementById('ratingRegion').textContent;
            // return document.getElementById('ratingRegion').innerHTML;
        });
        console.log(ua);
    }
    phantom.exit();
}

/* main */
var page = require('webpage').create();

console.log("The default user agent is:\n" + page.settings.userAgent);
//Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1
page.settings.userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0";
console.log("The setting user agent is:\n" + page.settings.userAgent);

page.open(url, pageload);

// 直接在这里退出会导致pageload执行不完
// phantom.exit();