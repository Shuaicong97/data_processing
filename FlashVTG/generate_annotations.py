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

        # 获取视频时长。假如是奇数帧，则最后一帧显示2s。Start-End时间间隔保持不变。
        duration = video_length_map.get(video, 0)
        if duration % 2 != 0:
            duration += 1
        vid = f"{video}_0.0_{duration}.0"

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

        # 1) [20,25] => [19,25](in video form)
        # valid set 164 未从1开始 171-334
        if video == "cfff47c3":
            start = start - 170 - 1
            end = end - 170
        # train set 342 不连续 1-70, 72, 89-359
        elif video == "86a88668":
            if start <= 70:
                start -= 1

            if start == 72:
                start = 71 - 1
            if end == 72:
                end = 71

            if start >= 89:
                start = start - 17 - 1
            if end >= 89:
                end = end - 17
        # valid set 231 不连续 1-5, 8, 12-236
        elif video == "af48b2f9":
            if start <= 5:
                start -= 1

            if start == 8:
                start = 6 - 1
            if end == 8:
                end = 6

            if start >= 12:
                start = start - 5 - 1
            if end >= 12:
                end = end - 5
        # train set 84 不连续 1-13, 15-85
        elif video == "2fb5a55b":
            if start <= 13:
                start -= 1

            if start >= 15:
                start = start - 1 - 1
            if end >= 15:
                end = end - 1
        else:
            start -= 1

        # 2) 保持奇数的GT不变 [19,25]
        # if start % 2 != 0:
        #     start += 1
        # if end % 2 != 0:
        #     end -= 1

        processed[key]["relevant_windows"].append([start, end])

    keys_to_remove = []
    removed_count = 0

    # print(processed)
    # 合并 relevant_windows 并重新计算 relevant_clip_ids
    for key, value in processed.items():
        previous_windows = value["relevant_windows"]
        value["relevant_windows"] = merge_windows(value["relevant_windows"])
        merged_windows = value["relevant_windows"]

        # if previous_windows != merged_windows:
        #     print(f'{key}\tprevious_windows: {previous_windows}')
        #     print(f'merged_windows: {merged_windows}')

        # 可能的windows例子：[[26, 27]], [[12, 15], [17, 18]] 其中不包括end值，即对于[26, 27]，object只出现在26秒
        for window in merged_windows:
            if window[1] - window[0] == 1:
                print(f"只出现1s的query: {key}\t{merged_windows}")

    for key, value in processed.items():
        jsonl_lines.append(json.dumps(value, ensure_ascii=False))

    # 保存为 JSONL 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(jsonl_lines) + "\n")

    print(f"JSONL 文件已生成: {output_file}")

generate_jsonl('generated_files/OVIS-training-filtered.json', '../OVIS/video_info_train.json',
               'ovis_train_release_no_ids.jsonl', 1)
generate_jsonl('generated_files/OVIS-valid-filtered.json', '../OVIS/video_info_valid.json',
               'ovis_val_release_no_ids.jsonl', 5095)

def generate_clip_ids_and_scores(data):
    relevant_clip_ids = []
    saliency_scores = []

    for window in data["relevant_windows"]:
        start, end = window
        # 计算clip_start和clip_end 可简化4种情况
        # case 1 [0, 16] => [0,1,2,3,4,5,6,7]
        # if start % 2 == 0 and end % 2 == 0:
        #     clip_start = start // 2
        #     clip_end = end // 2 - 1
        # # case 2 [1, 13] => [0,1,2,3,4,5,6]
        # if start % 2 != 0 and end % 2 != 0:
        #     clip_start = start // 2
        #     clip_end = end // 2
        # # case 3 [1, 4] => [0,1]
        # if start % 2 != 0 and end % 2 == 0:
        #     clip_start = start // 2
        #     clip_end = end // 2 - 1
        # # case 4 [2, 7] => [1,2,3]
        # if start % 2 == 0 and end % 2 != 0:
        #     clip_start = start // 2
        #     clip_end = end // 2
        clip_start = start // 2
        clip_end = (end - 1) // 2

        # 生成relevant_clip_ids
        clip_ids = list(range(clip_start, clip_end + 1))
        relevant_clip_ids.extend(clip_ids)

        # 生成saliency_scores，数量与clip_ids相同，每个为[4, 4, 4]
        saliency_scores.extend([[4, 4, 4]] * len(clip_ids))

    data["relevant_clip_ids"] = relevant_clip_ids
    data["saliency_scores"] = saliency_scores

    return data

def process_jsonl(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    processed_data = []
    for line in lines:
        data = json.loads(line)
        data = generate_clip_ids_and_scores(data)
        processed_data.append(data)

    count = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in processed_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            if len(item["relevant_clip_ids"]) == 1:
                count += 1
                print(f"Length 1 found for qid {item['qid']} with relevant_clip_ids: {item['relevant_clip_ids']}")
    print(f"总共有 {count} 个只有一个clip id, 说明query持续了1帧或者2帧")

    print(f"JSONL 文件已生成: {output_file}")

    return processed_data

processed_data = process_jsonl('ovis_train_release_no_ids.jsonl', 'ovis_train_release_V1.jsonl')
processed_data = process_jsonl('ovis_val_release_no_ids.jsonl', 'ovis_val_release_V1.jsonl')
