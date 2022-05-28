import os
import re
import shutil
import psycopg2
from get_perform_data import common_func
from get_perform_data import stream
from get_perform_data import iozone
from get_perform_data import netperf
from get_perform_data import spec2000
from get_perform_data import specjvm2008
from get_perform_data import unixbench
from get_perform_data import unixbench_2d


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
                # 提取数据
                # stream_list = [Copy, Scale, Add, Triad]
                stream_list = stream.get_data(perform_file_path)

                # 构造pgsql
                insert_cmd, select_cmd, thread_num = stream.struct_sql(perform_file_path, stream_list)
                # 将数据写入pgsql
                write_db("stream_" + thread_num, insert_cmd, select_cmd)
            elif "iozone" in perform_file_path:
                # iozone_list = [read, ran_read, write, ran_write]
                iozone_list = iozone.get_data(perform_file_path)

                insert_cmd, select_cmd = iozone.struct_sql(perform_file_path, iozone_list)
                write_db("iozone", insert_cmd, select_cmd)
            elif "netperf" in perform_file_path and "netcard" not in perform_file_path:
                """
                netperf_dict = {'TCP_Connect_Request_Response': ['8597.88'],
                                 'TCP_REQUEST_RESPONSE': ['24423.41'],
                                 'TCP_STREAM': ['941.49'],
                                 'UDP_REQUEST_RESPONSE': ['27617.19'],
                                 'udp_stream': ['960.62', '960.62']}
                """
                netperf_dict = netperf.get_data(perform_file_path)

                insert_cmd, select_cmd, test_way = netperf.struct_sql(perform_file_path, netperf_dict)
                write_db("netperf_"+test_way, insert_cmd, select_cmd)
            elif "UnixBench" in perform_file_path:
                """
                unixbench_dict = {'Dhrystone_2_using_register_variables': '2316.6',
                                 'Double-Precision_Whetstone': '694.4',
                                 'Execl_Throughput': '1065.0',
                                 'File_Copy_1024_bufsize_2000_maxblocks': '2154.1',
                                 'File_Copy_256_bufsize_500_maxblocks': '1433.6',
                                 'File_Copy_4096_bufsize_8000_maxblocks': '3752.7',
                                 'Pipe-based_Context_Switching': '769.4',
                                 'Pipe_Throughput': '1215.4',
                                 'Process_Creation': '926.4',
                                 'Shell_Scripts_1_concurrent': '2490.6',
                                 'Shell_Scripts_8_concurrent': '5178.5',
                                 'System_Benchmarks_Index_Score': '1605.1',
                                 'System_Call_Overhead': '1318.8'}
                """
                unixbench_dict = unixbench.get_data(perform_file_path)

                insert_cmd, select_cmd, test_way = unixbench.struct_sql(perform_file_path, unixbench_dict)
                write_db("unixbench_"+test_way, insert_cmd, select_cmd)
            elif "Unixbench_2d" in perform_file_path:
                """
                unixbench_2d_dict = {'2D_Graphics_Benchmarks_Index_Score': '7127.1',
                                     '2D_graphics_aa_polygons': '2579.0',
                                     '2D_graphics_ellipses': '1230.6',
                                     '2D_graphics_images_and_blits': '78241.9',
                                     '2D_graphics_rectangles': '10951.3',
                                     '2D_graphics_text': '233889.6',
                                     '2D_graphics_windows': '206.1',
                                     '3D_Graphics_Benchmarks_Index_Score': '18.0',
                                     '3D_graphics_gears': '18.0'}
                """
                unixbench_2d_dict = unixbench_2d.get_data(perform_file_path)

                insert_cmd, select_cmd = unixbench_2d.struct_sql(perform_file_path, unixbench_2d_dict)
                write_db("unixbench_2d", insert_cmd, select_cmd)
            elif "specjvm2008" in perform_file_path:
                pass
            elif "spec2000" in perform_file_path or "SPEC2000" in perform_file_path:
                # SPEC2000 单核
                # spec2000 多核
                pass
            elif "spec2006" in perform_file_path or "SPEC2006" in perform_file_path:
                # SPEC2006 单核
                # spec2006 多核
                pass


def write_db(type, insert_cmd, select_cmd):
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

    logger.debug("{} 测试执行插入pgsql命令，命令为：\n {} ".format(type, insert_cmd))
    try:
        # 执行插入数据
        cur.execute(insert_cmd)
        conn.commit()
    except Exception as e:
        logger.error("{} 测试的数据插入pgsql失败，失败信息如下：\n {}".format(type, e))
        return

    logger.debug("{} 测试执行查询命令，判断数据是否写入成功，命令为：\n {} ".format(type, select_cmd))
    # 查看数据是否写入成功
    cur.execute(select_cmd)
    if cur.fetchone() is None:
        logger.error("查询不到 {} 所插入的数据，请检查 insert 命令是否成功".format(type))
    else:
        logger.info("{} 数据插入成功".format(type))

    cur.close()
    conn.close()


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
    download_specified_data("perform_iozone", "Unixbench_2d")
