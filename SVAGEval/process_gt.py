import json

training_path = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json'
valid_path = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json'

def add_qid(input_path, output_path, qid_counter):
    # 读取原始 JSON 文件
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 创建一个映射来存储已分配的 QID
    qid_map = {}

    # 遍历数据并分配 QID
    for item in data:
        key = (item["Video"], item["Language Query"])
        if key not in qid_map:
            qid_map[key] = str(qid_counter)
            qid_counter += 1
        item["QID"] = qid_map[key]

    # 写回原文件（备份原始数据建议另存为）
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# add_qid('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-training-doubled.json',
#         '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/MOT20-training-doubled_qid.json', 1)
# add_qid('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-valid-doubled.json',
#         '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/MOT20-valid-doubled_qid.json', 810)
add_qid('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-training-doubled.json',
        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/MOT17-training-doubled_qid.json', 1)
add_qid('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-valid-doubled.json',
        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/MOT17-valid-doubled_qid.json', 782)
add_qid('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json',
        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/OVIS-training-doubled_qid.json', 1)
add_qid('/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json',
        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/OVIS-valid-doubled_qid.json', 5095)