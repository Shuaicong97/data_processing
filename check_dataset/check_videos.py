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
                                 '/Users/shuaicongwu/Desktop/ovis_videos/ovis_training_V1')
valid_mismatches = check_lengths('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/video_info_valid.json',
                                 '/Users/shuaicongwu/Desktop/ovis_videos/ovis_valid_V1')

# 输出不一致项
print("=== Train Mismatches ===")
if train_mismatches:
    for m in train_mismatches:
        print(m)
else:
    print("train没有不一致")

print("\n=== Valid Mismatches ===")
if valid_mismatches:
    for m in valid_mismatches:
        print(m)
else:
    print("valid没有不一致")
