/*
* jQuery测试
*/

/* variables */
var url = 'http://www.ucxiaoshuo.com/book/9354/4482326.html';

/* functions */
function pageload(status) {
    console.log("Status: " + status);
    if (status !== 'success') {
        console.log("Unable to access network");
    } else {
        console.log("Accessed network");
        page.includeJs("http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.6.1.js", function () {
            $("#book_text").css("background-color","red");
        });
        // $("#book_text").css("background-color","red");
        page.render('page2.png');
    }
    phantom.exit();
}

/* main */
var page = require('webpage').create();
// console.log("The default user agent is:\n" + page.settings.userAgent);
//Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1
page.settings.userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0";
// console.log("The setting user agent is:\n" + page.settings.userAgent);

page.open(url, pageload);

// 直接在这里退出会导致pageload执行不完
// phantom.exit();