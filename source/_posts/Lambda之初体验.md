---
title: Lambda之初体验
date: 2017-06-25 17:26:19
tags: ["Java","Python"]
---

## Lambda表达式之初体验
最近在重新系统地学习Python这门语言，在学习关于数据结构中的列表构造部分时，里面也有提到Lambda表达式，不过只是浅尝辄止罢了，加上之前Java（8以上的版本才支持）里面也有用到过Lambda这个东西，索性单独学习并记录之。

### Lambda表达式的定义
Lambda 表达式是一个匿名函数，Lambda表达式基于数学中的λ演算得名，直接对应于其中的lambda抽象(lambda abstraction)，是一个匿名函数，即没有函数名的函数。

### Lambda表达的不完全列举用法
1.使用Lambda表达式作为函数：
```
f = lambda x:x**2
x = f(2)
```
- 一个返回某个集合的所有子集的 lambda 函数
```
f = lambda x:[[y for j, y in enumerate(set(x)) if(i >> j) & 1] for i in range(2**len(set(x)))]
```

2.使用Lambda表达式作为参数传递：
```
pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
pairs.sort(key=lambda pair: pair[1])
```

3.使用Lambda表达式构造列表：
```
res = list(map(lambda x:x**2,range(10)))
```
- map() 函数，它可以将一个函数映射到一个可枚举类型上面。于是map(f,a)就意味着将函数f依次作用在a的每一个元素上。

4.使用Lambda函数作为闭包：
> 闭包就是一个定义在函数内部的函数，闭包使得变量即使脱离了该函数的作用域范围也依然能被访问到。
```
def foo(n):
    return lambda x: x+n
f = foo(0)
print(f(1))
```


### 下面是对比在Python中使用嵌套结构和Lambda两种方式构造列表的比较：
```
#!/usr/bin/env python

matrix = [[1,2,3,4],
            [5,6,7,8],
                [9,10,11,12]]

#嵌套结构的列表推导式
res = [[row[i] for row in matrix] for i in range(len(matrix[0]))]

#Lambda表达式构造外层列表，列表推导式构造里层列表
res = list(map(lambda x:[row[x] for row in matrix],range(len(matrix[0]))))

#Lambda表达式构造里层列表，列表推导式构造外层列表-1
res = [list(map(lambda row:row[x],matrix)) for x in range(len(matrix[0]))]

#Lambda表达式构造里层列表，列表推导式构造外层列表-2
res = [list(map(lambda row:row[x],[row for row in matrix])) for x in range(len(matrix[0]))]


#双Lambda方式构造列表-1
res = list(map(lambda x:list(map(lambda row:row[x],matrix)),range(len(matrix[0]))))

#双Lambda方式构造列表-2
res = list(map(lambda x:list(map(lambda row:row[x],[row for row in matrix])),range(len(matrix[0]))))
```

**未完待续ing....**