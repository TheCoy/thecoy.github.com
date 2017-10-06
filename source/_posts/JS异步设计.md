---
title: JS异步设计
date: 2017-08-27 11:55:16
tags: 异步
---

## JavaScript 异步任务设计
```javascript
// asyncFunA()
// asyncFunB()
// asyncFunC()
RunTasks({
    duration:1000,
    tasks:[
        [asyncFunA, 'foo', 'bar'],
        asyncFunB,
        [asyncFunC,'baz']
    ],
    done:function (resultA, resultB, resultC) {
        console.log(resultA, resultB, resultC);
    },
    fail:function (err) {
        console.error(err);
    },
    timeout:function () {
        console.log('timeout');
    }
});
```
<!-- more -->
要求设计一个RunTask函数，使得三个异步任务在给定时间内执行完后输出对应结果，如果超时则打印超时提示，如果失败则提示任务异常信息：
```javascript
var asyncFunA = function (param1, param2, callback) {
    console.info('asyncFunctionA running');
    callback && callback();
    return true;
}
var asyncFunB = function (callback) {
    console.info('asyncFunctionB running');
    callback && callback();
    return true;
}
var asyncFunC = function (param1,callback){
    var otime = new Date();
    console.info('asyncFunctionC running');
    var ntime = new Date();
    while(ntime-otime < 1000){
        ntime = new Date();
        console.log("time:" + Date(ntime-otime));
    }
    callback && callback();
    return true;
}
```

```javascript
function  RunTasks(runTasks) {
    var res = [];
    var length  =runTasks.tasks.length;
    var timeout = false;
    var timer1 = function (callback) {
        timeout = false;
        console.log('-----start-----');
        return setTimeout(function () {
            timeout = true;
            callback && callback();
        },runTasks.durartion);

    };

    var timer = timer1(runTasks.timeout);

    runTasks.tasks.forEach( function (funitem, index ){
        try {
            var fun = funitem;
            if (Array.isArray(funitem)) {
                fun = funitem[0];
                funitem = funitem.slice(1);
                //fun = funitem.splice(0,1);
            }
            else {
                funitem = [];
            }
            funitem.push(function () {
                res[index] = true;
                for (var i =0;i<length;i++ ) {
                    if (!res[i])
                        return;
                }
                clearTimeout(timer);
                timeout || runTasks.done(res);
            });

            setTimeout(function(){
                fun.apply(this, funitem);
            });

        }
        catch (e){
            runTasks.fail(e)
        }
    })
}
```