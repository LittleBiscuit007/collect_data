import re
import pprint


def get_data(perform_file_path):
    """

    :param perform_file_path:
    :return:
    spec2006_cint_dict = {'400_perlbench': '83.6',
                         '401_bzip2': '60.8',
                         '403_gcc': '61.4',
                         '429_mcf': '35.0',
                         '445_gobmk': '77.0',
                         '456_hmmer': '59.2',
                         '458_sjeng': '76.4',
                         '462_libquantum': '45.6',
                         '464_h264ref': '112',
                         '471_omnetpp': '30.0',
                         '473_astar': '45.6',
                         '483_xalancbmk': '60.2',
                         'specint_r__base2006': '58.5'}
    spec2006_cfp_dict = {'410_bwaves': '51.8',
                         '416_gamess': '91.9',
                         '433_milc': '29.4',
                         '434_zeusmp': '67.2',
                         '435_gromacs': '55.7',
                         '436_cactusADM': '54.6',
                         '437_leslie3d': '41.3',
                         '444_namd': '73.0',
                         '447_dealII': '97.1',
                         '450_soplex': '41.4',
                         '453_povray': '117',
                         '454_calculix': '66.6',
                         '459_GemsFDTD': '30.1',
                         '465_tonto': '94.7',
                         '470_lbm': '28.1',
                         '481_wrf': '59.9',
                         '482_sphinx3': '64.6',
                         'specfp_r__base2006': '57.6'}
    """
    line_num = 0
    spec2006_dict = {}
    with open(perform_file_path, "r") as f:
        while True:
            con = f.readline()
            if not con:
                break
            if "CFP2006" in perform_file_path:
                line_num = 18
            elif "CINT2006" in perform_file_path:
                line_num = 13
            if "==============================================================================" in con:
                for i in range(line_num):
                    data = f.readline()
                    data_name_list = re.split(r' ', data)
                    data_value_list = data.split()
                    if data_value_list[-1] == "*":
                        spec2006_dict["_".join([i for i in data_name_list[:2] if i != ""]).replace(".", "_")] = \
                        data_value_list[-2]
                    else:
                        if "Est. SPECfp(R)_base2006" in data or "Est. SPECfp(R)_rate_base2006" in data:
                            spec2006_dict["specfp_r__base2006"] = data_value_list[-1].replace("*", "")
                            continue
                        elif "Est. SPECint(R)_base2006" in data or "Est. SPECint(R)_rate_base2006" in data:
                            spec2006_dict["specint_r__base2006"] = data_value_list[-1].replace("*", "")
                            continue
                        spec2006_dict["_".join([i for i in data_name_list[:6] if i != ""]).replace(".", "_")] = \
                        data_value_list[-1].replace("*", "")
                break
    return spec2006_dict


def struct_sql(perform_file_path, spec2006_dict):
    """

    :param perform_file_path:
    :param spec2006_dict:
    :return:
    cint:
    ip | exec_date | thread_status | perlbench_400 | bzip2_401 | gcc_403 | mcf_429 | gobmk_445 | hmmer_456 | sjeng_458
    | libquantum_462 | h264ref_464 | omnetpp_471 | astar_473 | xalancbmk_483 | specint_r__base2006
    cfp:
    ip | exec_date | thread_status | bwaves_410 | gamess_416 | milc_433 | zeusmp_434 | gromacs_435 | cactusadm_436 |
    leslie3d_437 | namd_444 | dealii_447 | soplex_450 | povray_453 | calculix_454 | gemsfdtd_459 | tonto_465 | lbm_470
    | wrf_481 | sphinx3_482 | specfp_r__base2006
    """
    insert_cmd = ""
    select_cmd = ""
    spec2006_type = ""
    data_list = re.split(r'/|-|\.|_', perform_file_path)
    ip = ".".join(data_list[7:11])
    exec_date = "-".join(data_list[11:14]) + " " + ":".join(data_list[14:17])
    # SPEC2006 单核
    # spec2006 多核
    thread_status = "undefined"
    if "spec2006" in perform_file_path:
        thread_status = "omp"
    elif "SPEC2006" in perform_file_path:
        thread_status = "one"
    # print(ip, exec_date, thread_status)
    if "CFP2006" in perform_file_path:
        spec2006_type = "cfp"
        insert_cmd = "insert into spec2006_cfp values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            ip, exec_date, thread_status, spec2006_dict["410_bwaves"], spec2006_dict["416_gamess"],
            spec2006_dict["433_milc"], spec2006_dict["434_zeusmp"], spec2006_dict["435_gromacs"],
            spec2006_dict["436_cactusADM"], spec2006_dict["437_leslie3d"], spec2006_dict["444_namd"],
            spec2006_dict["447_dealII"], spec2006_dict["450_soplex"], spec2006_dict["453_povray"],
            spec2006_dict["454_calculix"], spec2006_dict["459_GemsFDTD"], spec2006_dict["465_tonto"],
            spec2006_dict["470_lbm"], spec2006_dict["481_wrf"], spec2006_dict["482_sphinx3"],
            spec2006_dict["specfp_r__base2006"]
        )
        select_cmd = "select * from spec2006_cfp where ip='{}' and exec_date='{}' and thread_status='{}';".format(
            ip, exec_date, thread_status
        )
    elif "CINT2006" in perform_file_path:
        spec2006_type = "cint"
        insert_cmd = "insert into spec2006_cint values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            ip, exec_date, thread_status, spec2006_dict["400_perlbench"], spec2006_dict["401_bzip2"],
            spec2006_dict["403_gcc"], spec2006_dict["429_mcf"], spec2006_dict["445_gobmk"],
            spec2006_dict["456_hmmer"], spec2006_dict["458_sjeng"], spec2006_dict["462_libquantum"],
            spec2006_dict["464_h264ref"], spec2006_dict["471_omnetpp"], spec2006_dict["473_astar"],
            spec2006_dict["483_xalancbmk"], spec2006_dict["specint_r__base2006"]
        )
        select_cmd = "select * from spec2006_cint where ip='{}' and exec_date='{}' and thread_status='{}';".format(
            ip, exec_date, thread_status
        )
    return insert_cmd, select_cmd, thread_status, spec2006_type


if __name__ == '__main__':
    path_cfp = "/home/loongson/tmp_performance_data/spec2006/192.168.0.104-2022-05-27-11-23-05/spec2006_2022-05-27-11-23-05/CFP2006.020.ref.txt"
    path_cint = "/home/loongson/tmp_performance_data/spec2006/192.168.0.104-2022-05-27-11-23-05/spec2006_2022-05-27-11-23-05/CINT2006.020.ref.txt"
    spec2006_cint_dict = get_data(path_cint)
    pprint.pprint(spec2006_cint_dict)
    spec2006_cfp_dict = get_data(path_cfp)
    pprint.pprint(spec2006_cfp_dict)
    insert_cmd, select_cmd, thread_status, spec2006_type = struct_sql(path_cfp, spec2006_cfp_dict)
    print(insert_cmd)
    print(select_cmd)
    print(thread_status)
    print(spec2006_type)
    insert_cmd, select_cmd, thread_status, spec2006_type = struct_sql(path_cint, spec2006_cint_dict)
    print(insert_cmd)
    print(select_cmd)
    print(thread_status)
    print(spec2006_type)
