/*
* 测试中文输出
*/

/* variables */

/* functions */

/* main */
phantom.outputEncoding="utf-8";
console.log("["+phantom.outputEncoding+"]测试中文输出");


phantom.outputEncoding="gbk";
console.log("["+phantom.outputEncoding+"]测试中文输出");


phantom.exit();