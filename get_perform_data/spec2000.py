import re
import pprint


def get_data(perform_file_path):
    """

    :param perform_file_path:
    :return:
    spec2000_cfp_dict = {'168_wupwise': '106',
                         '171_swim': '76.3',
                         '172_mgrid': '79.0',
                         '173_applu': '60.7',
                         '177_mesa': '143',
                         '178_galgel': '270',
                         '179_art': '360',
                         '183_equake': '70.1',
                         '187_facerec': '142',
                         '188_ammp': '106',
                         '189_lucas': '76.7',
                         '191_fma3d': '85.6',
                         '200_sixtrack': '56.1',
                         '301_apsi': '140',
                         'Est__SPECfp_rate_base2000': '108'}
    spec2000_cint_dict = {'164_gzip': '56.4',
                         '175_vpr': '88.9',
                         '176_gcc': '126',
                         '181_mcf': '54.7',
                         '186_crafty': '129',
                         '197_parser': '80.5',
                         '252_eon': '186',
                         '253_perlbmk': '121',
                         '254_gap': '96.8',
                         '255_vortex': '138',
                         '256_bzip2': '89.3',
                         '300_twolf': '119',
                         'Est__SPECint_rate_base2000': '101'}
    """
    line_num = 0
    spec2000_dict = {}
    with open(perform_file_path, "r") as f:
        while True:
            con = f.readline()
            if not con:
                break
            if "CFP2000" in perform_file_path:
                line_num = 15
            elif "CINT2000" in perform_file_path:
                line_num = 13
            if "   ========================================================================" in con:
                for i in range(line_num):
                    data = f.readline()
                    data_name_list = re.split(r' ', data)
                    data_value_list = data.split()
                    if data_value_list[-1] == "*":
                        spec2000_dict["_".join([i for i in data_name_list[:6] if i != ""]).replace(".", "_")] = data_value_list[-2]
                    else:
                        if "Est. SPECfp_base2000" in data or "Est. SPECfp_rate_base2000" in data:
                            spec2000_dict["Est__SPECfp_rate_base2000"] = data_value_list[-1].replace("*", "")
                            continue
                        elif "Est. SPECint_rate_base2000" in data or "Est. SPECint_base2000" in data:
                            spec2000_dict["Est__SPECint_rate_base2000"] = data_value_list[-1].replace("*", "")
                            continue
                        spec2000_dict["_".join([i for i in data_name_list[:6] if i != ""]).replace(".", "_")] = data_value_list[-1].replace("*", "")
                break
    return spec2000_dict


def struct_sql(perform_file_path, spec2000_dict):
    """

    :param perform_file_path:
    :param spec2000_dict:
    :return:
    CFP:
    ip | exec_date | thread_status | wupwise_168 | swim_171 | mgrid_172 | applu_173 | mesa_177 | galgel_178 | art_179 |
    equake_183 | facerec_187 | ammp_188 | lucas_189 | fma3d_191 | sixtrack_200 | apsi_301 | specfp_rate_base2000
    CINT:
    ip | exec_date | thread_status | gzip_164 | vpr_175 | gcc_176 | mcf_181 | crafty_186 | parser_197 | eon_252 |
    perlbmk_253 | gap_254 | vortex_255 | bzip2_256 | twolf_300 | specint_rate_base2000
    """
    insert_cmd = ""
    select_cmd = ""
    spec2000_type = ""
    data_list = re.split(r'/|-|\.|_', perform_file_path)
    ip = ".".join(data_list[7:11])
    exec_date = "-".join(data_list[11:14]) + " " + ":".join(data_list[14:17])
    # SPEC2000 单核
    # spec2000 多核
    thread_status = "undefined"
    if "spec2000" in perform_file_path:
        thread_status = "omp"
    elif "SPEC2000" in perform_file_path:
        thread_status = "one"
    # print(ip, exec_date, thread_status)
    if "CFP2000" in perform_file_path:
        spec2000_type = "cfp"
        insert_cmd = "insert into spec2000_cfp values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            ip, exec_date, thread_status, spec2000_dict["168_wupwise"], spec2000_dict["171_swim"],
            spec2000_dict["172_mgrid"], spec2000_dict["173_applu"], spec2000_dict["177_mesa"],
            spec2000_dict["178_galgel"], spec2000_dict["179_art"], spec2000_dict["183_equake"],
            spec2000_dict["187_facerec"], spec2000_dict["188_ammp"], spec2000_dict["189_lucas"],
            spec2000_dict["191_fma3d"], spec2000_dict["200_sixtrack"], spec2000_dict["301_apsi"],
            spec2000_dict["Est__SPECfp_rate_base2000"]
        )
        select_cmd = "select * from spec2000_cfp where ip='{}' and exec_date='{}' and thread_status='{}';".format(
            ip, exec_date, thread_status
        )
    elif "CINT2000" in perform_file_path:
        spec2000_type = "cint"
        insert_cmd = "insert into spec2000_cint values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            ip, exec_date, thread_status, spec2000_dict["164_gzip"], spec2000_dict["175_vpr"],
            spec2000_dict["176_gcc"], spec2000_dict["181_mcf"], spec2000_dict["186_crafty"],
            spec2000_dict["197_parser"], spec2000_dict["252_eon"], spec2000_dict["253_perlbmk"],
            spec2000_dict["254_gap"], spec2000_dict["255_vortex"], spec2000_dict["256_bzip2"],
            spec2000_dict["300_twolf"], spec2000_dict["Est__SPECint_rate_base2000"]
        )
        select_cmd = "select * from spec2000_cint where ip='{}' and exec_date='{}' and thread_status='{}';".format(
            ip, exec_date, thread_status
        )
    return insert_cmd, select_cmd, thread_status, spec2000_type


if __name__ == '__main__':
    path_cfp = "/home/loongson/tmp_performance_data/spec2000/192.168.0.104-2022-05-27-11-20-34/spec2000_2022-05-27-11-20-34/CFP2000.001.asc"
    path_cint = "/home/loongson/tmp_performance_data/spec2000/192.168.0.104-2022-05-27-11-20-34/spec2000_2022-05-27-11-20-34/CINT2000.001.asc"
    spec2000_cfp_dict = get_data(path_cfp)
    # pprint.pprint(spec2000_cfp_dict)
    spec2000_cint_dict = get_data(path_cint)
    # pprint.pprint(spec2000_cint_dict)
    insert_cmd, select_cmd, thread_status, spec2000_type = struct_sql(path_cfp, spec2000_cfp_dict)
    print(insert_cmd)
    print(select_cmd)
    print(thread_status)
    print(spec2000_type)
    insert_cmd, select_cmd, thread_status, spec2000_type = struct_sql(path_cint, spec2000_cint_dict)
    print(insert_cmd)
    print(select_cmd)
    print(thread_status)
    print(spec2000_type)
