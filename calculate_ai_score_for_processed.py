"""
统计各种ai评分情况.给后处理过的轨迹们使用
"""
import os
from process_data_util import *
import json
from calculate_excel import *

filtered_fail_data_for_check = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_3_27/1_processed_data" # 本次后处理完成的轨迹的目标文件夹
filtered_app_trajectry_paths = get_sorted_subfolder_paths(filtered_fail_data_for_check) # 获取本次完成后处理的app的文件夹路径
# 为成功轨迹准备的统计
score_count_dic = {
    "1":0,
    "2":0,
    "3":0,
    "4":0,
    "5":0,
}
# 为失败轨迹准备的统计
score_count_dic_fail = {
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
        # 首先判断一下是那种类型的轨迹的后处理结果
        if os.path.exists(os.path.join(trajectry_path, "0.png")) is False:
            # 没有截图，说明是失败轨迹的处理结果
            score_json_path = os.path.join(trajectry_path, "score.json")
            with open(score_json_path, 'r', encoding='utf-8') as file:
                score_json = json.load(file)
            score = score_json["score"]
            score_count_dic_fail[str(score)] += 1
        else:
            # 有截图就是成功轨迹的
            score_json_path = os.path.join(trajectry_path, "score.json")
            new_score_json_path = os.path.join(trajectry_path, "new_score.json")
            if os.path.exists(new_score_json_path) is True:
                # 有新老分数之分，说明是原始小于5分的，被后处理过的轨迹
                with open(score_json_path, 'r', encoding='utf-8') as file:
                    score_json = json.load(file)
                with open(new_score_json_path, 'r', encoding='utf-8') as file:
                    new_score_json = json.load(file)
                if score_json["score"] >= new_score_json["score"]:
                    score = score_json["score"]
                else:
                    score = new_score_json["score"]
                score_count_dic[str(score)] += 1
            else:
                # 没有新老分数之分，那就是原始5分轨迹
                with open(score_json_path, 'r', encoding='utf-8') as file:
                    score_json = json.load(file)
                score = score_json["score"]
                score_count_dic[str(score)] += 1
            print("本条轨迹为", trajectry_path,", 最终分数为", score)
            
print("对于成功轨迹而言")
print("所有分数的分布为", score_count_dic)
calculate_weighted_average_and_total(score_count_dic)

print("对于失败轨迹而言")
print("所有分数的分布为", score_count_dic_fail)
calculate_weighted_average_and_total(score_count_dic_fail)

output_path = os.path.join(filtered_fail_data_for_check, "score_distruption_success.png")
plot_bar_chart(score_count_dic, output_path)

output_path = os.path.join(filtered_fail_data_for_check, "score_distruption_fail.png")
plot_bar_chart(score_count_dic_fail, output_path)