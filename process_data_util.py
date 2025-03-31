from pathlib import Path
import os
import shutil
from openpyxl import Workbook

def get_sorted_subfolder_paths(folder_path: str | Path) -> list[Path]:
    """
    获取指定文件夹内所有子文件夹的路径，并按名字顺序排序。

    参数:
        folder_path (str | Path): 父文件夹的路径。

    返回:
        list[Path]: 按名字顺序排序的子文件夹路径列表。
    """
    folder_path = Path(folder_path)  # 确保路径是 Path 对象
    if not folder_path.exists() or not folder_path.is_dir():
        raise ValueError(f"路径 {folder_path} 不存在或不是一个文件夹。")

    # 获取所有子文件夹路径
    subfolder_paths = [subfolder for subfolder in folder_path.iterdir() if subfolder.is_dir()]

    # 按名字排序
    subfolder_paths.sort(key=lambda p: p.name)

    return subfolder_paths

def create_directory(directory_path):
    try:
        # 如果文件夹不存在，则创建文件夹
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
        else:
            print(f"Directory already exists: {directory_path}")
    except OSError as error:
        print(f"Error: {error.strerror}. Directory: {directory_path}")

def copy_folder(src: str, dst: str) -> None:
    """
    复制整个文件夹（包括文件夹本身）到目标路径。
    如果目标路径不存在，则会自动创建。

    参数:
        src (str): 源文件夹路径。
        dst (str): 目标文件夹路径。
    """
    # 检查源文件夹是否存在
    if not os.path.exists(src) or not os.path.isdir(src):
        raise FileNotFoundError(f"源文件夹 '{src}' 不存在或不是一个文件夹。")

    # 获取源文件夹的父目录和文件夹名称
    src_folder_name = os.path.basename(src)
    dst_full_path = os.path.join(dst, src_folder_name)

    # 如果目标路径不存在，创建目标路径
    if not os.path.exists(dst):
        os.makedirs(dst)
        print(f"目标路径 '{dst}' 已创建。")

    # 复制整个文件夹
    try:
        shutil.copytree(src, dst_full_path, dirs_exist_ok=True)
        print(f"整个文件夹 '{src}' 已成功复制到 '{dst_full_path}'。")
    except Exception as e:
        print(f"复制文件夹时出错：{e}")
        print("目标文件夹可能已存在。本次操作不会覆盖该文件夹")

def copy_files(src_dir, dst_dir):
    # 检查源文件夹是否存在
    if not os.path.exists(src_dir):
        print(f"Source directory does not exist: {src_dir}")
        return
    
    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        print(f"Destination directory created: {dst_dir}")
    
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename)
        
        # 确保是文件而不是文件夹
        if os.path.isfile(src_file):
            # 复制文件
            shutil.copy2(src_file, dst_file)
            print(f"Copied file: {src_file} to {dst_file}")

def copy_files_except_pkl(src_dir, dst_dir):
    # 检查源文件夹是否存在
    if not os.path.exists(src_dir):
        print(f"Source directory does not exist: {src_dir}")
        return
    
    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        print(f"Destination directory created: {dst_dir}")
    
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename)
        
        # 确保是文件而不是文件夹
        if os.path.isfile(src_file):
            # 忽略以 .pkl 结尾的文件
            if filename.endswith('.pkl'):
                print(f"Skipping file: {src_file} (ends with .pkl)")
                continue
            
            # 复制文件
            shutil.copy2(src_file, dst_file)
            print(f"Copied file: {src_file} to {dst_file}")

def write_list_to_excel(data_list, output_file):
    """
    将字符串列表逐行写入 Excel 文件。

    参数:
        data_list (list[str]): 包含字符串的列表。
        output_file (str): 输出的 Excel 文件路径。
    """
    # 创建一个新的工作簿
    workbook = Workbook()
    sheet = workbook.active  # 获取当前活动的工作表

    # 将列表中的每个字符串写入 Excel 的一行
    for index, item in enumerate(data_list, start=1):
        sheet.cell(row=index, column=1, value=item)  # 写入到第一列

    # 保存工作簿
    workbook.save(output_file)
    print(f"数据已成功写入文件：{output_file}")

def calculate_weighted_average_and_total(score_count_dic):
    """
    计算并打印数字的加权平均值和总出现次数。
    
    参数:
        score_count_dic (dict): 一个字典，其中的键是数字（"1", "2", "3", "4", "5"），值是这些数字出现的次数。
    """
    total_count = 0
    weighted_sum = 0

    for score, count in score_count_dic.items():
        total_count += count
        weighted_sum += int(score) * count

    if total_count > 0:
        weighted_average = weighted_sum / total_count
    else:
        weighted_average = 0

    print(f"加权平均值: {weighted_average}")
    print(f"总轨迹数: {total_count}")

import matplotlib.pyplot as plt

def plot_bar_chart(score_count_dic, output_path):
    """
    绘制柱状图，显示每个数字的出现次数，并保存到指定路径。
    
    参数:
        score_count_dic (dict): 一个字典，其中的键是数字（"1", "2", "3", "4", "5"），值是这些数字出现的次数。
        output_path (str): 保存柱状图的路径。
    """
    # 提取数字和对应的出现次数
    scores = list(score_count_dic.keys())
    counts = list(score_count_dic.values())

    # 绘制柱状图
    plt.figure(figsize=(8, 6))
    plt.bar(scores, counts, color='skyblue')
    plt.xlabel('Scores')
    plt.ylabel('Counts')
    plt.title('Score Counts')
    plt.xticks(scores)  # 确保 x 轴标签显示所有数字

    # 保存图表到指定路径
    plt.savefig(output_path)
    plt.close()

    print(f"柱状图已保存到 {output_path}")