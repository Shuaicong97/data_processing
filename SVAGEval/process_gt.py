import json

training_path = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json'
valid_path = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json'

# 读取原始 JSON 文件
with open(valid_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建一个映射来存储已分配的 QID
qid_map = {}
qid_counter = 5095

# 遍历数据并分配 QID
for item in data:
    key = (item["Video"], item["Language Query"])
    if key not in qid_map:
        qid_map[key] = str(qid_counter)
        qid_counter += 1
    item["QID"] = qid_map[key]

# 写回原文件（备份原始数据建议另存为）
with open(valid_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
