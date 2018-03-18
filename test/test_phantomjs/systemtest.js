/*
* system test
*/

var system = require('system');
// args: 命令行输入参数
var args = system.args;
console.log("args.length = " + args.length);
if (args.length > 1){
    //array.forEach(function(currentValue, [index, arr]), [thisValue])
    args.forEach(function (arg, i) {
        console.log(i + ': ' + arg);
    });
    // phantom.exit(0);
}

// env: 系统环境变量
var env = system.env;
Object.keys(env).forEach(function (key) {
    console.log('[key]' + key + '=' + env[key]);
});

// os: 操作系统信息
var os = system.os;
console.log(os.architecture); // 32 bit
console.log(os.name); // windows
console.log(os.version); // 10

// pid for this program
var pid = system.pid;
console.log(pid);

// platform name
var platform = system.platform;
console.log(platform); // phantomjs

phantom.exit(0);