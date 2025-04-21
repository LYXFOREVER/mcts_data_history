"""
统计各种ai评分情况.给后处理过的轨迹们使用
25-4-9 新增统计轨迹长度分布功能
"""
import os
from process_data_util import *
import json
from calculate_excel import *

data_for_check = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_4_15"
filtered_fail_data_for_check = os.path.join(data_for_check, "1_processed_data") # 本次后处理完成的轨迹的目标文件夹
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

# 为轨迹们统计长度分布
lenth_count_dic_success = {}
lenth_count_dic_fail = {}

for filtered_app_trajectry_path in filtered_app_trajectry_paths:
    print("本次要处理的app为:",filtered_app_trajectry_path)
    trajectry_paths = get_sorted_subfolder_paths(filtered_app_trajectry_path)
    for trajectry_path in trajectry_paths:
        # 首先判断一下是那种类型的轨迹的后处理结果
        if os.path.exists(os.path.join(trajectry_path, "0.png")) is False:
            # 没有截图，说明是失败轨迹的处理结果
            # 先统计分数
            score_json_path = os.path.join(trajectry_path, "score.json")
            with open(score_json_path, 'r', encoding='utf-8') as file:
                score_json = json.load(file)
            score = score_json["score"]
            score_count_dic_fail[str(score)] += 1

            # 统计长度
            end_index_json_path = os.path.join(trajectry_path, "end_index.json")
            with open(end_index_json_path, 'r', encoding='utf-8') as file:
                end_index_json = json.load(file)
            trajectry_lenth_str = str(end_index_json["end_index"])
            current_count = lenth_count_dic_fail.get(trajectry_lenth_str, 0)
            lenth_count_dic_fail[trajectry_lenth_str] = current_count+1
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
                    # 统计长度。对于原版轨迹，查看ui_action_summary.json就知道是多长
                    ui_action_summary_json_path = os.path.join(trajectry_path, "ui_action_summary.json")
                    with open(ui_action_summary_json_path, 'r', encoding='utf-8') as file:
                        ui_action_summary_json = json.load(file)
                    trajectry_lenth_str = str(len(ui_action_summary_json))
                    current_count = lenth_count_dic_success.get(trajectry_lenth_str, 0)
                    lenth_count_dic_success[trajectry_lenth_str] = current_count+1
                else:
                    score = new_score_json["score"]
                    # 统计长度.对于改写后更好的轨迹，，查看endindex 就知道有多长
                    end_index_json_path = os.path.join(trajectry_path, "end_index.json")
                    with open(end_index_json_path, 'r', encoding='utf-8') as file:
                        end_index_json = json.load(file)
                    trajectry_lenth_str = str(end_index_json["end_index"])
                    current_count = lenth_count_dic_success.get(trajectry_lenth_str, 0)
                    lenth_count_dic_success[trajectry_lenth_str] = current_count+1
                score_count_dic[str(score)] += 1

                
            else:
                # 没有新老分数之分，那就是原始5分轨迹
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
score_count_dic_fail = {k: score_count_dic_fail[k] for k in sorted(score_count_dic_fail, key=int)}
lenth_count_dic_success = {k: lenth_count_dic_success[k] for k in sorted(lenth_count_dic_success, key=int)}
lenth_count_dic_fail = {k: lenth_count_dic_fail[k] for k in sorted(lenth_count_dic_fail, key=int)}

print("对于成功轨迹而言")
print("所有分数的分布为", score_count_dic)
calculate_weighted_average_and_total(score_count_dic)
print("所有轨迹长度分布为:", lenth_count_dic_success)
calculate_weighted_average_and_total(lenth_count_dic_success)

print("对于失败轨迹而言")
print("所有分数的分布为", score_count_dic_fail)
calculate_weighted_average_and_total(score_count_dic_fail)
print("所有轨迹长度分布为:", lenth_count_dic_fail)
calculate_weighted_average_and_total(lenth_count_dic_fail)

output_path = os.path.join(filtered_fail_data_for_check, "score_distruption_success.png")
plot_bar_chart(score_count_dic, output_path)

output_path = os.path.join(filtered_fail_data_for_check, "score_distruption_fail.png")
plot_bar_chart(score_count_dic_fail, output_path)

output_path = os.path.join(filtered_fail_data_for_check, "lenth_distruption_success.png")
plot_bar_chart(lenth_count_dic_success, output_path)

output_path = os.path.join(filtered_fail_data_for_check, "lenth_distruption_fail.png")
plot_bar_chart(lenth_count_dic_fail, output_path)