import json
import os
import shutil

def extract_vid(input_file, output_file):
    # 保存唯一的vid
    unique_vids = set()

    # 读取jsonl文件
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            vid = data.get("vid")
            if vid:
                unique_vids.add(vid)

    # 写入txt文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for vid in sorted(unique_vids):
            f.write(f"{vid}\n")

    print(f"共提取并保存了 {len(unique_vids)} 个唯一vid到 {output_file}")

extract_vid("OVIS/ovis_train_release.jsonl", "OVIS/ovis_train_vid.txt")
extract_vid("OVIS/ovis_val_release.jsonl", "OVIS/ovis_val_vid.txt")
extract_vid("MOT17/mot17_train_release.jsonl", "MOT17/mot17_train_vid.txt")
extract_vid("MOT17/mot17_val_release.jsonl", "MOT17/mot17_val_vid.txt")
extract_vid("MOT20/mot20_train_release.jsonl", "MOT20/mot20_train_vid.txt")
extract_vid("MOT20/mot20_val_release.jsonl", "MOT20/mot20_val_vid.txt")


def copy_target_videos(txt_path, source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)

    # 读取vid列表
    with open(txt_path, 'r') as f:
        vid_list = [line.strip() for line in f if line.strip()]

    # 遍历并复制文件
    for vid in vid_list:
        mp4_name = f"{vid}.mp4"
        src_path = os.path.join(source_dir, mp4_name)
        dst_path = os.path.join(target_dir, mp4_name)

        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            # print(f"已复制：{mp4_name}")
        else:
            print(f"未找到：{mp4_name}")

    # 统计目标文件夹中.mp4文件的数量
    saved_files = [f for f in os.listdir(target_dir) if f.endswith(".mp4")]
    print(f"\n目标文件夹中共保存了 {len(saved_files)} 个 .mp4 文件。")

# copy_target_videos("ovis_train_vid.txt", "/Users/shuaicongwu/Desktop/ovis_videos/ovis_train_videos_all_V1",
#                    "/Users/shuaicongwu/Desktop/ovis_videos/ovis_train_videos_533_V1")
# copy_target_videos("ovis_val_vid.txt", "/Users/shuaicongwu/Desktop/ovis_videos/ovis_valid_videos_all_V1",
#                    "/Users/shuaicongwu/Desktop/ovis_videos/ovis_valid_videos_137_V1")


def extract_queries(input_file, output_file):
    # 存储提取的query
    queries = []

    # 读取jsonl文件
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            queries.append(data['query'])

    # 将queries写入json文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(queries, f, ensure_ascii=False, indent=4)

    print(f"共提取并保存了 {len(queries)} 个query到 {output_file}")

extract_queries('OVIS/ovis_train_release.jsonl', 'OVIS/OVIS_train_queries.json')
extract_queries('OVIS/ovis_val_release.jsonl', 'OVIS/OVIS_val_queries.json')
extract_queries('MOT17/mot17_train_release.jsonl', 'MOT17/mot17_train_queries.json')
extract_queries('MOT17/mot17_val_release.jsonl', 'MOT17/mot17_val_queries.json')
extract_queries('MOT20/mot20_train_release.jsonl', 'MOT20/mot20_train_queries.json')
extract_queries('MOT20/mot20_val_release.jsonl', 'MOT20/mot20_val_queries.json')
