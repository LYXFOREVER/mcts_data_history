"""
本代码是统计sft版本的reward函数与人工审核结果的一致性的代码。
需要分成两个部分，一个部分是在orignial或者success的轨迹上的一致性，一部分是在processed版本上的一致性
"""

import json

calculate_result_json_path = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_3_31/data_for_check_result/calculate_result.json" # 记录了人工审核结果的json
language_json_path = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_3_31/data_for_check_result/language.json" # 记录了sft reward判断结果的json

with open(calculate_result_json_path, 'r', encoding='utf-8') as file:
    calculate_result_json = json.load(file)

with open(language_json_path, 'r', encoding='utf-8') as file:
    language_json = json.load(file)

trajectry_paths = calculate_result_json["trajectry_paths"]
human_result = calculate_result_json["major_vote_list"]

sft_reward_result = language_json[0]["pred_labels"]

print(len(trajectry_paths))
print(len(sft_reward_result))

# 有一条失败轨迹dialer/2025_03_31_00_30_50_id_2_r_fail_v_processed，这个轨迹没有做sft reward审查，因此需要被去除
index = trajectry_paths.index("dialer/2025_03_31_00_30_50_id_2_r_fail_v_processed")
del trajectry_paths[index]
del human_result[index]

# 开始逐个轨迹比较
original_result = {
    "h_success_r_success": 0,
    "h_fail_r_fail": 0,
    "h_success_r_fail": 0,
    "h_fail_r_success": 0,
}

processed_result = {
    "h_success_r_success": 0,
    "h_fail_r_fail": 0,
    "h_success_r_fail": 0,
    "h_fail_r_success": 0,
}

for i in range(len(trajectry_paths)):
    # 取得本次需要比较的信息
    trajectry_path = trajectry_paths[i]
    human_result_tag = human_result[i]
    sft_reward_result_tag = sft_reward_result[i]

    # 确定本次的轨迹类型
    suffixes = [
        "original",
        "processed",
        "success"
    ]
    for suffix in suffixes:
        if trajectry_path.endswith(suffix):
            break
    
    if suffix == "original" or suffix == "success":
        # 原始轨迹，没有做过RW
        if human_result_tag == 0:
            # 人类认为这条轨迹是对的
            if sft_reward_result_tag == 1:
                # sft reward认为这条轨迹是对的
                original_result["h_success_r_success"] += 1
            else:
                # sft reward认为这条轨迹是错的
                original_result["h_success_r_fail"] += 1
        else:
            # 人类认为这条轨迹是错的
            if sft_reward_result_tag == 1:
                # sft reward认为这条轨迹是对的
                original_result["h_fail_r_success"] += 1
            else:
                # sft reward认为这条轨迹是错的
                original_result["h_fail_r_fail"] += 1

    else:
        # 做过RW
        if human_result_tag == 0:
            # 人类认为这条轨迹是对的
            if sft_reward_result_tag == 1:
                # sft reward认为这条轨迹是对的
                processed_result["h_success_r_success"] += 1
            else:
                # sft reward认为这条轨迹是错的
                processed_result["h_success_r_fail"] += 1
        else:
            # 人类认为这条轨迹是错的
            if sft_reward_result_tag == 1:
                # sft reward认为这条轨迹是对的
                processed_result["h_fail_r_success"] += 1
            else:
                # sft reward认为这条轨迹是错的
                processed_result["h_fail_r_fail"] += 1

print("对于原始轨迹，sft的准确度如下:")
print(original_result)

print("对于RW轨迹，sft的准确度如下:")
print(processed_result)