import re


def get_data(perform_file_path):
    """

    :param perform_file_path:
    :return:
    stream_list = [Copy, Scale, Add, Triad]
    """
    flag = 0
    stream_list = []
    with open(perform_file_path, "r") as f:
        while True:
            con = f.readline()
            if not con:
                break
            if "Function    Best Rate MB/s" in con:
                flag = 1
                continue
            if flag != 0:
                flag += 1
            if 1 < flag < 6:
                stream_list.append(con.split()[1])
    return stream_list


def struct_sql(perform_file_path, stream_list):
    """

    :param perform_file_path:
    :param data:
    :return:
     ip | exec_date | thread_num | copy | scale | add | triad
    """
    data_list = re.split(r'/|-|\.|_', perform_file_path)
    ip = ".".join(data_list[7:11])
    exec_date = "-".join(data_list[11:14]) + " " + ":".join(data_list[14:17])
    thread_num = data_list[25]
    insert_cmd = "insert into stream values('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(ip, exec_date,
                                                                                               thread_num,
                                                                                               stream_list[0],
                                                                                               stream_list[1],
                                                                                               stream_list[2],
                                                                                               stream_list[3])
    select_cmd = "select * from stream where ip='{}' and exec_date='{}' and thread_num='{}';".format(ip,
                                                                                                     exec_date,
                                                                                                     thread_num)
    return insert_cmd, select_cmd, thread_num


if __name__ == '__main__':
    path = "/home/loongson/tmp_performance_data/stream/192.168.0.104-2022-05-27-11-09-26/stream_2022-05-27-11-09-26/stream.1core_2022-05-27-11-09.txt"
    stream_list = get_data(path)
    insert_cmd, select_cmd, thread_num = struct_sql(path, stream_list)
