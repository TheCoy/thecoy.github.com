---
title: Java装拆箱
date: 2017-05-24 20:47:33
tags: Java
---

## 关于Java装拆箱与包装类型的学习

### Java的包装类
> Java语言是一个面向对象的语言，但是Java中的基本数据类型却是不面向对象的，这在实际使用时存在很多的不便，为了解决这个不足，在设计类时为每个基本数据类型设计了一个对应的类进行代表，这样八个和基本数据类型对应的类统称为包装类(Wrapper Class)，有些地方也翻译为外覆类或数据类型类，如下表所示：


基本数据类型| 对应的包装类
---|---
byte | Byte
short | Short
int | Integer
long | Long
char | Character
float | Float
double | Double
boolean | Boolean
<!-- more -->
#### Java 包装器类的主要目的
- 提供一种机制，将基本值“包装”到对象中，从而使基本值能够包含在为对象而保留的操作中，比如添加到Collections 中，或者从带对象返回值的方法中返回。
- 为基本值提供分类功能。这些功能大多数于各种转换有关：在基本值和String对象间相互转换，在基本值和String对象之间按不同基数转换，如二进制、八进制和十六进制。

---

### 装箱与拆箱
在Java SE5之前，如果要生成一个数值为100的Integer对象，必须这样进行：

```
Integer i = new Integer(100);
```
而从Java SE5开始提供了自动装箱的特性，上述代码可写成如下形式：
```
int i = 100;
```
那么在这个过程中会自动根据数值创建对应的Integer对象，这就是***装箱***，自动调用Integer的valueOf()方法。
```
Integer test = null;
int f = test.initValue();
```
而以上则就是所谓的***拆箱***，自动调用Integer的intValue（）方法。于是，

```
graph LR
装箱-->自动将基本数据类型转换为包装器类型
拆箱-->自动将包装器类型转换为基本数据类型
```

---

### 与之相关的坑与警示
- 由于最近在看《阿里巴巴JAVA开发手册》，在（4）OOP规约的第7条中提到，
> 7. 【强制】所有的相同类型的包装类对象之间值的比较，全部使用 equals 方法比较。 

究竟是什么原因让阿里的程序猿们如此深恶痛觉，其实只需一看源码便知晓答案了，下面这段代码是Integer的valueOf方法的具体实现：
```
public static Integer valueOf(int i){
    if(i >= -128 && i <= IntegerCache.high)
        return IntergerCache.cache[i + 128];
    else
        return new Integer(i);
}
```
- 说明：对于 Integer var=?在-128 至 127 之间的赋值，Integer 对象是在 IntegerCache.cache 产生，会复用已有对象，这个区间内的 Integer 值可以直接使用==进行 判断，但是这个区间之外的所有数据，都会在堆上产生，并不会复用已有对象，这是一个大坑， 推荐使用 equals 方法进行判断

---
### 一些关于装箱与拆箱的面试题
- 这里，先通过下面的表格弄清楚“==”和equals()的区别.

基本数据类型 | == | equals()
--- | --- | ---
字符串变量|对象内存地址|字符串内容
非字符串变量|对象内存地址|对象内存地址
基本类型|值|不可用
包装类|对象内存地址|内容

```
public class Main {
    public static void main(String[] args) {
        Integer i1 = 100;
        Integer i2 = 100;
        Integer i3 = 200;
        Integer i4 = 200;
        
        System.out.println(i1==i2);
        System.out.println(i3==i4);
    }
}
输出结果：
true
false
```
参照以上Integer的valueOf()方法的源码不难理解上述的输出。

```
public class Main {
    public static void main(String[] args) {
        Double i1 = 100.0;
        Double i2 = 100.0;
        Double i3 = 200.0;
        Double i4 = 200.0;
        
        System.out.println(i1==i2);
        System.out.println(i3==i4);
    }
}
输出结果：
false
false
```
在这里只解释一下为什么Double类的valueOf方法会采用与Integer类的valueOf方法不同的实现。很简单：在某个范围内的整型数值的个数是有限的，而浮点数却不是。

```
public class Main {
    public static void main(String[] args) {
        Boolean i1 = false;
        Boolean i2 = false;
        Boolean i3 = true;
        Boolean i4 = true;
         
        System.out.println(i1==i2);
        System.out.println(i3==i4);
    }
}
输出结果：
true
true
```
以上结果参照Boolean类的源码也会一目了然：
```
public static Boolean valueOf(boolean b) {
        return (b ? TRUE : FALSE);
    }
```
> 以及TRUE 和 FALSE的定义
```
/**
 * The {@code Boolean} object corresponding to the primitive
 * value {@code true}.
 */
public static final Boolean TRUE = new Boolean(true);
/**
 * The {@code Boolean} object corresponding to the primitive
 * value {@code false}.
 */
public static final Boolean FALSE = new Boolean(false);
```










