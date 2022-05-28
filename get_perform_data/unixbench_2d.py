import re
import pprint


def get_data(perform_file_path):
    """

    :param perform_file_path:
    :return:
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
    unixbench_2d_dict = {}
    with open(perform_file_path, "r") as f:
        while True:
            con = f.readline()
            if not con:
                break
            if "2D Graphics Benchmarks Index Values" in con:
                for i in range(13):
                    data = f.readline()
                    if "========" in data or "\n" == data or "3D Graphics Benchmarks Index Values" in data:
                        continue
                    unixbench_2d_dict["_".join([i for i in re.split(r' |:', data)[:6] if i != ""])] = data.split()[-1]
    return unixbench_2d_dict


def struct_sql(perform_file_path, unixbench_2d_dict):
    """

    :param perform_file_path:
    :param unixbench_2d_dict:
    :return:
    s >> 2
    t >> 3
    ip | exec_date | sd_graphics__aa_polygons | sd_graphics__ellipses | sd_graphics__images_and_blits |
    sd_graphics__rectangles | sd_graphics__text | sd_graphics__windows | sd_graphics_benchmarks_index_score |
    td_graphics__gears | td_graphics_benchmarks_index_score
    """
    data_list = re.split(r'/|-|\.|_', perform_file_path)
    ip = ".".join(data_list[8:12])
    exec_date = "-".join(data_list[12:15]) + " " + ":".join(data_list[15:18])
    # print(ip, exec_date)
    insert_cmd = "insert into unixbench_2d values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
        ip, exec_date, unixbench_2d_dict["2D_graphics_aa_polygons"], unixbench_2d_dict["2D_graphics_ellipses"],
        unixbench_2d_dict["2D_graphics_images_and_blits"], unixbench_2d_dict["2D_graphics_rectangles"],
        unixbench_2d_dict["2D_graphics_text"], unixbench_2d_dict["2D_graphics_windows"],
        unixbench_2d_dict["2D_Graphics_Benchmarks_Index_Score"], unixbench_2d_dict["3D_graphics_gears"],
        unixbench_2d_dict["3D_Graphics_Benchmarks_Index_Score"]
    )
    select_cmd = "select * from unixbench_2d where ip='{}' and exec_date='{}';".format(ip, exec_date)
    return insert_cmd, select_cmd


if __name__ == '__main__':
    path = "/home/loongson/tmp_performance_data/Unixbench_2d/192.168.0.104-2022-05-27-11-13-34/Unixbench_2d_2022-05-27-11-13-34/Unixbench_2d.log"
    unixbench_2d_dict = get_data(path)
    # pprint.pprint(unixbench_2d_dict)
    insert_cmd, select_cmd = struct_sql(path, unixbench_2d_dict)
    print(insert_cmd)
    print(select_cmd)
