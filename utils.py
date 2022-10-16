#
#   @Author Hypocritical Fish
#   @Create 2022/10/16 6:27
#   @Description    工具方法


import datetime
import os


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


# 获取格式化后的当前时间戳字符串，例如20221016014826
def get_timestamp():
    timestamp = str(datetime.datetime.now()).replace('-', '').replace(':', '').replace(' ', '')
    index = timestamp.rfind('.')
    timestamp = timestamp[:index]
    return timestamp


# 递归删除指定文件夹下的所有文件
def del_file(path_data):
    for i in os.listdir(path_data):
        file_data = path_data + "\\" + i
        if os.path.isfile(file_data):
            os.remove(file_data)
        else:
            del_file(file_data)
