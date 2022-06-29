# Douyin-live-room-data-collection
dy直播间基本数据采集

**本项目仅供学习，严禁用于任何商业、违法行为！**

***

### 1.项目运行所需库
- uvicorn     服务运行基础
- fastapi     web接口服务
- apscheduler 定时任务库
- aiosql      数据库异步读写
- httpx       web异步请求库

### 2.更改配置
转到douyin/config.py文件

其中，room_id填入在网页访问dy直播间的网址id
例： https://live.d**y**.com/**123456789**
**123456789**即需要填入的房间id
其余按注释修改即可。

### 3.运行
进入根目录后
`uvicorn main:app --port 8880`
或
`python3 main.py`

### 4.数据管理
项目并未编写数据管理面板，如有需要请自行解决
但项目提供了一个最简单的状态查看接口，内网环境下访问 http://127.0.0.1:8880, 外网环境可使用ngnix反代后ip加端口即可。

请求后返回：
`在线房间，房间名及房间所属用户，房间在线用户状态`
