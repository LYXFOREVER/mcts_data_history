"""
本代码的工作是挑选长度符合要求的轨迹，将合适的轨迹放入单独的文件夹，统计信息
25-3-13 新增将失败轨迹放入指定文件夹的功能
"""
# 25-2-24-19-15 按照至少5步的要求，筛选了bilibili，酷狗，微博，QQ浏览器，腾讯视频5个app，共91条轨迹
from process_data_util import *
import os
import json

folder_name_list = ["com.kugou.android", "com.sina.weibo", "com.tencent.mtt", "com.tencent.qqlive", "tv.danmaku.bili"]

for folder_name in folder_name_list:
    destination_folder = "data_for_check" # 长度达标的轨迹的文件夹
    fail_destination_folder = "fail_data_for_check" # 任务失败的轨迹文件夹
    minimal_lenth = 5 # 对于轨迹长度的要求
    trajectry_path_list = get_sorted_subfolder_paths(folder_name)

    qualified_trajectry_path_list = []
    failed_trajectry_path_list = []

    for trajectry_path in trajectry_path_list:
        ui_action_path = os.path.join(trajectry_path,"ui_action_summary.json")
        if os.path.exists(ui_action_path) is False:
            failed_trajectry_path_list.append(trajectry_path)
            continue
        with open(ui_action_path) as file:
            data = json.load(file)
        trajectry_lenth = len(data)

        if trajectry_lenth >= minimal_lenth:
            qualified_trajectry_path_list.append(trajectry_path)

    print("文件夹",folder_name,"当中共有",len(qualified_trajectry_path_list),"个轨迹长度符合标准")
    print("文件夹",folder_name,"当中共有",len(failed_trajectry_path_list),"个轨迹失败")

    destination_folder_for_this_app = os.path.join(destination_folder, folder_name) # 不同app的轨迹放在不同的地方
    failed_destination_folder_for_this_app = os.path.join(fail_destination_folder, folder_name) # 不同app的轨迹放在不同的地方

    for qualified_trajectry_path in qualified_trajectry_path_list:
        copy_folder(src=qualified_trajectry_path, dst=destination_folder_for_this_app)
    for failed_trajectry_path in failed_trajectry_path_list:
        copy_folder(src=failed_trajectry_path, dst=failed_destination_folder_for_this_app)