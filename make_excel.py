"""
本代码的工作是根据data_for_check当中保存的轨迹生成一个与之对应的excel文件
"""
import os
from process_data_util import *
parent_folder_path = "data_for_check_25_3_27/2_data_for_check"
folder_paths = get_sorted_subfolder_paths(parent_folder_path)
total_lenth = 0
for folder_path in folder_paths:
    trajectry_path_list = get_sorted_subfolder_paths(folder_path)
    trajectry_name_list = []
    for trajectry_path in trajectry_path_list:
        trajectry_name_list.append(os.path.basename(trajectry_path))

    total_lenth += len(trajectry_name_list)
    # 将轨迹名字写入excel文件
    output_file_name = os.path.basename(folder_path) + ".xlsx"
    output_file_path = os.path.join(parent_folder_path, output_file_name)

    write_list_to_excel(trajectry_name_list, output_file_path)

print("总共有:", total_lenth,"条轨迹被收入")