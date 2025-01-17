## 测试

### 前提

- 确保两台机器的蓝牙都在可用状态
- 蓝牙设备属性中‘外设’角色为是（Peripheral Role 为 true，下简称‘外设属性真’），参考： [Windows 系统报错: 设备不支持命令功能 / The device does not support the command feature](https://learn.microsoft.com/en-us/answers/questions/1504974/cause-of-system-exception-the-device-does-not-supp)

### 步骤

1、2两步可互换顺序。

1. 甲机server启动
2. 乙机client启动
3. 乙机client连接成功后打印connected
4. 甲机server打印“吃了吗”
5. 乙机client打印“我吃了”
6. 乙机client自动退出
7. 甲机server保持开启，乙机再次启动client
8. 回到第3步

### 测试结果

| 服务端运行系统 | 客户端运行系统 | 测试结果 |
|-------------------|----------|-------|
| Win11 | Win10 | 成功 |
| Win10 | Win11 | 【待测】 |
| Win11 | Mac 14.5 | 成功 |
| Win11 | Win11 外设属性否 | 【待测】成功发送一次，之后客户端启动发送失败 |
| Win11 外设属性否 | | 【待测】服务端启动失败，报错“设备不支持命令功能” |

## 运行机制

见 [此文档](运行机制/README.md)。