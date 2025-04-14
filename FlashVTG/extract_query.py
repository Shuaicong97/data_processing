import json

# # 读取 JSONL 文件并提取 query
# video_candidates = set()
# with open('generated_files/OVIS_train_release.jsonl', 'r', encoding='utf-8') as f:
#     for line in f:
#         data = json.loads(line.strip())  # 解析 JSON 行
#         if "vid" in data:
#             video_candidates.add(data["vid"])
#
# video_candidates = list(video_candidates)
#
# # 打印结果
# print(video_candidates)
#
# with open('OVIS_train_videos.json', 'w', encoding='utf-8') as f:
#     json.dump(video_candidates, f, ensure_ascii=False, indent=4)

import json

file_path = 'ovis_val_release_V2.jsonl'  # 替换为你的jsonl文件路径

with open(file_path, 'r') as f:
    for line in f:
        obj = json.loads(line)
        qid = obj.get("qid")
        duration = obj.get("duration")
        relevant_windows = obj.get("relevant_windows", [])

        # 遍历 relevant_windows 中的所有数值，查找是否有 >= duration 的情况
        if any(val > duration for window in relevant_windows for val in window):
            print(f"> qid: {qid}, duration: {duration}, relevant_windows: {relevant_windows}")
        if any(val == duration for window in relevant_windows for val in window):
            print(f"== qid: {qid}, duration: {duration}, relevant_windows: {relevant_windows}")

