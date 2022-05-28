import re
import pprint


def get_data(perform_file_path):
    """

    :param perform_file_path:
    :return:
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
    unixbench_dict = {}
    with open(perform_file_path, "r") as f:
        while True:
            con = f.readline()
            if not con:
                break
            if "System Benchmarks Index Values " in con:
                for i in range(14):
                    data = f.readline()
                    if "========" in data:
                        continue
                    unixbench_dict["_".join([i for i in re.split(r' |\(|\)', data)[:6] if i != ""])] = data.split()[-1]
    return unixbench_dict


def struct_sql(perform_file_path, unixbench_dict):
    """

    :param perform_file_path:
    :param unixbench_dict:
    :return:
    ip | exec_date | test_way | dhrystone_2_using_register_variables | execl_throughput |
    file_copy_1024_bufsize_2000_maxblocks | file_copy_256_bufsize_500_maxblocks | file_copy_4096_bufsize_8000_maxblocks|
    pipe_based_context_switching | pipe_throughput | process_creation | shell_scripts_1_concurrent |
    shell_scripts_8_concurrent | system_call_overhead | system_benchmarks_index_score
    """
    data_list = re.split(r'/|-|\.|_', perform_file_path)
    ip = ".".join(data_list[7:11])
    exec_date = "-".join(data_list[11:14]) + " " + ":".join(data_list[14:17])
    test_way = data_list[25]
    # print(ip, exec_date, test_way)
    insert_cmd = "insert into unixbench values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
        ip, exec_date, test_way, unixbench_dict["Dhrystone_2_using_register_variables"],
        unixbench_dict["Execl_Throughput"], unixbench_dict["File_Copy_1024_bufsize_2000_maxblocks"],
        unixbench_dict["File_Copy_256_bufsize_500_maxblocks"], unixbench_dict["File_Copy_4096_bufsize_8000_maxblocks"],
        unixbench_dict["Pipe-based_Context_Switching"], unixbench_dict["Pipe_Throughput"],
        unixbench_dict["Process_Creation"], unixbench_dict["Shell_Scripts_1_concurrent"],
        unixbench_dict["Shell_Scripts_8_concurrent"], unixbench_dict["System_Call_Overhead"],
        unixbench_dict["System_Benchmarks_Index_Score"]
    )
    select_cmd = "select * from unixbench where ip='{}' and exec_date='{}' and test_way='{}';".format(ip, exec_date,
                                                                                                      test_way)
    return insert_cmd, select_cmd, test_way


if __name__ == '__main__':
    path = "/home/loongson/tmp_performance_data/UnixBench/192.168.0.104-2022-05-27-11-11-28/UnixBench_2022-05-27-11-11-28/Unixbench_1_2022-05-27-11-11.txt"
    unixbench_dict = get_data(path)
    # pprint.pprint(unixbench_dict)
    insert_cmd, select_cmd, test_way = struct_sql(path, unixbench_dict)
    print(insert_cmd, select_cmd, test_way)
