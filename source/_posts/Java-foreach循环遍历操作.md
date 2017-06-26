---
title: Java foreach循环遍历操作
date: 2017-05-31 20:22:12
tags: [Java]
---

## 先贴一段会报异常的代码

```java
public static void main(String[] args){
        List<String> list = new ArrayList<>();

        list.add("first");
        list.add("second");
        list.add("third");
        list.add("fourth");

        for(String str:list){
            if("first".equals(str))
                list.remove(str);
        }
        
        System.out.println(list.toString());
    }
```

如上代码会报java.util.ConcurrentModificationException这个异常：
```
Exception in thread "main" java.util.ConcurrentModificationException
```
<!-- more -->
 for(String str:list)　这句话实际上是用到了集合的iterator() 方法,一般我们也会经常用到iterator来遍历集合，但是一旦设计到对元素进行修改（CRUD）的时候就需要格外注意了，具体一看源码便知：
 
 ```java
 <!--java.util. AbstractList的内部类Itr的源码-->
  public void remove() {  
        if (lastRet == -1)  
            throw new IllegalStateException();  
            checkForComodification();  
  
        try {  
            AbstractList.this.remove(lastRet); //执行remove的操作  
            if (lastRet < cursor)  
              cursor--;  
            lastRet = -1;  
            expectedModCount = modCount; //保证了modCount和expectedModCount的值的一致性，避免抛出ConcurrentModificationException异常  
        } catch (IndexOutOfBoundsException e) { 
            throw new ConcurrentModificationException();  
        }  
    }  
  
    final void checkForComodification() {  
        if (modCount != expectedModCount) //当modCount和expectedModCount值不相等时，则抛出ConcurrentModificationException异常  
            throw new ConcurrentModificationException();  
    }  
    
 ```
 然而，ArrayList的remove方法是这样的：
 ```java
 public boolean remove(Object o) {  
    if (o == null) {  
            for (int index = 0; index < size; index++)  
        if (elementData[index] == null) {  
            fastRemove(index);  
            return true;  
        }  
    } else {  
        for (int index = 0; index < size; index++)  
        if (o.equals(elementData[index])) {  
            fastRemove(index);  
            return true;  
        }  
    }  
    return false;  
}  
  
    /* 
     * Private remove method that skips bounds checking and does not 
     * return the value removed. 
     */  
    private void fastRemove(int index) {  
        modCount++; //只是修改了modCount，因此modCount将与expectedModCount的值不一致  
        int numMoved = size - index - 1;  
        if (numMoved > 0)  
            System.arraycopy(elementData,index+1,elementData,index,numMoved);  
        elementData[--size] = null; // Let gc do its work  
    } 
 ```
 
 * 通过阅读源码即可知道，ArrayList的remove方法只是修改了modCount的值，并没有修改expectedModCount，导致modCount和expectedModCount的值的不一致性，当next()时则抛出ConcurrentModificationException异常。因此使用Iterator遍历集合时，不要改动被迭代的对象，可以使用 Iterator 本身的方法 remove() 来删除对象，Iterator.remove()方法会在删除当前迭代对象的同时维护modCount和expectedModCount值的一致性。
 
* 另外注意如果是如下的情况又不会报异常：
```java
public static void main(String[] args){
        List<String> list = new ArrayList<>();

        list.add("first");
        list.add("second");
        list.add("third");
        list.add("fourth");

        for(String str: list){
            if("third".equals(str))
                list.remove(str);
        }

        System.out.println(list.toString());
    }
```
- 这是因为在删除倒数第二个元素的时候，cursor指向最后一个元素的，而此时删掉了倒数第二个元素后，cursor和size()正好相等了，所以hasNext()返回false，遍历结束，于是也就不会进入到next（）执行checkForComodification检查了，所以也就不会报异常。
- 最后，回到本文的主题，foreach（）循环遍历的正确打开方式如下：
```java
public static void main(String[] args){
        List<String> list = new ArrayList<>();

        list.add("first");
        list.add("second");
        list.add("third");
        list.add("fourth");
        list.add("five");

        Iterator<String> it = list.iterator();
        while(it.hasNext()){
            String temp = it.next();
            if("five".equals(temp))
                it.remove();
        }

        System.out.println(list.toString());
    }
```
- 不过对于在多线程环境下对集合类元素进行迭代修改操作，最好把代码放在一个同步代码块内，这样才能保证modCount和expectedModCount的值的一致性，类似如下：
```java
Iterator<String> iterator = list.iterator();    
synchronized(synObject) {  
    while(iterator.hasNext()) {    
        String str = iterator.next();    
        if(del.contains(str)) {    
            iterator.remove();    
        }    
    }    
} 
```
