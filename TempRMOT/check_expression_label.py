import os
import json


# 查看json文件的label里的key（帧）是否递增
def check_expression(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        label_keys = list(data.get("label", {}).keys())
                        key_ints = list(map(int, label_keys))
                        sorted_keys = sorted(key_ints)

                        # 找出未递增（顺序不对的）帧号
                        unordered = [orig for orig, expected in zip(key_ints, sorted_keys) if orig != expected]
                        if unordered:
                            print(f"\n❌ 文件未递增排序: {file_path}")
                            print(f"未递增帧号: {unordered}")
                except Exception as e:
                    print(f"无法处理文件 {file_path}: {e}")
    print('没有未递增的帧')


check_expression('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-ovis-v2/expression/training')
check_expression('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-ovis-v2/expression/valid')
check_expression('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-mot17-v2/expression/training')
check_expression('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-mot17-v2/expression/valid')
check_expression('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-mot20-v2/expression/training')
check_expression('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-mot20-v2/expression/valid')