# 用蓝牙共享内容

### 介绍

通过蓝牙而非网络共享文字内容。

逐步搭建原型的同时技术调研，详情见 [悬赏任务](https://gitee.com/zhishi/share-content-using-bluetooth/issues)。

进展：

1. [在两个win 10系统之间通过蓝牙传输文字信息](https://gitee.com/zhishi/share-content-using-bluetooth/issues/IABP3R)

### 参考

- [Briar](https://briarproject.org/)

### 运行期望
行为期望：
先在甲机启动server，然后在乙机启动client，需要确保两台机器的蓝牙都在可用状态

 **甲机server.py详细运行行为：** 
1. 导入必要的模块和库：包括 sys, asyncio, threading 以及 bless 库中的相关类和函数。
2. 定义同步触发器：根据操作系统类型选择使用 threading.Event 或 asyncio.Event 作为触发器。
3. 定义读写请求处理函数：
read_request：返回特征的当前值。
write_request：设置特征的新值，并在接收到特定字符串 "吃了吗" 时触发事件。
4. 定义异步运行函数 run：
 清除触发器。
 实例化 BlessServer 并设置读写请求处理函数。
 添加服务和特征。
 启动服务器并等待触发器事件。
 停止服务器。
5. 运行事件循环：获取事件循环并运行 run 函数直到完成。
 **这些代码的主要目的是创建一个BLE服务器，能够在收到读写请求时运行定义过的处理函数，其中“写”请求被出发时判断写入值是否为“吃了吗”，若判断通过，则控制trigger取消在主线程的阻塞结束程序** 

 **乙机client.py详细运行行为：** 
1. 导入必要的库：导入 asyncio 和 bleak 库中的相关模块。
2. 定义常量：定义了服务 UUID 和特征 UUID。
3. 定义匹配函数：match_service_uuid 函数用于检查扫描到的设备是否包含指定的服务 UUID。
4. 定义主函数 main：
 使用 BleakScanner 扫描蓝牙设备，并通过 match_service_uuid 过滤设备。
 找到匹配设备后，使用 BleakClient 连接设备。
 连接成功后，获取服务和特征，并向特征写入数据（"吃了吗"）。
 **代码的主要目的是通过service的uuid扫描并连接特定的蓝牙设备，然后向甲设备发送数据。** 

 **甲机行为概括：** 
创建并配置server对象（主要为服务uuid、特征uuid和读写权限）
启动server线程并使用trigger阻塞掉主线程防止主线程执行完后自动关闭导致server线程被强制退出
主线程被trigger阻塞，直到server线程收到内容并检查，如果检查为“吃了吗”那么关闭主线程的trigger阻塞
由于主线程不再阻塞，程序立即执行到末尾，程序结束

 **乙机行为概括：** 
创建并配置client对象（这步包含了连接甲机，通过service的uuid搜索并连接）
一旦连上就立即向甲机写入“吃了吗”
程序结束