import json
import csv

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 将每个对象转为不可变的 tuple 形式，用于集合比较
def obj_to_tuple(obj):
    return (
        obj.get("Video", ""),
        # obj.get("Language Query", ""),
        str(obj.get("Start", "")),
        str(obj.get("End", ""))
    )

def load_csv_tuples(file_path):
    results = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["Video"], str(row["Start"]), str(row["End"]))
            results.add(key)
    return results

# 主比较函数
def compare_json_files(file_a, csv_file_b, csv_file_c):
    data_a = load_json(file_a)
    set_b = load_csv_tuples(csv_file_b)
    set_c = load_csv_tuples(csv_file_c)

    # set_a = set(obj_to_tuple(item) for item in data_a)
    # set_b = set(obj_to_tuple(item) for item in data_b)
    # set_c = set(obj_to_tuple(item) for item in data_c)

    # only_in_a = set_a - set_b
    # only_in_b = set_b - set_a

    # print("\n=== 在 filtered 中但不在 filtered_1 中的对象 ===")
    # for item in only_in_a:
    #     print(item)
    #
    # print("\n=== 在 filtered_1 中但不在 filtered 中的对象 ===")
    # for item in only_in_b:
    #     print(item)
    print("\n=== 以下对象在 data_a 中，但不在 data_b 和 data_c 中 ===")
    for obj in data_a:
        key = (
            obj.get("Video", ""),
            str(obj.get("Start", "")),
            str(obj.get("End", ""))
        )
        if key not in set_b and key not in set_c:
            print(obj)


# 示例用法（替换成你自己的路径）
print('\n')
compare_json_files("../Rephrased data/OVIS-valid-doubled.json",
                   "../OVIS/Sheet/Grounded Tracking Annotations - OVIS-Test(Ashiq).csv",
                   "../OVIS/Sheet/Grounded Tracking Annotations - OVIS-Test(Seenat).csv")
