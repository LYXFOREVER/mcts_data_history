"""
统计各种ai评分情况.给原始轨迹使用，因此也不会统计失败轨迹的情况
25-4-9 新增统计轨迹长度分布功能
"""
import os
from process_data_util import *
import json
from calculate_excel import *

data_for_check = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_4_15"
original_data_for_check = os.path.join(data_for_check, "0_original_data") # 本次后处理完成的轨迹的目标文件夹
original_data_for_check_paths = get_sorted_subfolder_paths(original_data_for_check) # 获取本次完成后处理的app的文件夹路径
# 为成功轨迹准备的统计
score_count_dic = {
    "1":0,
    "2":0,
    "3":0,
    "4":0,
    "5":0,
}

# 为轨迹们统计长度分布
lenth_count_dic_success = {}

for filtered_app_trajectry_path in original_data_for_check_paths:
    print("本次要处理的app为:",filtered_app_trajectry_path)
    trajectry_paths = get_sorted_subfolder_paths(filtered_app_trajectry_path)
    for trajectry_path in trajectry_paths:
        # 首先判断一下是那种类型的轨迹的后处理结果
        if os.path.exists(os.path.join(trajectry_path, "0.png")) is False:
            # 没有截图，说明是失败轨迹，直接跳过
            continue
        else:
            # 有截图就是成功轨迹的
            # 统计分数
            score_json_path = os.path.join(trajectry_path, "score.json")
            with open(score_json_path, 'r', encoding='utf-8') as file:
                score_json = json.load(file)
            score = score_json["score"]
            score_count_dic[str(score)] += 1

            # 统计长度。对于原版轨迹，查看ui_action_summary.json就知道是多长
            ui_action_summary_json_path = os.path.join(trajectry_path, "ui_action_summary.json")
            with open(ui_action_summary_json_path, 'r', encoding='utf-8') as file:
                ui_action_summary_json = json.load(file)
            trajectry_lenth_str = str(len(ui_action_summary_json))
            current_count = lenth_count_dic_success.get(trajectry_lenth_str, 0)
            lenth_count_dic_success[trajectry_lenth_str] = current_count+1
            
            print("本条轨迹为", trajectry_path,", 最终分数为", score,", 轨迹长度为:",trajectry_lenth_str)

score_count_dic = {k: score_count_dic[k] for k in sorted(score_count_dic, key=int)}
lenth_count_dic_success = {k: lenth_count_dic_success[k] for k in sorted(lenth_count_dic_success, key=int)}

print("对于成功轨迹而言")
print("所有分数的分布为", score_count_dic)
calculate_weighted_average_and_total(score_count_dic)
print("所有轨迹长度分布为:", lenth_count_dic_success)
calculate_weighted_average_and_total(lenth_count_dic_success)


output_path = os.path.join(original_data_for_check, "score_distruption_success.png")
plot_bar_chart(score_count_dic, output_path)


output_path = os.path.join(original_data_for_check, "lenth_distruption_success.png")
plot_bar_chart(lenth_count_dic_success, output_path)
