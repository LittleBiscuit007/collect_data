import logging
import os
import colorlog


def check_network_con(ip):
    """
    检查 ip 的网络连接，本机是否可以 ping 通
    :param ip: ping 的目的IP
    :return:
    无法ping通直接抛出异常，退出程序
    """
    status = os.popen("ping -c 3 {} | grep 'packet loss' | awk '{{print $6}}'".format(ip)).read()
    if "0%" in status:
        logger.info("{} 可以 ping 通！".format(ip))
    else:
        logger.error("{} 不能 ping 通！".format(ip))
        raise


def get_logger():
    log_colors_config = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red'
    }

    file_formatter = logging.Formatter(
        fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S'
    )
    console_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors=log_colors_config
    )

    # LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    # # LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s, line:%(lineno)d - %(message)s" 带有文件名、行号
    # DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    logger = logging.getLogger()
    # 设置日志的级别，默认为 WARNING
    logger.setLevel(logging.DEBUG)

    # 输出到文件
    file_handler = logging.FileHandler("log/all.log", mode='a', encoding='utf-8')

    # 输出到控制台
    stream_handler = logging.StreamHandler()

    # 错误日志单独输出到一个文件
    error_handler = logging.FileHandler('log/error.log', mode='a', encoding='utf-8')
    # 错误日志只记录ERROR级别的日志
    error_handler.setLevel(logging.ERROR)

    # 将所有的处理器加入到logger中
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.addHandler(error_handler)

    # formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # 设置格式化
    file_handler.setFormatter(file_formatter)
    stream_handler.setFormatter(console_formatter)
    error_handler.setFormatter(file_formatter)

    return logger


logger = get_logger()

if __name__ == '__main__':
    logger.info('info级别的')
    logger.error('error级别')
    logger.debug('debug级别')
    logger.warning('warning级别')
    logger.critical("critical级别")
