import json

def check_window_valid(file_path):
    # 十分重要 避免无效的start,end值。
    with open(file_path, 'r') as f:
        for line in f:
            obj = json.loads(line)
            qid = obj.get("qid")
            duration = obj.get("duration")
            relevant_windows = obj.get("relevant_windows", [])

            # 遍历 relevant_windows 中的所有数值，查找是否有 > duration 的情况
            if any(val > duration for window in relevant_windows for val in window):
                print(f"out of boundary qid: {qid}, duration: {duration}, relevant_windows: {relevant_windows}")
            # if any(val == duration for window in relevant_windows for val in window):
            #     print(f"til the last frame qid: {qid}, duration: {duration}, relevant_windows: {relevant_windows}")

check_window_valid('OVIS/ovis_train_release.jsonl')
check_window_valid('OVIS/ovis_val_release.jsonl')

check_window_valid('MOT17/mot17_train_release.jsonl')
check_window_valid('MOT17/mot17_val_release.jsonl')

check_window_valid('MOT20/mot20_train_release.jsonl')
check_window_valid('MOT20/mot20_val_release.jsonl')

