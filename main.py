import os
import re
import psycopg2
from get_perform_data import common_func


def download_specified_data(test_group_name, test_type):
    """
    从10.2.5.25上获取 test_group_name 下的机器IP的 test_type 的数据，
    并调用 get_specified_data 函数来获取性能数据写入pgsql
    :param test_group_name:
    :param test_type:
    :return:
    """
    pass


def get_test_machine():
    """
    hosts 文件需要与 main.py 文件位于同级目录
    :return:
        测试机器的信息，包含组名及其组下的机器IP
        {'perform_stream': ['192.168.0.103', '192.168.0.101'], 'perform_iozone': ['192.168.0.102']}
    """
    test_machine_dict = {}
    group_name = ""
    with open("hosts", "r") as f:
        while True:
            con = f.readline()
            if not con:
                break
            if "\n" == con:
                continue
            if "[" in con:
                group_name = re.split(r'\[|\]', con)[1]
                test_machine_dict[group_name] = []
                continue
            test_machine_dict[group_name].append(con.strip())
    logger.debug("测试机器信息如下：\n{}".format(test_machine_dict))
    return test_machine_dict


def get_specified_data():
    """
    获取文件的存储路径，调用 get_perform_data 下的脚本，用于获取性能数据
    调用 write_db 函数写入数据库
    :return:
    """
    pass


def write_db():
    """
    链接 pgsql 数据库，将性能数据写入对应的 table ，并检查是否写入成功
    :return:
    """
    pgsql_ip = '127.0.0.1'
    # 检查pgsql服务端是否可以ping通，若无法ping通直接退出程序
    common_func.check_network_con(pgsql_ip)

    PG_CONF = {
        'user': 'loongson',
        'port': 5432,
        'host': pgsql_ip,
        'password': 'loongson',
        'database': 'performance_data'
    }
    try:
        conn = psycopg2.connect(**PG_CONF)
    except Exception as e:
        logger.error(e)
        raise

    # 创建光标用于执行sql语句
    cur = conn.cursor()

    # 执行插入数据
    # cur.execute()

    # 查看数据是否写入成功
    cur.execute("SELECT * FROM iozone;")
    print(cur.fetchone())


# 定义logger，并将info/debug/waring/error/critical日志写入文件，设置的日志级别为 debug
logger = common_func.logger

if __name__ == '__main__':
    """
    1. 从10.2.5.25上获取性能数据
    2. 从文件中提取需要的数据
    3. 写入pgsql数据库（10.40.57.1）
    """
    write_db()
    # test get_specified_data api function
    download_specified_data("perform_stream", "stream")
