@echo 【Windos下第一次运行前必须先双击运行项目目录下的'init.bat'初始化环境，否则无法爬取数据！】


@echo off
@echo off



call .\venv\Scripts\activate.bat
@echo 已激活虚拟环境，开始运行爬虫...

python fundSpider.py


@echo 爬取的数据保存在tt_fund数据库中，表结构以及字段含义请查看ReadMe文档，日志请查看log文件夹。

pause