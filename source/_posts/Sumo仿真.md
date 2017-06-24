---
title: Sumo仿真
date: 2017-06-24 23:25:45
tags: SUMO
---

# SUMO 仿真学习笔记
## 仿真方案的一般步骤
1.创建网络 
    - 使用Netgen生成抽象网络
    - 通过xml文件自定义配置网络，然后用Netconvert 导入
    - 使用Netconvert导入已存在的网络（OSM地图）
2.需求建模
    - 描述明确的车辆路径
    - 仅使用车流和转弯概率
    - 生成随机路径
    - 导入OD矩阵格式
    - 导入已存在路径
3.计算动态用户分配
4.校正仿真
5.执行仿真


<!-- more -->


### 1. SUMO道路网络的构建
**网络格式**
- Sumo 道路网络是个有向图
- 节点代表道路交叉口
- 边代表道路或街道

**边和车道**
- ID：边的标识
- From：起始节点的ID
- To：终止节点的ID
- Priority：道路的优先级
- Function:抽象边的用途（目的）
    - normal:普通边，如高速公路或链接两条道路的街道
    - connector:微观连接器，并不是真实世界道路网络的一部分
    - internal:这类“边”是交叉口的一部分（在交叉口内部）

**1.1 使用XML文件构建自定义道路网络**
* 节点的描述
节点文件一般以".nod.xml"作为扩展名，每行描述一个节点，如下所示：

```
<node id="<STRING>" x="<FLOAT>" y="<FLOAT>" [type="<TYPE>"]/> 
```

type为可选字段，代表节点的类型，其取值及含义如下所示：

Type| 对应含义
---|---
priority | 车辆必须等待，直到它们右侧车辆完全通过路口
traffic_light | 交叉口被交通灯控制
right_before_left | 来自右边的车辆优先通过

一个节点描述示例：
```
<node id="1" x="-500.0" y="0.0" type="priority"/>
```

* 边的描述
边和节点的描述差不多，但还有其他参数。边的描述格式如下所示：
```
<edge id="<STRING>" (fromnode="<NODE_ID>" tonode="<NODE_ID>" | xfrom="<FLOAT>" yfrom="<FLOAT>" xto="<FLOAT>" yto="<FLOAT>")  [type="<STRING>" | nolanes="<INT>" speed="<FLOAT>" priority="<UINT>" length="<FLOAT>")][shape="<2D_POINT> [ <2D_POINT>]*"] [spread_type="center"]/> 
```
每个边都是单向的：从起始节点开始，在终 止节点结束。如果所给出的节点名字不能提取(因为在节点文件中没有定义)，将会产生错误。
 
对每条边，应提供更多的属性，如拥有的车道数，允许的最大车速，边的长度(米)。而 且，还可以定义优先级(可选)。所有这些值（除了长度），可以使用相关的属性值给出，或 者给边一个类型以省略它们。

边的属性如下：

属性名 | 值类型 | 描述
--- | --- | ---
ID | string | 边的名字
fromnode | 参考node_id | 边的起始节点，需在节点文件中存在
tonode | 参考node_id | 边的终止节点，需在节点文件中存在
type | 参考type_id | 类型名
nolanes | int | 边的车道数，必须是整数
speed | float |边允许的最大车速(m/s)，必须是浮点数
priority | int | 边的优先权
length | float | 边长(m)
shape | 位置列表，用(x1,y1,x2,y2)表示，单位m | 例如：<edge id="e1" fromnode="0" tonode="1" shape="0,0 0,100"/> 描述一个边， 从节点0开始，首先经过点(0,0)，然后向右行 100米，最后到达节点1
spread_type | 枚举类型（right,center）| 描述怎样延展车道，center表示双向延展车道， 其他值为右向延展 

一条边的描述示例：
```
<edge id="2o" fromnode="0" tonode="2" priority="1" nolanes="1" speed="11.11"/> 
```
* 使用Netconvert构建网络调用格式如下：
```
netconvert --xml-node-files=MyNodes.nod.xml --xml-edge-files=MyEdges.edg.xml --output-file=MySUMONet.net.xm
```
如果还使用了类型和连接文件，则调用格式如下：
```
netconvert --xml-node-files=MyNodes.nod.xml --xml-edge-files=MyEdges.edg.xml --xml-connection-files=MyConnections.con.xml --xml-type-files=MyTypes.typ.xml --output-file=MySUMONet.net.xml 
```
可能你的边的定义不完整或有错，如果你仍希望导入这个网络，可以试着使用 NETCONVERT的--dismiss-loading-errors参数忽略这些。这样，定义不正确的边将被省略， 但是NETCONVERT仍试图构建网络。

**1.2 OpenStreetMap格式的路网导入**

从OpenStreetMap的[官方网站](http://www.openstreetmap.org/)可以知道， OpenStreetMap是一个可自由编辑的世界地图，它由来自全世界的人士共同编辑维护。 OpenStreetMap工程的地图数据文件是一个或多个XML文件。 注意：OSM数据可以有多种不同的方式下载获得。

NETCONVERT可以导入本地的OSM数据文件，这需要使用选项—osm-files \<file> 下面的命令导入OSM格式路网文件berlin.osm.xml，并把产生的SUMO路网文件保存为 berlin.net.xml：
```
netconvert --osm-files berlin.osm.xml -o berlin.net.xml 
```
注意：导入OSM路网后，一个路口节点可能被分为很多歌节点，这样既不美观，也影响 仿真效果，我们可以合并距离较近的节点，或者指定合并哪些节点，具体如下： 
 ```
netconvert --osm-files map.osm --junctions.join-dist 50 -o guiyang.net.xml 
 ```
 ---

### 2. 需求建模
 在产生路网之后，我们通过GUISIM可以发现，并没有车辆运行。我们还需要对车辆进行一些描述，于是有了如下关于旅程和路径的定义：
 - 旅程(trip) —— 旅程是车辆从一地到另一地的移动，由起始边，目的边和所用时间的定义 
 - 路径(route) —— 路径是扩展的旅程，这就是说路径的定义不仅包含起止边，还包括车俩将 通过的所有的边。SUMO和GUISIM需要路径作为车辆移动的输入数据。有多种方法可以为 SUMO生产路径信息

Sumo中用于处理路径信息的工具：
1. Duarouter —— 负责从其他仿真软件包导入路径或定义，并使用Dijkstra的最短路径算 法计算路径。另外与仿真相结合，DUAROUTER程序可以计算动态用户分配(C. Gawron的模 型)
2. Jtrrouter —— 使用交叉口的转弯率来静态的建模交通
3. Od2trips —— 用于转换OD矩阵到旅程信息
4. Dfrouter —— 从所给的观察点的度量计算路径

**可行的生成随机路径的方法**
1.使用sumo\tools\trip目录下的randomTrips.py脚本生成*.trip.xml随机旅程文件(net 文件作为输入)
```
randomTrips.py  –n  beijing.net.xml 
```
2.使用Duarouter工具(使用net文件和trip文件作为输入)生成路径文件 
```
Duarouter  –n test.net.xml  –t test.trip.xml  –o test.rou.xml --continue-on-unbuild(忽略错误继续) –w(不显示警告信息) 
```
---
### 3. 可行的仿真方案
**3.1  使用随机路径仿真**
1.在OpenStreetMap网站下载osm格式的城市地图
2.使用netconvert把osm格式地图转换为SUMO格式的路网:
```
netconvert --osm-files berlin.osm.xml -o berlin.net.xml
```
3.使用sumo\tools\trip目录下的randomTrips.py脚本生成*.trip.xml随机旅程文件(net 文件作为输入)，以下命令生成berlin.trip.xml随机旅程文件:
```
randomTrips.py  –n  berlin.net.xml 
```
4.使用Duarouter工具(使用net文件和trip文件作为输入)生成路径文件(也可使用车 辆定义文件) 
```
Duarouter  –n berlin.net.xml  –t berlin.trip.xml  –o berlin.rou.xml --continue-on-unbuild(忽略错误继续) –w(不显示警告信息) 
```
5.手工编辑berlin.sumo.cfg配置文件 
```
<?xml version="1.0" encoding="iso-8859-1"?>
    <configuration>
        <input>
            <net-file value="berlin.net.xml"/>
            <route-files value="berlin.rou.xml"/>
            <!--产生的polygon文件berlin.poly.xml需要添加进sumo-gui配置里面： -->
            <additional-files value="berlin.poly.xml"/>
        </input>
        <output>
            <vehroute-output value="vehroutes.xml"/>
        </output> 
        <report>
            <no-duration-log value="true"/> <no-step-log value="true"/>
        </report>
    </configuration>
```
6.在可视化仿真工具sumo-gui中打开berlin.sumo.cfg配置文件，点击运行仿真按钮即可开始仿真
