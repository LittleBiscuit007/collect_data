import re
import pprint


def get_data(perform_file_path):
    """

    :param perform_file_path:
    :return:
    netperf_dict = {'TCP_Connect_Request_Response': ['8597.88'],
                     'TCP_REQUEST_RESPONSE': ['24423.41'],
                     'TCP_STREAM': ['941.49'],
                     'UDP_REQUEST_RESPONSE': ['27617.19'],
                     'udp_stream': ['960.62', '960.62']}
    """
    netperf_dict = {}
    with open(perform_file_path, "r") as f:
        while True:
            con = f.readline()
            if not con:
                break
            if "UDP UNIDIRECTIONAL" in con:
                for i in range(4):
                    f.readline()
                udp_1 = f.readline()
                udp_2 = f.readline()
                netperf_dict["udp_stream"] = [udp_1.split()[-1], udp_2.split()[-1]]
                continue
            if "TCP STREAM" in con or "TCP REQUEST/RESPONSE" in con or "UDP REQUEST/RESPONSE" in con or \
                    "TCP Connect/Request/Response" in con:
                for i in range(5):
                    f.readline()
                data_con = f.readline()
                netperf_dict["_".join(con.split()[:2]).replace("/", "_")] = [data_con.split()[-1]]
    # pprint.pprint(netperf_dict)
    return netperf_dict


def struct_sql(perform_file_path, netperf_dict):
    """

    :param perform_file_path:
    :param netperf_dict:
    :return:
    ip | exec_date | test_way | tcp_stream | udp_stream | tcp_rr | udp_rr | tcp_crr
    """
    data_list = re.split(r'/|-|\.|_', perform_file_path)
    ip = ".".join(data_list[8:12])
    exec_date = "-".join(data_list[12:15]) + " " + ":".join(data_list[15:18])
    test_way = data_list[7]
    udp_data = " ".join(netperf_dict["udp_stream"])
    # print(ip, exec_date, test_way)
    insert_cmd = "insert into netperf values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(ip, exec_date,
                                                                                                     test_way,
                                                                                                     netperf_dict["TCP_STREAM"][0],
                                                                                                     udp_data,
                                                                                                     netperf_dict["TCP_REQUEST_RESPONSE"][0],
                                                                                                     netperf_dict["UDP_REQUEST_RESPONSE"][0],
                                                                                                     netperf_dict["TCP_Connect_Request_Response"][0])
    select_cmd = "select * from netperf where ip='{}' and exec_date='{}' and test_way='{}';".format(ip, exec_date,
                                                                                                    test_way)
    return insert_cmd, select_cmd, test_way


if __name__ == '__main__':
    path = "/home/loongson/tmp_performance_data/netperf_direct/192.168.0.104-2022-05-27-11-16-26/netperf_direct_2022-05-27-11-16-26/netperf_direct.log"
    netperf_dict = get_data(path)
    insert_cmd, select_cmd, test_way = struct_sql(path, netperf_dict)
    print(insert_cmd)
    print(select_cmd)
