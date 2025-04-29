import csv
import json

# 加载 video_info_train.json 数据
def load_video_info(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 构建映射：Video ID -> length
    return {item["file_name"]: item["length"] for item in data}

# 遍历 CSV，检查不合规的 Start/End
def check_timestamps(csv_path, video_info_json):
    video_lengths = load_video_info(video_info_json)

    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            video_id = row["Video"]
            start_str = row["Start"]
            end_str = row["End"]

            # 跳过 Start 或 End 为空的情况
            if not start_str or not end_str:
                continue

            try:
                start = float(start_str)
                end = float(end_str)
            except ValueError:
                continue  # 非法数字，跳过

            length = video_lengths.get(video_id)

            if length is None:
                continue  # 视频信息不存在，跳过

            if start > length or end > length:
                print(f"❌ 不合规数据 -> Video: {video_id}, Start: {start}, End: {end}, Length: {length}")

def check_timestamps_in_json(json_data, video_info_json):
    video_lengths = load_video_info(video_info_json)

    for row in json_data:
        video_id = row["Video"]
        start_str = row["Start"]
        end_str = row["End"]

        # 跳过 Start 或 End 为空的情况
        if not start_str or not end_str:
            continue

        try:
            start = float(start_str)
            end = float(end_str)
        except ValueError:
            continue  # 非法数字，跳过

        length = video_lengths.get(video_id)

        if length is None:
            continue  # 视频信息不存在，跳过

        if start > length or end > length:
            print(f"❌ 不合规数据 -> Video: {video_id}, Start: {start}, End: {end}, Length: {length}")

# 示例用法（替换路径）
check_timestamps("../OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS(Ashiq).csv",
                 "../OVIS/video_info_train.json")
check_timestamps("../OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS(Seenat).csv",
                 "../OVIS/video_info_train.json")
check_timestamps("../OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS-Test(Ashiq).csv",
                 "../OVIS/video_info_valid.json")
check_timestamps("../OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS-Test(Seenat).csv",
                 "../OVIS/video_info_valid.json")

# with open("/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json", "r") as f:
#     json_data = json.load(f)
# check_timestamps_in_json(json_data, "../OVIS/video_info_train.json")
# with open("/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json", "r") as f:
#     json_data = json.load(f)
# check_timestamps_in_json(json_data, "../OVIS/video_info_valid.json")