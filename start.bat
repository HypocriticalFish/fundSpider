@echo 【第一次运行前必须先双击运行项目目录下的'init.bat'初始化环境，否则无法爬取数据！】


echo.
@echo 【请输入数据库配置信息，默认为ip为localhost(127.0.0.1)，默认端口为3306，默认字符集为'utf8'】
@echo 【输入 # 代表使用Default_DB_Config.ini中的默认配置】


@echo off
@echo off


set /p host=请输入数据库ip:
set /p port=请输入端口号:
set /p user=请输入用户名:
set /p password=请输入密码:


call .\venv\Scripts\activate.bat
@echo 已激活虚拟环境，开始运行爬虫...

python fundSpider.py %host% %port% %user% %password%


@echo 爬取的数据保存在tt_fund数据库中，表结构以及字段含义请查看ReadMe文档，日志请查看log文件夹。

pause