#
#   @Author Hypocritical Fish
#   @Create 2022/10/16 6:27
#   @Description    工具方法


import configparser
import pymysql


# 读取配置文件获取数据库连接
def get_db_connection(host, port, user, password):
    config = configparser.ConfigParser()
    config.read('Default_DB_Config.ini')
    if host == '#':
        host = config.get('mysql-database', 'HOST')
    if port == '#':
        port = int(config.get('mysql-database', 'PORT'))
    if user == '#':
        user = config.get('mysql-database', 'USER')
    if password == '#':
        password = config.get('mysql-database', 'PASSWORD')
    charset = config.get('mysql-database', 'CHARSET')

    conn = pymysql.connect(host=host, user=user, password=password, port=port, charset=charset, database='mysql')

    return conn


# 根据指定Host和Referer构造请求头
def get_headers(host, referer, content_type):
    headers = {
        'igggggnoreburst': 'true',
        'MP-VERSION': '2.2.12',
        'Referer': referer,
        'gtoken': 'ceaf-7e460e8dd19b90228edca6a3e1a06623',
        'clientInfo': 'ttjj-RMX3366-Android-12',
        'Host': host,
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.13',
    }
    if content_type != "":
        headers['content-type'] = content_type
    else:
        headers['content-type'] = 'application/json'
    return headers
