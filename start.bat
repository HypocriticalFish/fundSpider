@echo 【第一次运行前必须先双击运行项目目录下的'init.bat'初始化环境，否则无法爬取数据！】


echo.
@echo 【爬取模式说明：】


@echo off
@echo off
@echo 【basic】：仅爬取投顾产品基本数据，不包含持仓信息、调仓信息以及每日涨幅信息；
@echo 【detial】：仅爬取投顾产品持仓信息、调仓信息以及每日涨幅信息，不包括基本数据；
@echo 【all】：爬取投顾产品全部信息，默认模式


@echo off

@echo off

set /p mode=请输入爬取模式:


call .\venv\Scripts\activate.bat
@echo 已激活虚拟环境，开始运行爬虫...

python fundSpider.py %mode%


@echo 爬取结果保存在项目目录下的fundData文件夹下，日志文件保存在log目录下。

pause