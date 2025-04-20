import os
from collections import defaultdict
import glob

def check_valid_videos():
    valid_dir = '/nfs/data3/shuaicong/refer-ovis/OVIS/valid'
    video_dir = '/nfs/data3/shuaicong/videos_by_images/ovis_valid_V1'

    # 获取所有子文件夹名称
    subfolders = [name for name in os.listdir(valid_dir)
                  if os.path.isdir(os.path.join(valid_dir, name))]

    # 获取所有视频文件名称
    video_files = os.listdir(video_dir)

    # 创建一个集合方便匹配
    video_prefixes = set()
    for vf in video_files:
        if vf.endswith('.mp4'):
            prefix = vf.split('_')[0]
            video_prefixes.add(prefix)

    # 查找没有对应视频的子文件夹
    for sub in subfolders:
        if sub not in video_prefixes:
            print(f"缺少视频: {sub}")

def check_training_videos():
    # 定义路径
    valid_dir = "/nfs/data3/shuaicong/refer-ovis/OVIS/training"
    video_dir = "/nfs/data3/shuaicong/videos_by_images/ovis_V1"

    # 获取所有子文件夹名称
    subfolders = [name for name in os.listdir(valid_dir) if os.path.isdir(os.path.join(valid_dir, name))]

    # 统计视频匹配数量
    match_count = defaultdict(int)

    # 遍历视频目录，找出每个视频对应的前缀（子文件夹名）
    for video_file in os.listdir(video_dir):
        if video_file.endswith(".mp4"):
            prefix = video_file.split("_")[0]
            match_count[prefix] += 1

    # 输出匹配数量大于1的子文件夹
    for folder in subfolders:
        if match_count[folder] != 1:
            print(f"{folder}: {match_count[folder]} matches")

    # 统计 valid_dir 中的子文件夹数量
    valid_subfolders = [d for d in os.listdir(valid_dir) if os.path.isdir(os.path.join(valid_dir, d))]
    num_valid_folders = len(valid_subfolders)

    # 统计 video_dir 中的 .mp4 文件数量
    video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
    num_videos = len(video_files)

    # 输出结果
    print(f"子文件夹数量（valid_dir）: {num_valid_folders}")
    print(f"视频数量（video_dir）: {num_videos}")

    # 获取 valid_dir 中的所有子文件夹名称（如 012b09a0）
    valid_subfolders = set([d for d in os.listdir(valid_dir) if os.path.isdir(os.path.join(valid_dir, d))])

    # 遍历 video_dir，提取视频前缀（如 012b09a0）
    video_prefixes = {}
    for video_file in os.listdir(video_dir):
        if video_file.endswith(".mp4"):
            prefix = video_file.split("_")[0]
            video_prefixes.setdefault(prefix, []).append(video_file)

    # 查找不在 valid_dir 中的前缀（即多出来的）
    extra_prefixes = [prefix for prefix in video_prefixes if prefix not in valid_subfolders]

    # 输出多出来的内容
    for prefix in extra_prefixes:
        print(f"多余视频前缀: {prefix}")
    for video in video_prefixes[prefix]:
        print(f"  - {video}")

# 视频长度是否正确
valid_dir = "/nfs/data3/shuaicong/refer-ovis/OVIS/training"
video_dir = "/nfs/data3/shuaicong/videos_by_images/ovis_V1"

for subfolder in os.listdir(valid_dir):
    subfolder_path = os.path.join(valid_dir, subfolder)
    if os.path.isdir(subfolder_path):
        jpg_files = glob.glob(os.path.join(subfolder_path, "*.jpg"))
        length = len(jpg_files)

        # 查找对应的mp4文件
        video_pattern = os.path.join(video_dir, f"{subfolder}_*.mp4")
        mp4_files = glob.glob(video_pattern)

        for mp4_file in mp4_files:
            mp4_name = os.path.basename(mp4_file)
            try:
                end_str = mp4_name.split('_')[-1].replace(".mp4", "")
                end = int(float(end_str))
                if (length % 2 == 1 and length + 1 != end) or (length % 2 == 0 and length != end):
                    print(mp4_name, 'length: ', length, 'end: ', end)
            except Exception as e:
                print(f"Error processing {mp4_name}: {e}")