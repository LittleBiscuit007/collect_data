import os
import re
import shutil
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
    # 共享目录的机器IP
    share_ip = "127.0.0.1"
    common_func.check_network_con(share_ip)
    share_username = "loongson-test"
    share_passwd = "loongson"

    logger.debug("需要下载的文件信息为 {} 组的 {} 性能测试数据".format(test_group_name, test_type))

    perform_data_root_path = "/home/loongson/tmp_performance_data"
    if os.path.exists(perform_data_root_path):
        shutil.rmtree(perform_data_root_path)
    os.mkdir(perform_data_root_path)
    # 获取测试机器信息
    test_machine_dict = get_test_machine()

    # 判断传递的参数 test_group_name 是否在 hosts 文件中
    if test_group_name not in test_machine_dict.keys():
        logger.error("传递的参数 {} 错误，该组名不存在于 hosts 测试机器的列表中".format(test_group_name))
        raise
    # 下载需要提取的性能数据文件
    type_perform_data_root_path = perform_data_root_path + "/" + test_type
    for test_ip in test_machine_dict[test_group_name]:
        # 创建下载数据的父目录名
        if not os.path.exists(type_perform_data_root_path):
            os.mkdir(type_perform_data_root_path)
        down_cmd = "sshpass -p {} scp -o StrictHostKeyChecking=no -r {}@{}:~/autotest_result/{}/{}* {}".format(
            share_passwd, share_username, share_ip, test_type, test_ip, type_perform_data_root_path
        )
        os.system(down_cmd)
        logger.debug("下载性能数据的命令为：\n{}".format(down_cmd))

    # 调用 get_specified_data 函数，提取性能数据
    get_specified_data(type_perform_data_root_path)


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


def traversal_dir(path, perform_file_list):
    """
    遍历 path 下的所有文件以及子目录的文件
    :param path: 被遍历的目录
    :return:
    """
    file_dir_list = os.listdir(path)
    for dir in file_dir_list:
        file_path = os.path.join(path, dir)
        if os.path.isdir(file_path):
            traversal_dir(file_path, perform_file_list)
        else:
            # print(file_path)
            perform_file_list.append(file_path)


def get_specified_data(type_perform_data_root_path):
    """
    获取文件的存储路径，调用 get_perform_data 下的脚本，用于获取性能数据
    调用 write_db 函数写入数据库
    :param type_perform_data_root_path: 存放指定测试类型的数据文件路径
    :return:
    """
    # 获取 type_perform_data_root_path 文件路径下的所有文件及子文件
    perform_file_list = []
    traversal_dir(type_perform_data_root_path, perform_file_list)

    logger.debug("该性能数据的文件路径为：\n{}".format(perform_file_list))

    # 遍历文件路径，提取每个文件的数据
    for perform_file_path in perform_file_list:
        if ".swap" not in perform_file_path:
            if "stream" in perform_file_path:
                pass
            elif "iozone" in perform_file_path:
                pass
            elif "netperf" in perform_file_path:
                pass
            elif "UnixBench" in perform_file_path:
                pass
            elif "Unixbench_2d" in perform_file_path:
                pass
            elif "specjvm2008" in perform_file_path:
                pass
            elif "spec" in perform_file_path or "SPEC" in perform_file_path:
                pass
    # SPEC2000 单核
    # spec2000 多核
    # SPEC2006 单核
    # spec2006 多核


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
    # write_db()
    # test get_specified_data api function
    download_specified_data("perform_iozone", "stream")
