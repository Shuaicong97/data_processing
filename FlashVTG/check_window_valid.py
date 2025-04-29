import json

# 十分重要 避免无效的start,end值。
file_path = 'ovis_train_release.jsonl'  # 替换为你的jsonl文件路径
with open(file_path, 'r') as f:
    for line in f:
        obj = json.loads(line)
        qid = obj.get("qid")
        duration = obj.get("duration")
        relevant_windows = obj.get("relevant_windows", [])

        # 遍历 relevant_windows 中的所有数值，查找是否有 > duration 的情况
        if any(val > duration for window in relevant_windows for val in window):
            print(f"> qid: {qid}, duration: {duration}, relevant_windows: {relevant_windows}")
        # if any(val == duration for window in relevant_windows for val in window):
        #     print(f"== qid: {qid}, duration: {duration}, relevant_windows: {relevant_windows}")

