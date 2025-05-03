import json


def compare_two_json_files(json_file1, json_file2):
    # 加载两个 JSON 文件
    with open(json_file1, 'r', encoding='utf-8') as f:
        a_data = json.load(f)
    with open(json_file2, 'r', encoding='utf-8') as f:
        b_data = json.load(f)

    key_fields = ["Video", "Language Query", "Type", "IDs", "Start", "End", "Revision"]

    # 把 A&B 中的元素转为集合（字符串形式）方便比较
    a_set = {
        json.dumps({k: obj.get(k, "") for k in key_fields}, sort_keys=True)
        for obj in a_data
    }
    b_set = {
        json.dumps({k: obj.get(k, "") for k in key_fields}, sort_keys=True)
        for obj in b_data
    }

    # 找出 A 中存在但 B 中不存在的项 或者 B 中存在但 A 中不存在的项
    only_in_a = [
        item for item in a_data
        if json.dumps({k: item.get(k, "") for k in key_fields}, sort_keys=True) not in b_set
    ]
    only_in_b = [
        item for item in b_data
        if json.dumps({k: item.get(k, "") for k in key_fields}, sort_keys=True) not in a_set
    ]


    # 输出结果或写入文件
    with open('only_in_a_ovis_training.json', 'w', encoding='utf-8') as f:
        json.dump(only_in_a, f, indent=4, ensure_ascii=False)

    print(f"找到 {len(only_in_a)} 个 A 中独有的项")

    # 输出结果或写入文件
    with open('only_in_b_ovis_training.json', 'w', encoding='utf-8') as f:
        json.dump(only_in_b, f, indent=4, ensure_ascii=False)

    print(f"找到 {len(only_in_b)} 个 B 中独有的项")

# compare_two_json_files('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/rephrased_annotations/OVIS-valid-doubled.json',
#                        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json')
compare_two_json_files('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/rephrased_annotations/OVIS-training-doubled.json',
                       '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json')
# compare_two_json_files('/Users/shuaicongwu/PycharmProjects/data_processing/Original/OVIS-training.json',
#                        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json')
# compare_two_json_files('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-training.json',
#                        '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.json')
# compare_two_json_files('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-training.json',
#                        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-training-doubled.json')
# compare_two_json_files('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-valid.json',
#                        '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.json')
# compare_two_json_files('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-valid.json',
#                        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-valid-doubled.json')
# compare_two_json_files('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT20-training.json',
#                        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-training-doubled.json')
# compare_two_json_files('/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT20-valid.json',
#                        '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-valid-doubled.json')


# 比较两个文件的内容，并打印不一致的行
def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # 去除换行符并转换为集合
    set1 = set(line.strip() for line in lines1)
    set2 = set(line.strip() for line in lines2)

    only_in_file1 = set1 - set2
    only_in_file2 = set2 - set1

    if only_in_file1:
        print("仅存在于 file1.txt 中的内容:")
        for line in sorted(only_in_file1):
            print(line)

    if only_in_file2:
        print("\n仅存在于 file2.txt 中的内容:")
        for line in sorted(only_in_file2):
            print(line)

    if not only_in_file1 and not only_in_file2:
        print("两个文件内容完全一致。")

# # 使用方法
# compare_files('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/temprmot/refer-ovis.train',
# '/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/refer-ovis.train')
# compare_files('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/seqmap_ovis.txt',
# '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/seqmap_ovis.txt')
