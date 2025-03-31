"""
将 1_processed_data 里的数据移动到 2_data_for_check 中，并将其格式调整为适合检查的格式
"""

import os
from process_data_util import *
import json
from calculate_excel import *

processed_data_path = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_3_27/1_processed_data" # 本次后处理完成的轨迹的目标文件夹
data_for_check_path = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_3_27/2_data_for_check" # 给人看的文件夹
app_folder_paths = get_sorted_subfolder_paths(processed_data_path) # 获取本次完成后处理的app的文件夹路径

for app_folder_path in app_folder_paths:
    print("本次要处理的app为:",app_folder_path)
    trajectry_paths = get_sorted_subfolder_paths(app_folder_path)
    data_for_check_app_folder_path = os.path.join(data_for_check_path, os.path.basename(app_folder_path))
    for trajectry_path in trajectry_paths:
        # 首先判断一下是那种类型的轨迹的后处理结果
        trajectry_path_name = os.path.basename(trajectry_path) # 本次要处理的轨迹的名字
        target_trajectry_path = os.path.join(data_for_check_app_folder_path, trajectry_path_name)
        if os.path.exists(os.path.join(trajectry_path, "0.png")) is False:
            # 没有截图，说明是失败轨迹的处理结果
            create_directory(target_trajectry_path)
            # 将图像信息复制过去
            copy_files(os.path.join(trajectry_path, "step_2_downscale_resolution"), target_trajectry_path)
            # 接下来复制文本信息
            with open(os.path.join(trajectry_path, "end_index.json"), "r") as f:
                end_index_json = json.load(f)
            end_index = end_index_json["end_index"]

            # 开始设置失败轨迹的ui action summary
            ui_action_summary_list = []
            with open(os.path.join(trajectry_path, "new_task_goal.json"), "r") as f:
                task_goal_json = json.load(f)
            for id in range(end_index):
                ui_action_summary_dic = {}
                ui_action_summary_dic["id"] = id
                ui_action_summary_dic["task_goal"] = task_goal_json["task_goal"]

                step_1_redundancy_removal_path = os.path.join(trajectry_path, "step_1_redundancy_removal")
                ui_element_list_path = os.path.join(step_1_redundancy_removal_path, str(id)+'_ui_element_list.json')
                with open(ui_element_list_path, "r") as f:
                    id_ui_element_list_json = json.load(f)
                ui_action_summary_dic["ui_list_description"] = id_ui_element_list_json

                action_json_path = os.path.join(step_1_redundancy_removal_path, "action.json")
                with open(action_json_path, "r") as f:
                    action_json = json.load(f)
                if id == 0:
                    # 我们的action是“上个状态到达本状态使用的action”，因此第一个是没有action的
                    ui_action_summary_dic["action"] = None
                    ui_action_summary_dic["action_output"] = None
                else:
                    ui_action_summary_dic["action"] = str(action_json["action_list"][id-1])
                    step_3_low_level_description_path = os.path.join(trajectry_path, "step_3_low_level_description")
                    sub_instruction_list_json_path = os.path.join(step_3_low_level_description_path, "sub_instruction_list.json")
                    with open(sub_instruction_list_json_path, "r") as f:
                        sub_instruction_list = json.load(f)
                    sub_instruction = sub_instruction_list[id-1]
                    ui_action_summary_dic["action_output"] = sub_instruction+ui_action_summary_dic["action"]
                
                ui_action_summary_list.append(ui_action_summary_dic)
            
            target_ui_action_summary_list_path = os.path.join(target_trajectry_path, "ui_action_summary.json")
            with open(target_ui_action_summary_list_path, "w", encoding="utf-8") as f:
                json.dump(ui_action_summary_list, f, ensure_ascii=False, indent=4)

            # 处理score.json和task_goal.json
            src_task_goal_path = os.path.join(trajectry_path, "new_task_goal.json")
            src_score_path = os.path.join(trajectry_path, "score.json")
            target_task_goal_path = os.path.join(target_trajectry_path, "task_goal.json")
            target_score_path = os.path.join(target_trajectry_path, "score.json")

            shutil.copy(src_task_goal_path, target_task_goal_path)
            shutil.copy(src_score_path, target_score_path)


        else:
            # 有截图就是成功轨迹的
            new_score_json_path = os.path.join(trajectry_path, "new_score.json")
            if os.path.exists(new_score_json_path) is True:
                # 有新老分数之分，说明是原始小于5分的，被后处理过的轨迹
                # 首先检查新老分数哪个高，这个决定了要使用哪个任务描述
                old_score_json_path = os.path.join(trajectry_path, "old_score.json")

                with open(new_score_json_path, "r") as f:
                    new_score_dic = json.load(f)
                new_score = new_score_dic["score"]

                with open(old_score_json_path, "r") as f:
                    old_score_dic = json.load(f)
                old_score = new_score_dic["score"]

                if new_score > old_score:
                    # 新分数高，使用新任务描述与新轨迹。新轨迹有截断
                    with open(os.path.join(trajectry_path, "end_index.json"), "r") as f:
                        end_index_json = json.load(f)
                    end_index = end_index_json["end_index"]

                    # 处理文本信息
                    ## 处理ui action summary
                    with open(os.path.join(trajectry_path, "ui_action_summary.json"), "r") as f:
                        old_ui_action_summary_json = json.load(f)
                    new_ui_action_summary_json = old_ui_action_summary_json[:end_index]

                    with open(os.path.join(trajectry_path, "new_task_goal.json"), "r") as f:
                        new_task_goal_json = json.load(f)

                    step_3_low_level_description_path = os.path.join(trajectry_path, "step_3_low_level_description")
                    step_3_low_level_description_list_path = os.path.join(step_3_low_level_description_path, "sub_instruction_list.json")
                    with open(step_3_low_level_description_list_path, "r") as f:
                        sub_instruction_list = json.load(f)
                    ### action_output需要修改，summary也需要去掉，因为它们对应的是原任务的
                    for i in range(end_index):
                        new_ui_action_summary_json[i]["task_goal"] = new_task_goal_json["task_goal"]
                        new_ui_action_summary_json[i]["summary"] = None
                        new_ui_action_summary_json[i]["summary_prompt"] = None
                        new_ui_action_summary_json[i]["reward_output"] = None
                        if i != 0:
                            # 只有非0的才有action_output
                            new_ui_action_summary_json[i]["action_output"] = sub_instruction_list[i-1]+new_ui_action_summary_json[i]["action"]
                    
                    # new_ui_action_summary_json处理完毕，可以保存
                    target_ui_action_summary_list_path = os.path.join(target_trajectry_path, "ui_action_summary.json")
                    with open(target_ui_action_summary_list_path, "w", encoding="utf-8") as f:
                        json.dump(new_ui_action_summary_json, f, ensure_ascii=False, indent=4)

                    ## TODO:处理task goal与score
                    src_task_goal_path = os.path.join(trajectry_path, "new_task_goal.json")
                    src_score_path = os.path.join(trajectry_path, "new_score.json")
                    target_task_goal_path = os.path.join(target_trajectry_path, "task_goal.json")
                    target_score_path = os.path.join(target_trajectry_path, "score.json")

                    shutil.copy(src_task_goal_path, target_task_goal_path)
                    shutil.copy(src_score_path, target_score_path)

                    # TODO:处理图像
                    for i in range(end_index):
                        num_png_path = os.path.join(trajectry_path, str(i)+'.png')
                        num_som_png_path = os.path.join(trajectry_path, str(i)+'_som.png')
                        num_with_action_png_path = os.path.join(trajectry_path, str(i)+'_with_action.png')

                        target_num_png_path = os.path.join(target_trajectry_path, str(i)+'.png')
                        target_num_som_png_path = os.path.join(target_trajectry_path, str(i)+'_som.png')
                        target_num_with_action_png_path = os.path.join(target_trajectry_path, str(i)+'_with_action.png')

                        if os.path.exists(num_png_path) is True:
                            shutil.copy(num_png_path, target_num_png_path)
                        
                        if os.path.exists(num_som_png_path) is True:
                            shutil.copy(num_som_png_path, target_num_som_png_path)

                        if os.path.exists(num_with_action_png_path) is True:
                            shutil.copy(num_with_action_png_path, target_num_with_action_png_path)

                
                else:
                    # 使用老任务描述与老轨迹。基本上也是复制，但是要删除掉end_index.json,new_score.json,new_task_goal.json,old_score.json
                    copy_files_except_pkl(trajectry_path, target_trajectry_path)
                    os.remove(os.path.join(target_trajectry_path, "end_index.json"))
                    os.remove(os.path.join(target_trajectry_path, "new_score.json"))
                    os.remove(os.path.join(target_trajectry_path, "new_task_goal.json"))
                    os.remove(os.path.join(target_trajectry_path, "old_score.json"))

            else:
                # 没有新老分数之分，那就是原始5分轨迹。这种轨迹只需要复制就好
                copy_files_except_pkl(trajectry_path, target_trajectry_path)
                
