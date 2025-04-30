import json


# 假设 A.json 和 B.json 分别是文件A和B的文件名
def get_unique_objects(file_a, file_b, output_file):
    key_fields = ["Video", "Language Query", "Type", "IDs", "Start", "End", "Revision"]

    # 读取文件A和B的内容
    with open(file_a, 'r') as fa:
        data_a = json.load(fa)

    with open(file_b, 'r') as fb:
        data_b = json.load(fb)

    # 将文件A的对象转化为集合以便快速比较
    set_a = {
        json.dumps({k: obj.get(k, "") for k in key_fields}, sort_keys=True)
        for obj in data_a
    }

    # 遍历B中的对象，获取不在A中的对象
    unique_objects = []
    for obj in data_b:
        obj_key = json.dumps({k: obj.get(k, "") for k in key_fields}, sort_keys=True)
        if obj_key not in set_a:
            # 提取需要的字段
            unique_objects.append({
                "Video": obj.get("Video"),
                "Language Query": obj.get("Language Query"),
                "IDs": obj.get("IDs"),
                "Start": obj.get("Start"),
                "End": obj.get("End"),
                "Raw sentence": ""
            })

    # 将结果保存到一个新的JSON文件
    with open(output_file, 'w') as fo:
        json.dump(unique_objects, fo, indent=4)


original_ovis_training = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/OVIS-training.json'
original_ovis_valid = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/OVIS-valid.json'
doubled_ovis_training = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json'
doubled_ovis_valid = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json'
unique_objects_ovis_training = 'unique_objects_ovis-training.json'
unique_objects_ovis_valid = 'unique_objects_ovis-valid.json'

# get_unique_objects(original_ovis_training, doubled_ovis_training, unique_objects_ovis_training)
# get_unique_objects(original_ovis_valid, doubled_ovis_valid, unique_objects_ovis_valid)

original_mot17_training = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-training.json'
original_mot17_valid = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-valid.json'
doubled_mot17_training = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-training-doubled.json'
doubled_mot17_valid = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-valid-doubled.json'
unique_objects_mot17_training = 'unique_objects_mot17-training.json'
unique_objects_mot17_valid = 'unique_objects_mot17-valid.json'

get_unique_objects(original_mot17_training, doubled_mot17_training, unique_objects_mot17_training)
get_unique_objects(original_mot17_valid, doubled_mot17_valid, unique_objects_mot17_valid)

original_mot20_training = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT20-training.json'
original_mot20_valid = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT20-valid.json'
doubled_mot20_training = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-training-doubled.json'
doubled_mot20_valid = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-valid-doubled.json'
unique_objects_mot20_training = 'unique_objects_mot20-training.json'
unique_objects_mot20_valid = 'unique_objects_mot20-valid.json'

get_unique_objects(original_mot20_training, doubled_mot20_training, unique_objects_mot20_training)
get_unique_objects(original_mot20_valid, doubled_mot20_valid, unique_objects_mot20_valid)

def add_raw_sentences(unique_file, file_a):
    # 读取unique.json和A.json的内容
    with open(unique_file, 'r') as fu:
        unique_data = json.load(fu)

    with open(file_a, 'r') as fa:
        data_a = json.load(fa)

    # 遍历unique.json中的对象，根据条件在A.json中查找匹配项
    for unique_obj in unique_data:
        for a_obj in data_a:
            if (unique_obj["Video"] == a_obj["Video"] and
                unique_obj["IDs"] == a_obj["IDs"] and
                unique_obj["Start"] == a_obj["Start"] and
                unique_obj["End"] == a_obj["End"]):
                # 将A.json中的Language Query赋值给unique.json的Raw sentence
                unique_obj["Raw sentence"] = a_obj["Language Query"]

    # 将更新后的unique.json保存回去
    with open(unique_file, 'w') as fu:
        json.dump(unique_data, fu, indent=4)

# add_raw_sentences(unique_objects_ovis_training, original_ovis_training)
# add_raw_sentences(unique_objects_ovis_valid, original_ovis_valid)
add_raw_sentences(unique_objects_mot17_training, original_mot17_training)
add_raw_sentences(unique_objects_mot17_valid, original_mot17_valid)
add_raw_sentences(unique_objects_mot20_training, original_mot20_training)
add_raw_sentences(unique_objects_mot20_valid, original_mot20_valid)
