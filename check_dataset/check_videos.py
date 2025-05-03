import json
import os
import re


def check_lengths(json_path, video_dir):
    mismatches = []

    with open(json_path, 'r') as f:
        info = json.load(f)

    for item in info:
        file_name = item['file_name']
        length = item['length']

        # 构造前缀匹配文件名
        pattern = re.compile(rf"^{file_name}.*_(\d+\.?\d*)\.mp4$")

        matched_file = None
        for filename in os.listdir(video_dir):
            match = pattern.match(filename)
            if match:
                matched_file = filename
                end = float(match.group(1))
                # 比较逻辑
                expected = length if length % 2 == 0 else length + 1
                if expected != end:
                    mismatches.append((file_name, length, end))
                break

        if not matched_file:
            mismatches.append((file_name, length, "NO_MATCH"))

    return mismatches


# 使用路径替换为你本地的路径
train_mismatches = check_lengths('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/video_info_train.json',
                                 '/Users/shuaicongwu/Desktop/MA_resources/ovis_videos/ovis_train_videos_all_V1')
valid_mismatches = check_lengths('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/video_info_valid.json',
                                 '/Users/shuaicongwu/Desktop/MA_resources/ovis_videos/ovis_valid_videos_all_V1')

# 输出不一致项
# print("=== Train Mismatches ===")
# if train_mismatches:
#     for m in train_mismatches:
#         print(m)
# else:
#     print("train没有不一致")
#
# print("\n=== Valid Mismatches ===")
# if valid_mismatches:
#     for m in valid_mismatches:
#         print(m)
# else:
#     print("valid没有不一致")

def check_video_name_list(name_folder, videos_folder):
    # 获取 train 文件夹下所有子文件夹的名称
    train_subfolders = set(os.listdir(name_folder))

    # 获取 videos 文件夹中所有 mp4 文件的前缀名（即第一个下划线之前的部分）
    video_files = [f for f in os.listdir(videos_folder) if f.endswith('.mp4')]
    video_prefixes = set(f.split('_')[0] for f in video_files)

    # 比较两个集合
    only_in_train = train_subfolders - video_prefixes
    only_in_videos = video_prefixes - train_subfolders

    # 输出结果
    print("仅在 train 中存在的子文件夹：", only_in_train)
    print("仅在 videos 中存在但不在 train 中的前缀：", only_in_videos)

    if not only_in_train and not only_in_videos:
        print("两个列表一致。")
    else:
        print("两个列表不一致。")

check_video_name_list('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-ovis/expression/training',
                      '/Users/shuaicongwu/Desktop/MA_resources/ovis_videos/ovis_train_videos_533_V1')
check_video_name_list('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-ovis/expression/valid',
                      '/Users/shuaicongwu/Desktop/MA_resources/ovis_videos/ovis_valid_videos_137_V1')

