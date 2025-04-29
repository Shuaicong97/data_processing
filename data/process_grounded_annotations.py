import json
import os
import shutil
import csv


def print_number_of_videos():
    with open('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json', 'r') as file:
        data = json.load(file)

    # 提取唯一的 Video 值
    videos = [entry['Video'] for entry in data]
    unique_videos = set(videos)
    unique_count = len(unique_videos)

    # 将唯一的视频值保存到文件
    with open('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/ours_unique_valid_videos.txt', 'w') as file:
        for video in unique_videos:
            file.write(f"{video}\n")

    print(f"总共有 {unique_count} 不同的valid videos。")


def check_and_move_directories(original_dir, target_dir, txt_file):
    # 读取txt文件中的唯一视频值
    with open(txt_file, 'r') as file:
        video_names = set(line.strip() for line in file.readlines())

    # 遍历目录A中的所有子文件夹
    for folder_name in os.listdir(original_dir):
        folder_path = os.path.join(original_dir, folder_name)

        # 确保是文件夹
        if os.path.isdir(folder_path):
            # 检查文件夹名是否在txt文件中
            if folder_name not in video_names:
                # 如果不在txt文件中，将该文件夹（及其内容）移动到目录B
                target_path = os.path.join(target_dir, folder_name)

                # 确保目标目录B中没有同名文件夹
                if not os.path.exists(target_path):
                    shutil.move(folder_path, target_path)
                    print(f"文件夹 {folder_name} 已移动到 {target_dir}")
                else:
                    print(f"文件夹 {folder_name} 已存在于目标目录 {target_dir}，跳过移动")

check_and_move_directories('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-ovis/OVIS/labels_with_ids/valid',
                           '/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/unneeded_videos',
                           '/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/ours_unique_valid_videos.txt')


def filter_and_save_csv(input_file, output_file, isTrain):
    """
    该方法会遍历输入的CSV文件，检查每一条记录的 'IDs', 'Start', 'End' 列
    是否有空值，若没有空值则将记录保存到输出的CSV文件中。

    :param input_file: 输入的CSV文件路径
    :param output_file: 输出的CSV文件路径
    """
    try:
        # 打开输入文件进行读取
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            # 读取表头
            header = next(reader)

            # 创建并打开输出文件进行写入
            with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
                writer = csv.writer(outfile)

                # 写入表头
                if isTrain:
                    writer.writerow(["Video", "QID", "Language Query", "Type", "IDs", "Start", "End", "Revision"])
                else:
                    writer.writerow(["ID mark frame", "Video", "QID", "Language Query", "Type", "IDs", "Start", "End", "Revision"])

                # 遍历每一行记录
                for row in reader:
                    # 检查 'IDs', 'Start', 'End' 是否有空值
                    if row[4] and row[5] and row[6]:  # 'IDs' = row[4], 'Start' = row[5], 'End' = row[6]
                        # 如果没有空值，写入输出文件
                        writer.writerow(row)

        print(f"数据已成功保存到 {output_file} 文件中！")

    except Exception as e:
        print(f"处理文件时发生错误: {e}")

# filter_and_save_csv('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations Minimum Version - OVIS-training.csv',
#                     '/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/OVIS-training.csv',
#                     True)
#
# filter_and_save_csv('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations Minimum Version - OVIS-valid.csv',
#                     '/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/OVIS-valid.csv',
#                     False)

def convert_csv_to_json(csv_filename, json_filename, isTrain):
    data = []

    # 读取CSV文件
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # 遍历每一行记录并格式化
        for row in reader:
            # 检查 row["IDs"] 是否是整数
            try:
                int(row["IDs"])  # 尝试将 "IDs" 转为整数
            except ValueError:
                # 如果转换失败，说明 "IDs" 不是整数，打印该行
                print("非整数 ID 行：", row)

            if isTrain:
                record = {
                    "Video": row["Video"],
                    "QID": row["QID"] if row["QID"] else "",  # 如果QID为空，设置为 ""
                    "Language Query": row["Language Query"],
                    "Type": row["Type"],
                    "IDs": row["IDs"],
                    "Start": row["Start"],
                    "End": row["End"],
                    "Revision": row["Revision"] if row["Revision"] else ""  # 如果Revision为空，设置为 ""
                }
            else:
                record = {
                    "ID mark frame": row["ID mark frame"],
                    "Video": row["Video"],
                    "QID": row["QID"] if row["QID"] else "",
                    "Language Query": row["Language Query"],
                    "Type": row["Type"],
                    "IDs": row["IDs"],
                    "Start": row["Start"],
                    "End": row["End"],
                    "Revision": row["Revision"] if row["Revision"] else ""
                }

            data.append(record)

    # 保存为JSON文件
    with open(json_filename, mode='w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4, ensure_ascii=False)

# convert_csv_to_json('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/OVIS-training.csv',
#                     '/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/OVIS-training.json', True)
# convert_csv_to_json('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/OVIS-valid.csv',
#                     '/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/OVIS-valid.json', False)

