<header><h1 align="center">Free Shadowsocks</h1></header>

A script that automatically crawls free shadowsock accounts from the web. 

一个自动抓取网络上的免费Shadowsocks账号的脚本。

## Requirements (运行环境)

- Windows system
- Python 2.x or 3.x
- Python libraries:
	+ lxml
	+ requests

## Build the environment (搭建环境)

- Windows 8以下的版本可能在运行时会报错如下，需要安装[.NET Framework 4.6.2](https://www.microsoft.com/zh-cn/download/details.aspx?id=17718)
	![.NET Framework 版本过低，无法运行shadowsocks.exe]("trouble_win.png")
- 如果没有安装Python环境，可以去官网[下载](https://www.python.org/downloads/windows/)，优先考虑3.x的版本。具体的安装过程可以参考[百度教程](http://jingyan.baidu.com/article/597a06435f5f02312b5243c6.html)
- 上一步安装成功的情况下，可以通过在cmd中执行如下命令安装lxml、requests的库
	```bash
	pip install lxml
	pip install requests
	```

## Files Introduction (文件说明)

## Questions (问题反馈)

如果在实际运行过程中，有其他类型的错误，可以邮件联系我(yifan.zhang0601@gmail.com)