import json

# 读取 JSONL 文件并提取 query
video_candidates = set()
with open('generated_files/OVIS_train_release.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line.strip())  # 解析 JSON 行
        if "vid" in data:
            video_candidates.add(data["vid"])

video_candidates = list(video_candidates)

# 打印结果
print(video_candidates)

with open('OVIS_train_videos.json', 'w', encoding='utf-8') as f:
    json.dump(video_candidates, f, ensure_ascii=False, indent=4)

