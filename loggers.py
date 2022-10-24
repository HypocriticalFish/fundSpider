#
#   @Author Hypocritical Fish
#   @Create 2022/10/16 2:37
#   @Description 通用日志模块

import logging
import os
import time
import colorlog


# 这里是为了永远将日志文件夹放在当前工程目录下，而不至于当项目下有多个子目录时
def project_path():
    pwd = os.getcwd()
    while len(pwd.split('\\')) > 6:
        pwd = os.path.dirname(pwd)  # 向上退一级目录
    # print(pwd)
    return pwd


def get_logger(isfile=False):
    # black, red, green, yellow, blue, purple, cyan(青) and white, bold(亮白色)
    log_colors_config = {
        'DEBUG': 'bold_white',
        'INFO': 'bold',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',  # 加bold后色彩变亮
    }
    logger = logging.getLogger()
    # 输出到console
    # logger.setLevel(level=logging.DEBUG)
    logger.setLevel(level=logging.INFO)  # 某些python库文件中有一些DEBUG级的输出信息，如果这里设置为DEBUG，会导致console和log文件中写入海量信息
    console_formatter = colorlog.ColoredFormatter(
        # fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        fmt='%(log_color)s %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        # datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors=log_colors_config
    )
    console = logging.StreamHandler()  # 输出到console的handler
    # console.setLevel(logging.DEBUG)
    console.setFormatter(console_formatter)
    logger.addHandler(console)
    # 输出到文件
    if isfile:
        # 设置文件名
        time_line = 'log_' + time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        log_path = os.path.join(project_path(), 'log')
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        logfile = log_path + '/' + time_line + '.txt'
        # 设置文件日志格式
        # logger.info(logfile)
        filer = logging.FileHandler(logfile, mode='w')  # 输出到log文件的handler
        # filer.setLevel(level=logging.DEBUG)
        file_formatter = logging.Formatter(
            fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'
        )
        # formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        filer.setFormatter(file_formatter)
        logger.addHandler(filer)

    return logger

