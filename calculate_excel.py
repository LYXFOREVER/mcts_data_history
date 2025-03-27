"""
该代码的目的是统计人为的审查结果
"""

from pathlib import Path
import os
import pandas as pd
import json

def get_all_files(folder_path):
    """
    返回指定文件夹内所有文件的路径（不包括子文件夹中的文件），
    并按字符串顺序（字母顺序）排序。
    
    参数:
        folder_path (str): 文件夹路径。
    
    返回:
        list: 文件夹内所有文件的路径字符串列表，按字母顺序排序。
    """
    folder = Path(folder_path)
    file_paths = [str(file.resolve()) for file in folder.iterdir() if file.is_file()]
    file_paths.sort()  # 按字符串顺序排序
    return file_paths

def extract_trajectory_results(excel_path):
    """
    从 Excel 文件中提取轨迹的执行结果。
    
    参数:
        excel_path (str): Excel 文件的路径。
    
    返回:
        list: 包含各个轨迹执行结果（数字）的列表。
    """
    # 读取 Excel 文件
    df = pd.read_excel(excel_path)
    
    results = []
    
    # 遍历每一行
    for index, row in df.iterrows():
        # 遍历每一列，找到第一个数字
        for cell in row:
            if pd.notna(cell) and isinstance(cell, (int, float)):
                results.append(cell)
                break
    
    return results

def extract_first_non_empty_string(excel_path):
    """
    从 Excel 文件中提取第一个非空的字符串。
    
    参数:
        excel_path (str): Excel 文件的路径。
    
    返回:
        list: 包含每个轨迹的第一个非空字符串的列表。
    """
    # 读取 Excel 文件
    df = pd.read_excel(excel_path)
    
    results = []
    
    # 遍历每一行
    for index, row in df.iterrows():
        # 遍历每一列，找到第一个非空的字符串
        for cell in row:
            if pd.notna(cell) and isinstance(cell, str):  # 检查是否为非空字符串
                results.append(cell)
                break
    
    return results

def find_unique_elements(list1, list2):
    """
    比较两个列表，找出独有的元素，并记录它们分别属于哪个列表。
    
    参数:
        list1 (list): 第一个列表。
        list2 (list): 第二个列表。
    
    返回:
        dict: 包含两个列表中独有的元素及其归属信息。
              格式为：{'only_in_list1': [elements], 'only_in_list2': [elements]}
    """
    # 将列表转换为集合
    set1 = set(list1)
    set2 = set(list2)
    
    # 找出独有的元素
    only_in_list1 = set1 - set2  # 在 list1 中但不在 list2 中
    only_in_list2 = set2 - set1  # 在 list2 中但不在 list1 中
    
    # 返回结果
    return {
        'only_in_list1': list(only_in_list1),
        'only_in_list2': list(only_in_list2)
    }

def calculate_proportions(numbers):
    """
    统计列表中各个数字（0、1、2）的比例。
    
    参数:
        numbers (list): 包含 0、1 和 2 的列表。
    
    返回:
        dict: 各个数字的比例，格式为 {0: proportion_0, 1: proportion_1, 2: proportion_2}。
    """
    # 统计每个数字的出现次数
    count_0 = numbers.count(0)
    count_1 = numbers.count(1)
    count_2 = numbers.count(2)
    
    # 计算总元素数
    total = len(numbers)
    
    # 计算比例
    proportions = {
        "0": count_0 / total if total > 0 else 0,
        "1": count_1 / total if total > 0 else 0,
        "2": count_2 / total if total > 0 else 0
    }
    
    return proportions

def majority_vote(lists):
    """
    对一个列表的列表进行多数投票，返回一个新列表，每个位置的值是该位置上出现次数最多的数字。
    
    参数:
        lists (list of list): 一个列表的列表，每个子列表长度相同，内容为数字（0, 1, 2）。
    
    返回:
        list: 投票结果的新列表。
    """
    # 检查输入是否为空
    if not lists:
        return []

    # 获取子列表的长度
    length = len(lists[0])
    
    # 初始化结果列表
    result = []
    
    # 遍历每个位置
    for i in range(length):
        # 统计每个位置上的数字出现次数
        count_0 = 0
        count_1 = 0
        count_2 = 0
        
        for lst in lists:
            if lst[i] == 0:
                count_0 += 1
            elif lst[i] == 1:
                count_1 += 1
            elif lst[i] == 2:
                count_2 += 1
        
        # 选择出现次数最多的数字
        if count_0 >= count_1 and count_0 >= count_2:
            result.append(0)
        elif count_1 >= count_2:
            result.append(1)
        else:
            result.append(2)
    
    return result

def compare_average_difference(a, b):
    """
    比较两个列表 b 和 a 中的数字，计算 b 中的数字平均比 a 中的数字大多少。
    
    参数:
        a (list): 第一个列表，包含数字。
        b (list): 第二个列表，包含数字。
    
    返回:
        float: b 中的数字平均比 a 中的数字大多少。
    
    异常:
        ValueError: 如果两个列表长度不一致。
    """
    # 检查两个列表长度是否一致
    if len(a) != len(b):
        print("a列表长度为:", len(a), "b列表长度为:", len(b))
        print("两个列表的长度不一致，无法进行比较。")
        return None
    
    # 计算 b 中的数字平均比 a 中的数字大多少
    differences = [b[i] - a[i] for i in range(len(a))]
    average_difference = sum(differences) / len(differences)
    
    return average_difference

def compare_difference(a, b):
    """
    比较两个列表 b 和 a 中的数字，计算 b 中的数字比 a 中的数字大多少。
    
    参数:
        a (list): 第一个列表，包含数字。
        b (list): 第二个列表，包含数字。
    
    返回:
        c (list): b 中的数字比 a 中的数字大多少。
    
    异常:
        ValueError: 如果两个列表长度不一致。
    """
    # 检查两个列表长度是否一致
    if len(a) != len(b):
        print("a列表长度为:", len(a), "b列表长度为:", len(b))
        print("两个列表的长度不一致，无法进行比较。")
        return None
    
    # 计算 b 中的数字平均比 a 中的数字大多少
    differences = [b[i] - a[i] for i in range(len(a))]
    
    return differences

def calculate_positive_negative_ratio(numbers):
    """
    计算列表中正数和负数的比例。
    
    参数:
        numbers (list): 包含数字的列表。
    
    返回:
        dict: 包含正数比例和负数比例的字典。
              格式为：{'positive_ratio': float, 'negative_ratio': float}
    """
    if not numbers:  # 如果列表为空，返回 0 比例
        return {'positive_ratio': 0.0, 'negative_ratio': 0.0}
    
    total_count = len(numbers)
    positive_count = sum(1 for num in numbers if num > 0)
    negative_count = sum(1 for num in numbers if num < 0)
    
    positive_ratio = positive_count / total_count
    negative_ratio = negative_count / total_count
    
    return {'positive_ratio': positive_ratio, 'negative_ratio': negative_ratio}

################################################
######             此处可以更改            ######
################################################

if __name__ == "__main__":
    folder = '25_2_25_data_for_check_result'
    expert_list = ['liu_zi_yang', 'zhang_ling_sen', 'zhang_ren_shan'] # 负责统计数据质量的三位专家

    """
    下面这个字典存储了全部的统计结果。结构如下:
    {
        "expert_name_0":{
                            "app_name_0":[0,1,2,0,1……], # 各个轨迹的检查结果
                            "app_name_1":[0,1,2,0,1……],
                            "app_name_2":[0,1,2,0,1……],
                            "total_result":以上几个列表连起来,
                            "proportions":各种轨迹的比例
                        }

        "expert_name_1":{
                            "app_name_0":[0,1,2,0,1……], # 各个轨迹的检查结果
                            "app_name_1":[0,1,2,0,1……],
                            "app_name_2":[0,1,2,0,1……],
                            "total_result":以上几个列表连起来,
                            "proportions":各种轨迹的比例
                        }

        "expert_name_2":{
                            "app_name_0":[0,1,2,0,1……], # 各个轨迹的检查结果
                            "app_name_1":[0,1,2,0,1……],
                            "app_name_2":[0,1,2,0,1……],
                            "total_result":以上几个列表连起来,
                            "proportions":各种轨迹的比例
                        }
        "mean_proportions":全部专家总结的各种轨迹的比例平均
        "major_vote_list":major vote 总体的列表
        "major_vote_proportions":major vote 结果
    }
    """
    calculate_result = {}

    for expert in expert_list:
        print("以下是专家",expert,"的检查结果")
        expert_check_dic = {} # 用于存储该expert统计的结果
        expert_check_list = [] # 用于存储该expert所有统计结果的综合

        excel_folder_path = os.path.join(folder, expert)
        excels_path = get_all_files(excel_folder_path)

        for excel_path in excels_path:
            # 分各个app，获取0,1,2的比例并打印出来
            check_result_list = extract_trajectory_results(excel_path=excel_path)
            excel_name = os.path.basename(excel_path)

            expert_check_dic[excel_name] = check_result_list
            expert_check_list = expert_check_list + check_result_list

            proportions = calculate_proportions(check_result_list)
            print("对于excel:",excel_name,"各总轨迹比例如下:")
            print(proportions)
            expert_check_dic[excel_name+'_proportions'] = proportions

        # 打印总体的0,1,2比例,要写明是哪个专家的
        proportions = calculate_proportions(expert_check_list)
        print("小结，对于专家",expert,",所有轨迹总体的比例如下:")
        print(proportions)
        expert_check_dic["total_result"] = expert_check_list
        expert_check_dic["proportions"] = proportions

        # 将结果记录到calculate_result
        calculate_result[expert] = expert_check_dic

    # 打印所有统计结果的总结果

    all_expert_check_list = []
    for expert in expert_list:
        all_expert_check_list += calculate_result[expert]["total_result"]

    proportions = calculate_proportions(all_expert_check_list)
    print("综合几位专家的结果，各种轨迹比例为:")
    print(proportions)

    calculate_result["mean_proportions"] = proportions


    # 接下来使用投票方法，统计各个轨迹的情况。
    expert_result_list = []
    for expert in expert_list:
        print("在major vote之前，先检查一下各个列表的长度")
        print(len(calculate_result[expert]["total_result"]))
        expert_result_list.append(calculate_result[expert]["total_result"])

    
    major_vote_list = majority_vote(expert_result_list)
    proportions = calculate_proportions(major_vote_list)
    print("令各个专家对各个轨迹进行投票，得到的最终结果是:")
    print(proportions)

    calculate_result["major_vote_list"] = major_vote_list
    calculate_result["major_vote_proportions"] = proportions

    # 记录一下本次都检查了哪些轨迹.格式就是app_name/trajectry_name
    expert = expert_list[0]
    excel_folder_path = os.path.join(folder, expert)
    excels_path = get_all_files(excel_folder_path) # 有按照正确的排序
    trajectry_paths = []
    for excel_path in excels_path:
        trajectry_name_list = extract_first_non_empty_string(excel_path=excel_path)
        excel_name = os.path.basename(excel_path)
        app_name = os.path.splitext(excel_name)[0]
        trajectry_paths.extend([os.path.join(app_name, subfolder) for subfolder in trajectry_name_list])
    
    calculate_result["trajectry_paths"] = trajectry_paths

    # 将本次的检查结果保存
    file_path = os.path.join(folder, "calculate_result.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(calculate_result, f, ensure_ascii=False, indent=4)
