"""
本代码的主要功能是统计data_for_check版本的轨迹的评分以及其对应的reward函数判断结果
该代码的作用主要在于评价reward函数，vercify函数的准确度，以及复活赛让轨迹复活的成功率。评价依据是人类审核的结果

25-4-10 新增检查data_for_check版本数据信息的功能
"""

import os
from process_data_util import *
import json
from calculate_excel import *

TRAJECTRY_SUCCESS = 0
TRAJECTRY_FAIL = 1
V_SCORE_SUCCESS = (5,)
V_SCORE_ALMOST_SUCCESS = (4,)

data_for_check = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_4_15"

filtered_fail_data_for_check = os.path.join(data_for_check, "2_data_for_check") # 本次后处理完成的轨迹的目标文件夹
filtered_app_trajectry_paths = get_sorted_subfolder_paths(filtered_fail_data_for_check) # 获取本次完成后处理的app的文件夹路径
calculate_result_path = os.path.join(data_for_check, "data_for_check_result/calculate_result.json")

# 看一下有没有人类审核结果
if os.path.exists(calculate_result_path) is True:
    with open(calculate_result_path, 'r', encoding='utf-8') as file:
        calculate_result = json.load(file)
    total_trajectry_paths = calculate_result["trajectry_paths"] # 记录了所有轨迹的app，轨迹名信息的列表，用来和人类审核结果对应
    major_vote_list = calculate_result["major_vote_list"] # 记录了所有轨迹的人类审核结果的列表

    result_dic = {
        "r_fail_v_original_h_success": 0,
        "r_fail_v_original_h_fail": 0,
        "r_fail_v_processed_success_h_success": 0,
        "r_fail_v_processed_success_h_fail": 0,
        "r_fail_v_processed_fail_h_success": 0,
        "r_fail_v_processed_fail_h_fail": 0,
        "r_success_v_original_h_success": 0,
        "r_success_v_original_h_fail": 0,
        "r_success_v_processed_success_h_success": 0,
        "r_success_v_processed_success_h_fail": 0,
        "r_success_v_processed_fail_h_success": 0,
        "r_success_v_processed_fail_h_fail": 0,
        "r_success_v_success_h_success": 0,
        "r_success_v_success_h_fail": 0,
    }
    suffixes_dic = {
        "r_fail_v_original": 0,
        "r_fail_v_processed": 0,
        "r_success_v_original": 0,
        "r_success_v_processed": 0,
        "r_success_v_success": 0,
    }
    v_almost_success_h_success = 0
    for filtered_app_trajectry_path in filtered_app_trajectry_paths:
        trajectry_paths = get_sorted_subfolder_paths(filtered_app_trajectry_path)
        for trajectry_path in trajectry_paths:
            trajectry_path = str(trajectry_path)
            # 首先判断一下是哪种类型的轨迹
            # 分为:r_fail_v_original r_fail_v_processed r_success_v_original r_success_v_processed r_success_v_success
            suffixes = [
                "r_fail_v_original",
                "r_fail_v_processed",
                "r_success_v_original",
                "r_success_v_processed",
                "r_success_v_success"
            ]
            for suffix in suffixes:
                if trajectry_path.endswith(suffix):
                    break
            
            # 获取本轨迹的v评分
            score_json_path = os.path.join(trajectry_path, "score.json")
            with open(score_json_path, 'r', encoding='utf-8') as file:
                score_dic = json.load(file)
            score = score_dic["score"]
            
            # 接着取出本条轨迹的最后两个部分，用来查看属于哪个app的那一条轨迹
            parts = trajectry_path.split('/')
            trajectry_app_and_name = '/'.join(parts[-2:])
            # 取得本轨迹的人工审核结果
            index = total_trajectry_paths.index(trajectry_app_and_name)
            human_result = major_vote_list[index]
            
            # TODO:区分各种轨迹类型，各自统计r,v的准确度（通过和人类比较）
            if suffix == "r_fail_v_original":
                suffixes_dic["r_fail_v_original"] += 1
                # 检查r的准确度
                if human_result == TRAJECTRY_FAIL:
                    result_dic["r_fail_v_original_h_fail"] += 1
                elif human_result == TRAJECTRY_SUCCESS:
                    result_dic["r_fail_v_original_h_success"] += 1
            
            elif suffix == "r_fail_v_processed":
                suffixes_dic["r_fail_v_processed"] += 1
                # 检查v的准确度
                if score in V_SCORE_SUCCESS:
                    # v认为其成功
                    if human_result == TRAJECTRY_FAIL:
                        result_dic["r_fail_v_processed_success_h_fail"] += 1
                    elif human_result == TRAJECTRY_SUCCESS:
                        result_dic["r_fail_v_processed_success_h_success"] += 1
                else:
                    # v认为其不成功
                    if human_result == TRAJECTRY_FAIL:
                        result_dic["r_fail_v_processed_fail_h_fail"] += 1
                    elif human_result == TRAJECTRY_SUCCESS:
                        result_dic["r_fail_v_processed_fail_h_success"] += 1
                        if score in V_SCORE_ALMOST_SUCCESS:
                            v_almost_success_h_success += 1

            elif suffix == "r_success_v_original":
                suffixes_dic["r_success_v_original"] += 1
                # 检查r和v的准确度
                if human_result == TRAJECTRY_FAIL:
                    result_dic["r_success_v_original_h_fail"] += 1
                elif human_result == TRAJECTRY_SUCCESS:
                    result_dic["r_success_v_original_h_success"] += 1
            
            elif suffix == "r_success_v_processed":
                suffixes_dic["r_success_v_processed"] += 1
                # 检查v的准确度
                if score in V_SCORE_SUCCESS:
                    # v认为其成功
                    if human_result == TRAJECTRY_FAIL:
                        result_dic["r_success_v_processed_success_h_fail"] += 1
                    elif human_result == TRAJECTRY_SUCCESS:
                        result_dic["r_success_v_processed_success_h_success"] += 1
                else:
                    # v认为其不成功
                    if human_result == TRAJECTRY_FAIL:
                        result_dic["r_success_v_processed_fail_h_fail"] += 1
                    elif human_result == TRAJECTRY_SUCCESS:
                        result_dic["r_success_v_processed_fail_h_success"] += 1
                        if score in V_SCORE_ALMOST_SUCCESS:
                            v_almost_success_h_success += 1

            elif suffix == "r_success_v_success":
                suffixes_dic["r_success_v_success"] += 1
                # 检查r和v的准确度
                if human_result == TRAJECTRY_FAIL:
                    result_dic["r_success_v_success_h_fail"] += 1
                elif human_result == TRAJECTRY_SUCCESS:
                    result_dic["r_success_v_success_h_success"] += 1
            

    print("r,v与人类审核的差异如下:")
    print(result_dic)
    #print("其中，v_fail_h_success虽然有", result_dic["v_fail_h_success"],"个，但是其中v给了高分（没有达到最高分）的有:",v_almost_success_h_success,"个")
    print("以下是各种轨迹的分布")
    print(suffixes_dic)

    # TODO:比较original版本的和processed版本的区别。从比较评分差异与人类审核结果差异可以看出来
    rw_result_dic = {
        "h_success_v_success":0,
        "h_fail_v_fail":0,
        "h_success_v_fail":0,
        "h_fail_v_success":0,
    }

    for filtered_app_trajectry_path in filtered_app_trajectry_paths:
        trajectry_paths = get_sorted_subfolder_paths(filtered_app_trajectry_path)
        for trajectry_path in trajectry_paths:
            trajectry_path = str(trajectry_path)
            # 首先判断一下是哪种类型的轨迹
            # 分为:r_fail_v_original r_fail_v_processed r_success_v_original r_success_v_processed r_success_v_success
            suffixes = [
                "r_fail_v_original",
                "r_fail_v_processed",
                "r_success_v_original",
                "r_success_v_processed",
                "r_success_v_success"
            ]
            for suffix in suffixes:
                if trajectry_path.endswith(suffix):
                    break
            
            # 取得原版评分
            score_json_path = os.path.join(trajectry_path, "score.json")
            with open(score_json_path, 'r', encoding='utf-8') as file:
                score_dic = json.load(file)
            score = score_dic["score"]

            # 接着取出本条轨迹的最后两个部分，用来查看属于哪个app的那一条轨迹
            parts = trajectry_path.split('/')
            trajectry_app_and_name = '/'.join(parts[-2:])
            # 取得本轨迹的人工审核结果
            index = total_trajectry_paths.index(trajectry_app_and_name)
            human_result = major_vote_list[index]
            
            # 获取本轨迹的processed版本
            if suffix == "r_fail_v_original":
                # 取得processed版本的v评分
                processed_trajectry_path = trajectry_path.replace(suffix, "r_fail_v_processed")
            elif suffix == "r_success_v_original":
                processed_trajectry_path = trajectry_path.replace(suffix, "r_success_v_processed")
            else:
                # 本条轨迹不是original的轨迹，跳过
                continue
            
            processed_score_json_path = os.path.join(processed_trajectry_path, "score.json")
            with open(processed_score_json_path, 'r', encoding='utf-8') as file:
                processed_score_dic = json.load(file)
            processed_score = processed_score_dic["score"]

            # 取得processed版本的人工审核结果
            processed_parts = processed_trajectry_path.split('/')
            processed_trajectry_app_and_name = '/'.join(processed_parts[-2:])
            # 取得本轨迹的人工审核结果
            processed_index = total_trajectry_paths.index(processed_trajectry_app_and_name)
            processed_human_result = major_vote_list[processed_index]

            if human_result == TRAJECTRY_FAIL and processed_human_result == TRAJECTRY_SUCCESS:
                # 在人类看来打赢了复活赛
                #if score not in V_SCORE_SUCCESS and processed_score in V_SCORE_SUCCESS:
                if score < processed_score:
                    # v认为轨迹打赢了复活赛
                    rw_result_dic["h_success_v_success"] += 1
                else:
                    # v不认为轨迹打赢了复活赛
                    rw_result_dic["h_success_v_fail"] += 1
            else:
                # 在人类看来复活赛没打赢
                #if score not in V_SCORE_SUCCESS and processed_score in V_SCORE_SUCCESS:
                if score < processed_score:
                    # v认为轨迹打赢了复活赛
                    rw_result_dic["h_fail_v_success"] += 1
                else:
                    # v不认为轨迹打赢了复活赛
                    rw_result_dic["h_fail_v_fail"] += 1

    print("RW环节的结果如下:")
    print(rw_result_dic)


else:
    print("没有检测到人类审核结果，因此本次只做常规检查")

# 不管怎么样，都要进行一次常规的检查  

# 统计各类轨迹的长度分布
suffixes_dic = {
    #"r_fail_v_original": {}, # 这个没什么意义，先排除
    "r_fail_v_processed": {},
    "r_success_v_original": {},
    "r_success_v_processed": {},
    "r_success_v_success": {},
    "total":{},
}
for filtered_app_trajectry_path in filtered_app_trajectry_paths:
    trajectry_paths = get_sorted_subfolder_paths(filtered_app_trajectry_path)
    for trajectry_path in trajectry_paths:
        trajectry_path = str(trajectry_path)
        suffixes = [
            "r_fail_v_original",
            "r_fail_v_processed",
            "r_success_v_original",
            "r_success_v_processed",
            "r_success_v_success"
        ]
        for suffix in suffixes:
            if trajectry_path.endswith(suffix):
                break
        
        if suffix == "r_fail_v_original":
            # 失败轨迹的原始轨迹没什么好统计的
            continue
        # 读取ui_action_summary.json，获取轨迹长度
        ui_action_summary_json_path = os.path.join(trajectry_path, "ui_action_summary.json")
        with open(ui_action_summary_json_path, 'r', encoding='utf-8') as file:
            ui_action_summary_json = json.load(file)
        lenth = len(ui_action_summary_json)
        trajectry_lenth_str = str(lenth)
        current_count = suffixes_dic[suffix].get(trajectry_lenth_str, 0)
        suffixes_dic[suffix][trajectry_lenth_str] = current_count+1
        suffixes_dic["total"][trajectry_lenth_str] = current_count+1

for suffix, lenth_dic in suffixes_dic.items():
    lenth_dic = {k: lenth_dic[k] for k in sorted(lenth_dic, key=int)}
    suffixes_dic[suffix] = lenth_dic
    output_path = os.path.join(filtered_fail_data_for_check, suffix+".png")
    plot_bar_chart(lenth_dic, output_path)

print("本次轨迹的各个种类的长度分布如下:")
print(suffixes_dic)

