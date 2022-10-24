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


@echo 爬取结果保存数据库tt_fund下，日志文件保存在log目录下。

pause