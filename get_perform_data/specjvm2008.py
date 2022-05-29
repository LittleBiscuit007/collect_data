import re
import pprint


def get_data(perform_file_path):
    """

    :param perform_file_path:
    :return:
    specjvm_dict = {'composite_result': '104.6',
                     'compress': '149.42',
                     'crypto': '303.04',
                     'derby': '216.48',
                     'mpegaudio': '102.79',
                     'scimark_large': '24.61',
                     'scimark_small': '179.53',
                     'serial': '86.4',
                     'startup': '23.1',
                     'sunflow': '50.93',
                     'xml': '346.32'}
    """
    flag = 0
    specjvm_dict = {}
    with open(perform_file_path, "r") as f:
        while True:
            con = f.readline()
            if not con:
                break
            if "================================" in con:
                flag += 1
            if flag == 3:
                for i in range(10):
                    data = f.readline()
                    data_list = data.split()
                    specjvm_dict[data_list[0].replace(".", "_")] = data_list[-1]
                flag += 1
            if "Noncompliant composite result" in con:
                specjvm_dict["_".join(re.split(r' |:', con)[1:3])] = con.split()[-2]
                break
    return specjvm_dict


def struct_sql(perform_file_path, specjvm_dict):
    """

    :param perform_file_path:
    :param specjvm_dict:
    :return:
    ip | exec_date | compiler | compress | crypto | derby | mpegaudio | scimark_large | scimark_small | serial |
    startup | sunflow | xml | composite_result
    """
    data_list = re.split(r'/|-|\.|_', perform_file_path)
    ip = ".".join(data_list[7:11])
    exec_date = "-".join(data_list[11:14]) + " " + ":".join(data_list[14:17])
    # TODO cartoon java 11 测试结果没有 compiler 字段的值，检查是否与java版本有关系，并对缺失的值以 N/A 补充
    if "compiler" not in specjvm_dict.keys():
        specjvm_dict["compiler"] = "N/A"

    insert_cmd = "insert into specjvm values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
        ip, exec_date, specjvm_dict["compiler"], specjvm_dict["compress"], specjvm_dict["crypto"],
        specjvm_dict["derby"], specjvm_dict["mpegaudio"], specjvm_dict["scimark_large"], specjvm_dict["scimark_small"],
        specjvm_dict["serial"], specjvm_dict["startup"], specjvm_dict["sunflow"], specjvm_dict["xml"],
        specjvm_dict["composite_result"]
    )
    select_cmd = "select * from specjvm where ip='{}' and exec_date='{}';".format(ip, exec_date)
    return insert_cmd, select_cmd


if __name__ == '__main__':
    path = "/home/loongson/tmp_performance_data/SpecJvm2008/192.168.0.104-2022-05-28-20-11-21/SpecJvm2008_2022-05-28-20-11-21/SPECjvm2008.001.txt"
    specjvm_dict = get_data(path)
    # pprint.pprint(specjvm_dict)
    insert_cmd, select_cmd = struct_sql(path, specjvm_dict)
    print(insert_cmd)
    print(select_cmd)
