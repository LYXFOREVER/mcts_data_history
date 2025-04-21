"""
此前的ui_action_summary.json中记录的ui边界坐标都是纯坐标，没有归一化。这里是将ui坐标改成归一化并*1000的代码
本代码
"""
import os
from process_data_util import *
import json
from calculate_excel import *


data_for_check_path = "/data7/Users/lyx/code/mcts_dataset/data_for_check_25_3_31/2_data_for_check" # 给人看的文件夹
app_folder_paths = get_sorted_subfolder_paths(data_for_check_path) # 获取本次完成后处理的app的文件夹路径

for app_folder_path in app_folder_paths:
    print("本次要处理的app为:",app_folder_path)
    trajectry_paths = get_sorted_subfolder_paths(app_folder_path)
    for trajectry_path in trajectry_paths:
        ui_action_summary_json_path = os.path.join(trajectry_path, "ui_action_summary.json")
        with open(ui_action_summary_json_path, 'r', encoding='utf-8') as file:
            ui_action_summary_json = json.load(file)
        
        for step_dic in ui_action_summary_json:
            if "ui_bbox_normalized" in step_dic and step_dic["ui_bbox_normalized"] is True:
                # 说明做过归一化了
                continue
            # 获取本次要处理的ui所在图像的长宽
            id = step_dic["id"]
            img_path = os.path.join(trajectry_path, str(id)+".png")
            with Image.open(img_path) as img:
                width, height = img.size
            ui_list_description = step_dic["ui_list_description"]
            for ui_element in ui_list_description:
                ui_bbox = ui_element["ui_bbox"] # 获取ui坐标
                ui_bbox[0] = int(float(ui_bbox[0])/float(width) * 1000)
                ui_bbox[1] = int(float(ui_bbox[1])/float(width) * 1000)
                ui_bbox[2] = int(float(ui_bbox[2])/float(height) * 1000)
                ui_bbox[3] = int(float(ui_bbox[3])/float(height) * 1000)
            step_dic["ui_bbox_normalized"] = True
        with open(ui_action_summary_json_path, 'w', encoding='utf-8') as file:
            json.dump(ui_action_summary_json, file, ensure_ascii=False, indent=4)
