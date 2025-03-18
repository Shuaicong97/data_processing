# {
#     "qid": 8737,
#     "query": "A family is playing basketball together on a green court outside.",
#     "duration": 126,
#     "vid": "bP5KfdFJzC4_660.0_810.0",
#     "relevant_windows": [[0, 16]],
#     "relevant_clip_ids": [0, 1, 2, 3, 4, 5, 6, 7],
#     "saliency_scores": [[4], [4], [4], [4], [4], [4], [4], [4]]
# }

import json

def get_unique_query(file_name, output_file_name):
    # 读取 ovis.json 文件
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 使用集合去重
    unique_entries = set()
    filtered_data = []

    for item in data:
        key = (item["Video"], item["Language Query"], item["Start"], item["End"])  # 去重关键
        if key not in unique_entries:
            unique_entries.add(key)
            filtered_data.append({
                "Video": item["Video"],
                "Language Query": item["Language Query"],
                "Start": item["Start"],
                "End": item["End"]
            })

    # 保存到 anno.json
    with open(output_file_name, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)

    print(f"去重后的数据已保存到 {output_file_name}")

# get_unique_query('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json',
#                  'generated_files/OVIS-training-filtered.json')
# get_unique_query('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json',
#                  'generated_files/OVIS-valid-filtered.json')

def merge_windows(windows):
    windows.sort()
    merged = []
    for start, end in windows:
        if not merged or merged[-1][1] < start - 1:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

def generate_jsonl(filtered_file, info_file, output_file, start_qid):
    # 读取 filtered.json
    with open(filtered_file, 'r', encoding='utf-8') as f:
        filtered_data = json.load(f)

    # 读取 info.json
    with open(info_file, 'r', encoding='utf-8') as f:
        info_data = json.load(f)

    # 创建一个映射，用于快速查找视频时长
    video_length_map = {item["file_name"]: item["length"] for item in info_data}

    # 处理数据
    jsonl_lines = []
    processed = {}

    for item in filtered_data:
        video = item["Video"]
        query = item["Language Query"]
        start = int(item["Start"])
        end = int(item["End"])

        # 获取视频时长
        duration = video_length_map.get(video, 0)
        vid = f"{video}_1_{duration}"

        key = (video, query)

        if key not in processed:
            processed[key] = {
                "qid": start_qid,
                "query": query,
                "duration": duration,
                "vid": vid,
                "relevant_windows": [],
                "relevant_clip_ids": [],
                "saliency_scores": []
            }
            start_qid += 1

        processed[key]["relevant_windows"].append([start, end])

    # 合并 relevant_windows 并重新计算 relevant_clip_ids
    for key, value in processed.items():
        value["relevant_windows"] = merge_windows(value["relevant_windows"])

        # 重新计算 relevant_clip_ids，按照 (1,2)->1, (3,4)->2, (5,6)->3 规则
        # 重新计算 relevant_clip_ids，按照 (0,2)->0, (2,4)->1, (4,6)->2 规则
        clip_ids = set()
        for start, end in value["relevant_windows"]:
            clip_start = (start - 1) // 2
            clip_end = end // 2  # 使 end 不包含在范围内
            if clip_start == clip_end:
                clip_ids.add(clip_start)
            else:
                clip_ids.update(range(clip_start, clip_end))

        value["relevant_clip_ids"] = sorted(clip_ids)
        value["saliency_scores"] = [[4, 4, 4]] * len(value["relevant_clip_ids"])

        jsonl_lines.append(json.dumps(value, ensure_ascii=False))

    # 保存为 JSONL 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(jsonl_lines) + "\n")

    print(f"JSONL 文件已生成: {output_file}")

generate_jsonl('generated_files/OVIS-training-filtered.json', '../OVIS/video_info_train.json',
               'ovis_train_release.jsonl', 1)
generate_jsonl('generated_files/OVIS-valid-filtered.json', '../OVIS/video_info_valid.json',
               'ovis_val_release.jsonl', 5095)