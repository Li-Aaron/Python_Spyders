/*
* jQuery测试
*/

// Read the Phantom webpage '#intro' element text using jQuery and "includeJs"

"use strict";
var page = require('webpage').create();

page.onConsoleMessage = function(msg) {
    console.log(msg);
};

page.open("http://phantomjs.org/", function(status) {
    if (status === "success") {
        page.includeJs("http://code.jquery.com/jquery-1.6.1.min.js", function() {
            page.evaluate(function() {
                console.log("$(\".explanation\").text() -> " + $(".explanation").text());
            });
            phantom.exit(0);
        });
    } else {
      phantom.exit(1);
    }
});
