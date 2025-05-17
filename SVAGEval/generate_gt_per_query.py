import os
import json
import time
from collections import defaultdict

def generate_gt_per_query(a_json_path, val_dir, output_root):
    """
    根据 a.json 中的标注信息，生成按 Language Query 划分的 gt.txt 文件。

    参数：
        a_json_path (str): a.json 文件路径。
        val_dir (str): 原始 val 文件夹路径，包含多个视频子文件夹，每个子文件夹下有 gt.txt。
        output_root (str): 输出根目录路径，例如 "gt-per-query/ovis/valid"。
    """
    os.makedirs(output_root, exist_ok=True)

    # 读取 a.json 文件
    with open(a_json_path, 'r', encoding='utf-8') as f:
        annotations = json.load(f)

    gt_cache = {}

    for ann in annotations:
        video = ann["Video"]
        lang_query = ann["Language Query"]
        ids = list(map(int, ann["IDs"].split(",")))
        start = int(ann["Start"])
        end = int(ann["End"])

        # 构建输出目录：gt-per-query/ovis/valid/Video/lang-query/gt.txt
        lang_folder = lang_query.lower().replace(" ", "-")
        out_folder = os.path.join(output_root, video, lang_folder)
        os.makedirs(out_folder, exist_ok=True)
        out_gt_path = os.path.join(out_folder, "gt.txt")

        # 读取 val 下的对应 gt.txt
        val_gt_path = os.path.join(val_dir, video, "gt.txt")
        if not os.path.exists(val_gt_path):
            print(f"⚠️  警告：未找到 {val_gt_path}，跳过。")
            continue

        if val_gt_path not in gt_cache:
            with open(val_gt_path, 'r') as vf:
                gt_lines = [line.strip() for line in vf.readlines()]
            gt_cache[val_gt_path] = gt_lines
        else:
            gt_lines = gt_cache[val_gt_path]

        # 记录已经写入的 (frame_id, track_id)，防止重复写入
        written = set()
        if os.path.exists(out_gt_path):
            with open(out_gt_path, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        written.add((int(parts[0]), int(parts[1])))

        with open(out_gt_path, 'a') as out_f:
            for line in gt_lines:
                parts = line.strip().split(',')
                if len(parts) < 2:
                    continue
                frame_id = int(parts[0])
                track_id = int(parts[1])
                if start <= frame_id <= end and track_id in ids:
                    key = (frame_id, track_id)
                    if key not in written:
                        out_f.write(line + "\n")
                        written.add(key)

# generate_gt_per_query(
#     a_json_path="/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json",
#     val_dir="/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/OVIS_GTs/val",
#     output_root="gt-per-query/ovis/valid"
# )
# print('ovis is done')
#
# generate_gt_per_query(
#     a_json_path="/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-valid-doubled.json",
#     val_dir="/Users/shuaicongwu/PycharmProjects/data_processing/MOT/MOT17_GTs/val",
#     output_root="gt-per-query/mot17/valid"
# )
# print('mot17 is done')
#
# generate_gt_per_query(
#     a_json_path="/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-valid-doubled.json",
#     val_dir="/Users/shuaicongwu/PycharmProjects/data_processing/MOT/MOT20_GTs/val",
#     output_root="gt-per-query/mot20/valid"
# )
# print('mot20 is done')



def slugify(text):
    return text.lower().replace(" ", "-")

def generate_gt_per_query_optimized(a_json_path, val_dir, output_root):
    """
    高效生成按 Language Query 分组的 gt.txt 文件，并打印处理进度。
    """
    start_time = time.time()

    os.makedirs(output_root, exist_ok=True)

    # 1. 读入所有标注并按 video 分组
    with open(a_json_path, 'r', encoding='utf-8') as f:
        annotations = json.load(f)

    video_to_annotations = defaultdict(list)
    for ann in annotations:
        video_to_annotations[ann["Video"]].append(ann)

    total_videos = len(video_to_annotations)
    video_count = 0
    total_queries = len(annotations)
    query_count = 0

    print(f"开始处理 {total_queries} 个 Language Query，来自 {total_videos} 个视频...\n")

    for video, ann_list in video_to_annotations.items():
        video_count += 1
        print(f"[{video_count}/{total_videos}] 正在处理视频: {video}，包含 {len(ann_list)} 个查询...")

        # 2. 读取 val/{video}/gt.txt 并构建索引 {(frame_id, track_id): line}
        val_gt_path = os.path.join(val_dir, video, "gt.txt")
        if not os.path.exists(val_gt_path):
            print(f"⚠️  缺失：{val_gt_path}，跳过 {video}")
            continue

        with open(val_gt_path, 'r') as f:
            gt_lines = [line.strip() for line in f if line.strip()]

        gt_index = defaultdict(list)
        for line in gt_lines:
            parts = line.split(',')
            if len(parts) < 2:
                continue
            frame_id = int(parts[0])
            track_id = int(parts[1])
            gt_index[(frame_id, track_id)].append(line)

        output_buffer = defaultdict(set)

        for ann in ann_list:
            query_count += 1
            lang_query = ann["Language Query"]
            ids = list(map(int, ann["IDs"].split(",")))
            start = int(ann["Start"])
            end = int(ann["End"])
            slug = slugify(lang_query)

            out_folder = os.path.join(output_root, video, slug)
            os.makedirs(out_folder, exist_ok=True)
            out_path = os.path.join(out_folder, "gt.txt")

            print(f"    - [{query_count}/{total_queries}] Query: \"{lang_query}\"")

            for frame_id in range(start, end + 1):
                for track_id in ids:
                    key = (frame_id, track_id)
                    if key in gt_index:
                        for line in gt_index[key]:
                            output_buffer[out_path].add(line)

        # 4. 批量写入
        for path, lines in output_buffer.items():
            with open(path, 'a') as f:
                for line in sorted(lines):
                    f.write(line + '\n')

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\n✅ 所有数据处理完成，耗时 {elapsed:.2f} 秒（约 {elapsed / 60:.2f} 分钟）。")

# generate_gt_per_query_optimized(
#     a_json_path="/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-valid-doubled.json",
#     val_dir="/Users/shuaicongwu/PycharmProjects/data_processing/MOT/MOT20_GTs/val",
#     output_root="gt-per-query/mot20_optimized/valid"
# )
# print('mot20 is done')