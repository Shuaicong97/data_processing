import json
import re

def check_video_frames(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    frame_pattern = re.compile(r'img_(\d+)\.jpg')
    path_prefix_pattern = re.compile(r'^([^/]+)/img_\d+\.jpg')

    non_continuous_videos = []

    for video in data.get("videos", []):
        file_names = video.get("file_names", [])
        frame_info = []

        for name in file_names:
            match = frame_pattern.search(name)
            if match:
                frame_number = int(match.group(1))
                frame_info.append((frame_number, name))

        frame_info.sort()
        frame_numbers = [f[0] for f in frame_info]

        if not frame_numbers:
            continue

        starts_from_one = frame_numbers[0] == 1
        is_continuous = all((b - a) == 1 for a, b in zip(frame_numbers, frame_numbers[1:]))

        # 提取前缀路径名（如 86a88668）
        prefix_match = path_prefix_pattern.match(file_names[0]) if file_names else None
        video_name = prefix_match.group(1) if prefix_match else "unknown"

        if not starts_from_one or not is_continuous:
            non_continuous_videos.append({
                "video_id": video["id"],
                "starts_from": frame_numbers[0],
                "is_continuous": is_continuous,
                "total_frames": len(frame_numbers),
                "video_name": video_name
            })

    print("\n=== 不连续或未从1开始的视频 ===")
    for item in non_continuous_videos:
        print(f"Video ID: {item['video_id']}")
        print(f"  起始帧号: {item['starts_from']}")
        print(f"  是否连续: {item['is_continuous']}")
        print(f"  总帧数: {item['total_frames']}")
        print(f"  视频目录名: {item['video_name']}")
        print("")

# check_video_frames("../OVIS/annotations_train.json")
# check_video_frames("../OVIS/annotations_valid.json")

# with open("../OVIS/annotations_train.json", "r") as f:
#     data = json.load(f)

# 获取目标 annotation 的 bboxes
# target_bbox = None
# for ann in data.get("annotations", []):
#     if ann["video_id"] == 29 and ann["id"] == 215:
#         target_bbox = ann["bboxes"]
#         break
#
# print("Target bboxes:", target_bbox)
#
# for i, box in enumerate(target_bbox):
#     if box is not None:
#         print(i+1, box)

def rename_json_fields_preserve_order(filepath):
    """
    读取指定路径的 JSON 文件，修改字段名后覆盖写回原文件。

    修改规则：
        - "Query ID" -> "QID"
        - "Track ID" -> "IDs"
        - "Start Frame" -> "Start"
        - "End Frame" -> "End"
    """
    rename_map = {
        "Query ID": "QID",
        "Track ID": "IDs",
        "Start Frame": "Start",
        "End Frame": "End"
    }

    target_fields_to_int = {"QID"}

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_data = []
    for item in data:
        new_item = {}
        for key, value in item.items():
            # 替换键名，如果有对应的新键名
            new_key = rename_map.get(key, key)
            if new_key in target_fields_to_int:
                try:
                    num = float(value)
                    if num.is_integer():
                        value = str(int(num))
                    else:
                        value = num
                except (ValueError, TypeError):
                    pass  # 保留原始值
            new_item[new_key] = value
        new_data.append(new_item)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)

# rename_json_fields_preserve_order('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.json')
# rename_json_fields_preserve_order('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.json')
# rename_json_fields_preserve_order('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training.json')
# rename_json_fields_preserve_order('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid.json')
# rename_json_fields_preserve_order('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-training-doubled.json')
# rename_json_fields_preserve_order('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-valid-doubled.json')
# rename_json_fields_preserve_order('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-training-doubled.json')
# rename_json_fields_preserve_order('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-valid-doubled.json')

def check_comma_in_query(data_file):
    # 假设你的 JSON 文件叫 data.json
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 遍历并找出含逗号的 Language Query
    for item in data:
        video = item["Video"]
        query = item.get("Language Query", "")
        if "," in query:
            print(f'{data_file} {video}: {query}')

# expression json files with comma
check_comma_in_query('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-training.json')
check_comma_in_query('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT20-training.json')
check_comma_in_query('/Users/shuaicongwu/PycharmProjects/data_processing/Original/OVIS-training.json')

#
# check_comma_in_query('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-valid.json')
# check_comma_in_query('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT20-valid.json')
# check_comma_in_query('/Users/shuaicongwu/PycharmProjects/data_processing/Original/OVIS-valid.json')

