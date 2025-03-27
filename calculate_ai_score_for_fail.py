"""
统计一下打过复活赛的失败轨迹的平均分，分数情况等
"""
import os
from process_data_util import *
import json
from calculate_excel import *

filtered_fail_data_for_check = "filtered_fail_data_for_check" # 本次后处理完成的轨迹的文件夹
filtered_app_trajectry_paths = get_sorted_subfolder_paths(filtered_fail_data_for_check) # 获取本次完成后处理的app的文件夹路径

score_count_dic = {
    "1":0,
    "2":0,
    "3":0,
    "4":0,
    "5":0,
}

for filtered_app_trajectry_path in filtered_app_trajectry_paths:
    print("本次要处理的app为:",filtered_app_trajectry_path)
    trajectry_paths = get_sorted_subfolder_paths(filtered_app_trajectry_path)
    for trajectry_path in trajectry_paths:
        score_json_path = os.path.join(trajectry_path, "score.json")
        with open(score_json_path, 'r', encoding='utf-8') as file:
            score_json = json.load(file)
        print("本条轨迹为", trajectry_path,", 复活后的分数为", score_json)
        score = score_json["score"]
        score_count_dic[str(score)] += 1

print("所有分数的分布为", score_count_dic)
calculate_weighted_average_and_total(score_count_dic)

output_path = os.path.join(filtered_fail_data_for_check, "score_distruption.png")
plot_bar_chart(score_count_dic, output_path)