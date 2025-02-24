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