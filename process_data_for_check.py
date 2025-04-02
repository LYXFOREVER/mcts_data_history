"""
将 1_processed_data 里的数据移动到 2_data_for_check 中，并将其格式调整为适合检查的格式
总体思路:
对于完成了后处理的轨迹文件们，首先分为两类：
1.reward判断为成功的轨迹
2.reward判断为失败的轨迹

对于情况1，我们会得到三种轨迹：
一种是verifer一开始就判定为5分的完美轨迹。这种轨迹直接保存，轨迹命名为:轨迹原名_r_success_v_success
另外两种种是verifer判定为不到5分的轨迹。对于这种轨迹我们既保存原本的，也保存rw后的。
这两种分别命名为:轨迹原名_r_success_v_original,轨迹原名_r_success_v_processed

对于情况2，我们会得到两种轨迹：
一种是直接把pkl解包得到的轨迹。这种轨迹非常长并且score被标记为0，代表它们是被reward判断为失败的轨迹。它们会被命名为:轨迹原名_r_fail_v_original
一种是将上述轨迹进行后处理得到后的轨迹。这种轨迹往往被截断过，并且有1--5的score。它们会被命名为:轨迹原名_r_fail_v_processed
"""

import os
from process_data_util import *
import json
from calculate_excel import *

processed_data_path = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_4_2/1_processed_data" # 本次后处理完成的轨迹的目标文件夹
data_for_check_path = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_4_2/2_data_for_check" # 给人看的文件夹
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
        # 没有截图，说明是失败轨迹的处理结果.失败轨迹需要被命名为轨迹原名_r_fail_v_original以及轨迹原名_r_fail_v_processed
        # 我们先保存好后处理过的轨迹
            target_trajectry_path_processed = target_trajectry_path + "_r_fail_v_processed"
            # 将图像信息复制过去
            copy_files(os.path.join(trajectry_path, "step_2_downscale_resolution"), target_trajectry_path_processed)
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
                    ui_action_summary_dic["action_output"] = ui_action_summary_dic["action"]
                    ui_action_summary_dic["summary"] = sub_instruction
                
                ui_action_summary_list.append(ui_action_summary_dic)
            
            target_ui_action_summary_list_path = os.path.join(target_trajectry_path_processed, "ui_action_summary.json")
            with open(target_ui_action_summary_list_path, "w", encoding="utf-8") as f:
                json.dump(ui_action_summary_list, f, ensure_ascii=False, indent=4)

            # 处理score.json和task_goal.json
            src_task_goal_path = os.path.join(trajectry_path, "new_task_goal.json")
            src_score_path = os.path.join(trajectry_path, "score.json")
            target_task_goal_path = os.path.join(target_trajectry_path_processed, "task_goal.json")
            target_score_path = os.path.join(target_trajectry_path_processed, "score.json")

            shutil.copy(src_task_goal_path, target_task_goal_path)
            shutil.copy(src_score_path, target_score_path)

        # 接下来保存没有后处理过的，就是把整条轨迹都保存下来，不管什么end_index和新任务描述了
            target_trajectry_path_original = target_trajectry_path + "_r_fail_v_original"
            create_directory(target_trajectry_path_original)
            # 处理图像信息
            step_0_path = os.path.join(trajectry_path, "step_0_raw")
            png_num = count_png_files(step_0_path) # png文件的数量代表这条轨迹总共有多长

            for i in range(png_num):
                # 确定原始图像和目标图像的路径
                image_name = str(i) + '.png'
                image_with_action_name = str(i) + '_with_action.png'
                image_path = os.path.join(step_0_path, image_name)
                output_original_path = os.path.join(target_trajectry_path_original, image_name)
                output_with_action_path = os.path.join(target_trajectry_path_original, image_with_action_name)

                # 获取ui信息
                ui_element_list_name = str(i) + '_ui_element_list.json'
                ui_element_list_path = os.path.join(step_0_path, ui_element_list_name)
                with open(ui_element_list_path, 'r', encoding='utf-8') as file:
                    ui_element_list = json.load(file)

                # 获取动作信息
                action_list_name = 'action.json'
                action_list_path = os.path.join(step_0_path, action_list_name)
                with open(action_list_path, 'r', encoding='utf-8') as file:
                    action_list = json.load(file)
                action_dic = action_list['action_list'][i]

                # 判断是否需要绘制动作
                if "index" in action_dic and len(ui_element_list) >= action_dic["index"]:
                    ui_index = action_dic["index"]
                    ui_bbox = ui_element_list[ui_index]["ui_bbox"]
                    draw_ui_border(image_path, output_with_action_path, ui_bbox)
                else:
                    shutil.copy(image_path, output_with_action_path)
                
                # 不管怎么样，都需要保存一下原始的图像
                shutil.copy(image_path, output_original_path)

            # 处理文本信息
            # 开始设置失败轨迹的ui action summary
            ui_action_summary_list = []
            with open(os.path.join(trajectry_path, "task_goal.json"), "r") as f:
                task_goal_json = json.load(f)
            for id in range(png_num):
                ui_action_summary_dic = {}
                ui_action_summary_dic["id"] = id
                ui_action_summary_dic["task_goal"] = task_goal_json["task_goal"]

                ui_element_list_path = os.path.join(step_0_path, str(id)+'_ui_element_list.json')
                with open(ui_element_list_path, "r") as f:
                    id_ui_element_list_json = json.load(f)
                ui_action_summary_dic["ui_list_description"] = id_ui_element_list_json

                action_json_path = os.path.join(step_0_path, "action.json")
                with open(action_json_path, "r") as f:
                    action_json = json.load(f)
                if id == 0:
                    # 我们的action是“上个状态到达本状态使用的action”，因此第一个是没有action的
                    ui_action_summary_dic["action"] = None
                    ui_action_summary_dic["action_output"] = None
                else:
                    ui_action_summary_dic["action"] = str(action_json["action_list"][id-1])
                    ui_action_summary_dic["action_output"] = action_json["action_output_list"][id-1]+ui_action_summary_dic["action"]
                
                ui_action_summary_list.append(ui_action_summary_dic)
            
            target_ui_action_summary_list_path = os.path.join(target_trajectry_path_original, "ui_action_summary.json")
            with open(target_ui_action_summary_list_path, "w", encoding="utf-8") as f:
                json.dump(ui_action_summary_list, f, ensure_ascii=False, indent=4)

            # 处理score.json和task_goal.json
            src_task_goal_path = os.path.join(trajectry_path, "task_goal.json")
            target_task_goal_path = os.path.join(target_trajectry_path_original, "task_goal.json")
            target_score_path = os.path.join(target_trajectry_path_original, "score.json")

            shutil.copy(src_task_goal_path, target_task_goal_path)
            original_score_dic = {"score": 0,"reason": "reward function return 0."}
            with open(target_score_path, "w", encoding="utf-8") as f:
                json.dump(original_score_dic, f, ensure_ascii=False, indent=4)
        else:
            # 有截图就是成功轨迹的
            # 成功轨迹分三类
            new_score_json_path = os.path.join(trajectry_path, "new_score.json")
            if os.path.exists(new_score_json_path) is True:
                # 有新老分数之分，说明是原始小于5分的，被后处理过的轨迹
                # 这种轨迹需要保存两个版本，一个版本是 轨迹原名_r_success_v_original,另一个是 轨迹原名_r_success_v_processed
                old_score_json_path = os.path.join(trajectry_path, "old_score.json")

                with open(new_score_json_path, "r") as f:
                    new_score_dic = json.load(f)
                new_score = new_score_dic["score"]

                with open(old_score_json_path, "r") as f:
                    old_score_dic = json.load(f)
                old_score = new_score_dic["score"]

            # 首先处理processed版本
                target_trajectry_path_processed = target_trajectry_path+"_r_success_v_processed"
                create_directory(target_trajectry_path_processed)
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
                target_ui_action_summary_list_path = os.path.join(target_trajectry_path_processed, "ui_action_summary.json")
                with open(target_ui_action_summary_list_path, "w", encoding="utf-8") as f:
                    json.dump(new_ui_action_summary_json, f, ensure_ascii=False, indent=4)

                ## TODO:处理task goal与score
                src_task_goal_path = os.path.join(trajectry_path, "new_task_goal.json")
                src_score_path = os.path.join(trajectry_path, "new_score.json")
                target_task_goal_path = os.path.join(target_trajectry_path_processed, "task_goal.json")
                target_score_path = os.path.join(target_trajectry_path_processed, "score.json")

                shutil.copy(src_task_goal_path, target_task_goal_path)
                shutil.copy(src_score_path, target_score_path)

                # TODO:处理图像
                for i in range(end_index):
                    num_png_path = os.path.join(trajectry_path, str(i)+'.png')
                    num_som_png_path = os.path.join(trajectry_path, str(i)+'_som.png')
                    num_with_action_png_path = os.path.join(trajectry_path, str(i)+'_with_action.png')

                    target_num_png_path = os.path.join(target_trajectry_path_processed, str(i)+'.png')
                    target_num_som_png_path = os.path.join(target_trajectry_path_processed, str(i)+'_som.png')
                    target_num_with_action_png_path = os.path.join(target_trajectry_path_processed, str(i)+'_with_action.png')

                    if os.path.exists(num_png_path) is True:
                        shutil.copy(num_png_path, target_num_png_path)
                    
                    if os.path.exists(num_som_png_path) is True:
                        shutil.copy(num_som_png_path, target_num_som_png_path)

                    if os.path.exists(num_with_action_png_path) is True:
                        shutil.copy(num_with_action_png_path, target_num_with_action_png_path)

            # 然后处理orignal版本的
                # 使用老任务描述与老轨迹。基本上也是复制，但是要删除掉end_index.json,new_score.json,new_task_goal.json,old_score.json
                target_trajectry_path_original = target_trajectry_path+"_r_success_v_original"
                copy_files_except_pkl(trajectry_path, target_trajectry_path_original)
                os.remove(os.path.join(target_trajectry_path_original, "end_index.json"))
                os.remove(os.path.join(target_trajectry_path_original, "new_score.json"))
                os.remove(os.path.join(target_trajectry_path_original, "new_task_goal.json"))
                os.remove(os.path.join(target_trajectry_path_original, "old_score.json"))

            else:
                # 没有新老分数之分，那就是原始5分轨迹。这种轨迹只需要复制就好
                target_trajectry_path_success = target_trajectry_path+"_r_success_v_success"
                copy_files_except_pkl(trajectry_path, target_trajectry_path_success)
                
