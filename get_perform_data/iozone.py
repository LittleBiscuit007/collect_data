import re


def get_data(perform_file_path):
    """

    :param perform_file_path:
    :return:
    iozone_list = [read, ran_read, write, ran_write]
    """
    flag = 0
    iozone_list = []
    with open(perform_file_path, "r") as f:
        while True:
            con = f.readline()
            if not con:
                break
            if flag == 1:
                if "\n" == con:
                    break
                data_list = con.split()
                iozone_list = [data_list[4], data_list[6], data_list[2], data_list[7]]
            if "KB  reclen   write rewrite" in con:
                flag = 1
                continue
    return iozone_list


def struct_sql(perform_file_path, iozone_list):
    """

    :param perform_file_path:
    :param iozone_list:
    :return:
    ip | exec_date | read | ran_read | write | ran_write
    """
    data_list = re.split(r'/|-|\.|_', perform_file_path)
    ip = ".".join(data_list[7:11])
    exec_date = "-".join(data_list[11:14]) + " " + ":".join(data_list[14:17])
    insert_cmd = "insert into iozone values('{}', '{}', '{}', '{}', '{}', '{}');".format(ip, exec_date, iozone_list[0],
                                                                                         iozone_list[1],
                                                                                         iozone_list[2],
                                                                                         iozone_list[3])
    select_cmd = "select * from iozone where ip='{}' and exec_date='{}';".format(ip, exec_date)
    return insert_cmd, select_cmd


if __name__ == '__main__':
    path = "/home/loongson/tmp_performance_data/iozone/192.168.0.104-2022-05-27-11-14-39/iozone_2022-05-27-11-14-39/iozone_2022-05-27-11-14.txt"
    iozone_list = get_data(path)
    struct_sql(path, iozone_list)

