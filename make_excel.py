"""
本代码的工作是根据data_for_check当中保存的轨迹生成一个与之对应的excel文件
"""
import os
from process_data_util import *

folder_name = "com.tencent.mtt"
folder_path = os.path.join("data_for_check", folder_name)

trajectry_path_list = get_sorted_subfolder_paths(folder_path)
trajectry_name_list = []
for trajectry_path in trajectry_path_list:
    trajectry_name_list.append(os.path.basename(trajectry_path))

# 将轨迹名字写入excel文件
output_file_name = folder_name + ".xlsx"
output_file_path = os.path.join("data_for_check", output_file_name)

write_list_to_excel(trajectry_name_list, output_file_path)