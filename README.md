# Proxy_Pool 代理池
***
+ 分为4个模块：获取、存储、检验、调度模块；
+ Python版本要求：Python 3.5+
***
## 依赖
+ aiohttp>=1.3.3
+ Flask>=0.11.1
+ redis>=2.10.6
+ requests>=2.13.0
+ pyquery>=1.2.17
***
## 1.运行
#### (1).命令行
```
python run.py
```
#### (2).Pycharm IDE 运行
***

## 2.获取代理IP API
运行run.py之后，程序会在本地开一个服务器，根据自己的设置输入IP和端口号，访问API
例如:

    API: http://localhost:5555/random



> 项目引自： https://github.com/Python3WebSpider/ProxyPool 

> 略修正 redis版本由2.10.5改为2.10.6 否则项目运行会报错
