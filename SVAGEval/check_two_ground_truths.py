import json
from collections import defaultdict

# 加载两个文件
with open('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json', 'r') as f1:
    data1 = json.load(f1)

with open('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/rephrased_annotations/OVIS-valid-doubled.json', 'r') as f2:
    data2 = json.load(f2)

# 构造键值索引映射：以 (Video, Language Query, IDs) 为键
def index_by_key(data):
    return {
        (item['Video'], item['Language Query'], item['IDs']): item
        for item in data
    }

index1 = index_by_key(data1)
index2 = index_by_key(data2)

# 查找键相同但 Start 或 End 不同的项
differences = []
for key in index1:
    if key in index2:
        item1 = index1[key]
        item2 = index2[key]
        if item1['Start'] != item2['Start'] or item1['End'] != item2['End']:
            differences.append({
                "Key": key,
                "File1": {"Start": item1['Start'], "End": item1['End']},
                "File2": {"Start": item2['Start'], "End": item2['End']}
            })

# 打印结果
for diff in differences:
    print(json.dumps(diff, indent=2))


with open('/Users/shuaicongwu/PycharmProjects/data_processing/SVAGEval/prediction_processing/ovis_valid_ground_truth.json', 'r') as f:
    data = json.load(f)

# 用于记录所有的 track_id 出现次数
track_id_count = defaultdict(int)

# 遍历所有的 track
for query in data.get("queries", []):
    query_text = query["query"]
    video = query["video_name"]
    for track in query.get("tracks", []):
        track_id = track["track_id"]
        temporal = track.get("temporal")
        if len(temporal) != 1:
            print(f'video {video} for query {query_text} and track {track_id} has {len(temporal)} temporal entries: {temporal}')

# 找出重复的 track_id
# duplicates = {track_id: count for track_id, count in track_id_count.items() if count > 1}
#
# # 输出结果
# if duplicates:
#     print("存在重复的 track_id：")
#     for track_id, count in duplicates.items():
#         print(f"track_id {track_id} 出现了 {count} 次")
# else:
#     print("所有 track_id 都是唯一的")
