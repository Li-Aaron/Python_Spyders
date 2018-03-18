/*
* jQuery测试
*/
"use strict";
/* variables */
var url = 'http://phantomjs.org/';
phantom.outputEncoding="gbk";

/* functions */

/* main */
var page = require('webpage').create();

page.open(url, function(status) {
    if (status === "success") {
        page.render('page1.png');
        console.log("page1.png saved success");
        page.includeJs("http://code.jquery.com/jquery-1.6.1.min.js", function() {
            page.evaluate(function() {
                // jQuery is loaded
                var jqsel = $('.explanation');
                // console.log("$(\".explanation\").text() -> " + jqsel.text());
                jqsel.text('My PhantomJS');
                // console.log("$(\".explanation\").text() -> " + jqsel.text());
            });
            page.render('page2.png');
            console.log("page2dnh.png saved success");
            phantom.exit(0);
        });
    } else {
        phantom.exit(1);
    }
});

// 直接在这里退出会导致pageload执行不完
// phantom.exit();