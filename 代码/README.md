## 测试

### 前提

- 确保两台机器的蓝牙都在可用状态
- 蓝牙设备属性中‘外设’角色为是（Peripheral Role 为 true，下简称‘外设属性真’），参考： [Windows 系统报错: 设备不支持命令功能 / The device does not support the command feature](https://learn.microsoft.com/en-us/answers/questions/1504974/cause-of-system-exception-the-device-does-not-supp)
- 服务端 BLE 广播名固定为 `PathIO`。该名称较短，可给 128 位服务 UUID 留出广播空间；若某系统的广播包仍未携带服务 UUID，客户端也会用此名称兜底匹配。

### 步骤

1、2两步可互换顺序。

1. 甲机server启动
2. 乙机client启动
3. 乙机client连接成功后打印connected
4. 甲机server和乙机client都会提示输入要让对端检查的路径
5. 在任一端输入一个路径，如 `c:\git\share-content-using-bluetooth\代码` 或 `/Users/xx/工具/share-content-using-bluetooth`
6. 对端收到路径后检查该路径在本机是否存在，并返回“存在”或“不存在”
7. 输入端显示对端返回的结果
8. 甲机或乙机都可以继续输入其他路径，可重复完成多次应答
9. 任一端直接回车退出本端程序

### 测试结果

| 服务端运行系统 | 客户端运行系统 | 测试结果 |
|-------------------|----------|-------|
| Win11 | Win10 | 【待测】 |
| Win10 | Win11 | 【待测】 |
| Win11 | Mac 14.5 | 【待测】 |
| Win11 | Win11 外设属性否 | 【待测】成功发送一次，之后客户端启动发送失败 |
| Win11 外设属性否 | | 【待测】服务端启动失败，报错“设备不支持命令功能” |
| Mac | Win11 | 成功！ |
| Win11 （py3.12） | Mac | 服务启动失败：TypeError: tp_basicsize for type '_bleak_winrt_Windows_Foundation.EventRegistrationToken' (24) is too small for base '_winrt.Object' (32) |

## 运行机制

见 [此文档](运行机制/README.md)。
