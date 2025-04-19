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

# 示例调用
check_video_frames("../OVIS/annotations_train.json")
check_video_frames("../OVIS/annotations_valid.json")
