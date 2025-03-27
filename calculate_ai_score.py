"""
统计ai给出的评分和认为给出的评分之间的差异。人为评分可能包括0，1，2.ai评分则在1~5之间。这些是什么对应关系？人为的0相当于5，其余的相当与1~4
"""
import os
from process_data_util import *
import json
from calculate_excel import *

data_for_check_path = "data_for_check" # 本次ai评分的轨迹的文件夹
filtered_data_for_check = "filtered_data_for_check" # 本次后处理完成的轨迹的文件夹
app_trajectry_paths = get_sorted_subfolder_paths(data_for_check_path) # 获取本次的各个app的文件夹路径
filtered_app_trajectry_paths = get_sorted_subfolder_paths(filtered_data_for_check) # 获取本次完成后处理的app的文件夹路径
data_for_check_human_path = "25_2_25_data_for_check_result" # 本次人工评分的结果保存文件夹
# 合格的轨迹至少要有多少分
min_score = 5

score_list = []
ai_scored_trajecry_path_total_list = []
for app_trajectry_path in app_trajectry_paths:
    print("本次要处理的app为:",app_trajectry_path)
    trajectry_paths = get_sorted_subfolder_paths(app_trajectry_path)
    trajectry_paths.pop(0)  #########################因为原来的审查bug，不得不删掉每个app的第一个轨迹
    ai_scored_trajecry_path_total_list.extend(trajectry_paths)

    for trajecry_path in trajectry_paths:
        score_json_path = os.path.join(trajecry_path, "score.json")
        with open(score_json_path, "r", encoding="utf-8") as json_file:
            score_dic = json.load(json_file)
        score = score_dic["score"]
        score_list.append(score)

# 读取之前获取的calculate_result.json
calculate_result_json_path = os.path.join(data_for_check_human_path, "calculate_result.json")
with open(calculate_result_json_path, "r", encoding="utf-8") as json_file:
    calculate_result = json.load(json_file)

# 现在可以了。两边的app顺序一样了
major_vote_result_list = calculate_result["major_vote_list"] 

# 现在是要比较这两个列表的差异。score评分为5相当于人类评分为0，score评分为其他相当于认为评分为其他
# 首先确认两个列表一样长
ai_true_hu_true = 0
ai_true_hu_flase = 0
ai_flase_hu_true = 0
ai_flase_hu_flase = 0
if len(score_list)==len(major_vote_result_list):
    for i in range(len(score_list)):
        if score_list[i] >= min_score and major_vote_result_list[i] in (0, 1):
            # ai和人都认为是对的
            ai_true_hu_true += 1
        elif score_list[i] >= min_score and major_vote_result_list[i] not in (0,1):
            # ai认为对，人认为错
            ai_true_hu_flase += 1
        elif score_list[i] < min_score and major_vote_result_list[i] in (0, 1):
            # ai认为错，人认为对
            ai_flase_hu_true += 1
        elif score_list[i] < min_score and major_vote_result_list[i] not in (0,1):
            # ai认为错，人也认为错
            ai_flase_hu_flase += 1
    print("本次参与的共有:", len(score_list),"条轨迹")
    print("ai和人都认为是对的有:", ai_true_hu_true)
    print("ai认为对，人认为错的有:", ai_true_hu_flase)
    print("ai认为错，人认为对的有:", ai_flase_hu_true)
    print("ai认为错，人也认为错的有:", ai_flase_hu_flase)

    print("总体正确率有:", (ai_true_hu_true+ai_flase_hu_flase)/len(score_list))
    print("在ai认为正确的轨迹当中，有:",ai_true_hu_flase/(ai_true_hu_flase+ai_true_hu_true),"的轨迹在人看来是错的")
    print("在ai认为错误的轨迹当中，有:",ai_flase_hu_true/(ai_flase_hu_true+ai_flase_hu_flase),"的轨迹在人看来是对的")
else:
    print("出现问题，ai评价数量和人工评价数量不一样?")
    print("ai score长度为:",len(score_list))
    print("major_vote_result_list长度为:",len(major_vote_result_list))

    # 检查是哪些轨迹不一样
    human_trajectrys = calculate_result["trajectry_paths"] # 人工检查过的轨迹
    ai_scored_trajecry_path_total_list = [str(path).replace('data_for_check/', '') for path in ai_scored_trajecry_path_total_list]
    unique_elements_dic = find_unique_elements(ai_scored_trajecry_path_total_list, human_trajectrys)
    print("only_in_ai_scored_trajecry_path_total_list:", unique_elements_dic['only_in_list1'])
    print("only_in_human_trajectrys:", unique_elements_dic['only_in_list2'])



# TODO:检查复活赛能加多少分
print("开始比较原始轨迹和进行了task goal gen的轨迹评分上升了多少")
filtered_score_list = []
filtered_scored_trajecry_path_total_list = []
for filtered_app_trajectry_path in filtered_app_trajectry_paths:
    print("本次要处理的app为:",filtered_app_trajectry_path)
    trajectry_paths = get_sorted_subfolder_paths(filtered_app_trajectry_path)
    trajectry_paths.pop(0)  #########################因为原来的审查bug，不得不删掉每个app的第一个轨迹
    filtered_scored_trajecry_path_total_list.extend(trajectry_paths)

    for trajecry_path in trajectry_paths:
        score_json_path = os.path.join(trajecry_path, "score.json")
        old_score_json_path = os.path.join(trajecry_path, "old_score.json")
        new_score_json_path = os.path.join(trajecry_path, "new_score.json")
        if os.path.exists(score_json_path) is True:
            with open(score_json_path, "r", encoding="utf-8") as json_file:
                score_dic = json.load(json_file)
            score = score_dic["score"]
            filtered_score_list.append(score)
        else:
            with open(old_score_json_path, "r", encoding="utf-8") as json_file:
                old_score_dic = json.load(json_file)
            old_score = old_score_dic["score"]
            with open(new_score_json_path, "r", encoding="utf-8") as json_file:
                new_score_dic = json.load(json_file)
            new_score = new_score_dic["score"]
            if new_score > old_score:
                filtered_score_list.append(new_score)
            else:
                filtered_score_list.append(old_score)

average_difference = compare_average_difference(score_list, filtered_score_list)
if average_difference is not None:
    print("后处理让轨迹的评分平均上升了:", average_difference)
    differences_list = compare_difference(score_list, filtered_score_list)
    positive_sum = 0
    for index, difference in enumerate(differences_list):
        if difference != 0:
            print("对于轨迹:", ai_scored_trajecry_path_total_list[index],",task goal gen前后的分数变化为:", difference)
        
        if difference > 0:
            positive_sum += difference
    p_n_radio = calculate_positive_negative_ratio(differences_list)
    print(p_n_radio)
    positive_average = positive_sum/(len(score_list)*p_n_radio["positive_ratio"])
    print("对于task goal gen有效的轨迹，评分平均提升了:",positive_average)
else:
    print("出现异常，检查一下是怎么回事")
    ai_scored_trajecry_path_total_list = [str(path).replace('data_for_check/', '') for path in ai_scored_trajecry_path_total_list]
    filtered_trajecry_path_total_list = [str(path).replace('filtered_data_for_check/', '') for path in filtered_scored_trajecry_path_total_list]
    unique_elements_dic = find_unique_elements(ai_scored_trajecry_path_total_list, filtered_trajecry_path_total_list)
    print("only_in_ai_scored_trajecry_path_total_list:", unique_elements_dic['only_in_list1'])
    print("only_in_filtered_trajecry_path_total_list:", unique_elements_dic['only_in_list2'])