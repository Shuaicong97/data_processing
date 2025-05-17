import os
import json
import shutil

# run generate_unique_queries.py first
def generate_labels_with_ids(gt_dir, info_json_path, output_dir):
    # 加载 b.json 数据
    with open(info_json_path, "r") as f:
        video_length_info = json.load(f)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 遍历目录a中的所有子文件夹
    for folder_name in os.listdir(gt_dir):
        folder_path = os.path.join(gt_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # 在 b.json 中匹配 file_name
        matched_entry = next((entry for entry in video_length_info if entry["file_name"] == folder_name), None)
        if not matched_entry:
            print(f"文件夹 {folder_name} 在 b.json 中未匹配，跳过。")
            continue

        # 获取 width 和 height
        width = matched_entry["width"]
        height = matched_entry["height"]

        # 读取 gt.txt 文件
        gt_file_path = os.path.join(folder_path, "gt.txt")
        if not os.path.isfile(gt_file_path):
            print(f"{gt_file_path} 文件不存在，跳过。")
            continue

        # 创建对应的输出子目录
        output_subdir = os.path.join(output_dir, folder_name)
        os.makedirs(output_subdir, exist_ok=True)

        # 处理 gt.txt 文件
        frame_data = {}
        with open(gt_file_path, "r") as gt_file:
            for line in gt_file:
                # 提取数据行的前六个字段
                frame_id, obj_id, x, y, w, h, *_ = map(float, line.strip().split(","))
                frame_id = int(frame_id)
                obj_id = int(obj_id)

                # 归一化并格式化数据
                x_normalized = round(x / width, 6)
                y_normalized = round(y / height, 6)
                w_normalized = round(w / width, 6)
                h_normalized = round(h / height, 6)

                # 构建输出数据行
                formatted_line = f"0 {obj_id} {x_normalized:.6f} {y_normalized:.6f} {w_normalized:.6f} {h_normalized:.6f}\n"

                # 将数据加入对应 frame_id 的列表
                if frame_id not in frame_data:
                    frame_data[frame_id] = []
                frame_data[frame_id].append(formatted_line)

        # 写入输出文件
        for frame_id, lines in frame_data.items():
            output_file_path = os.path.join(output_subdir, f"{frame_id:06}.txt")
            with open(output_file_path, "w") as output_file:
                output_file.writelines(lines)

        print(f"处理完成：{folder_name}")

    print(f"所有文件处理完成，结果保存在 {output_dir}。")

def clear_folder(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"路径 {folder_path} 不存在")
        return

    # 遍历文件夹中的所有内容
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 如果是文件夹，递归删除
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        # 如果是文件，直接删除
        elif os.path.isfile(file_path):
            os.remove(file_path)

    print(f"已清空文件夹：{folder_path}")

def generate_original_expression(input_f, output):
    with open(input_f, "r", encoding="utf-8") as f:
        data = json.load(f)

    label_dict = {}

    # 遍历数据并生成文件
    for entry in data:
        video_name = entry["Video"]
        language_query = entry["Language Query"]
        start = int(entry["Start"])
        end = int(entry["End"])
        ids = int(entry["IDs"])

        # 创建视频文件夹
        video_path = os.path.join(output, video_name)
        os.makedirs(video_path, exist_ok=True)

        # 生成文件名（小写并用-连接）
        file_name = language_query.lower().replace(" ", "-") + ".json"
        file_path = os.path.join(video_path, file_name)

        # 生成 frame_id 对应的 object_ids 映射
        if file_path not in label_dict:
            label_dict[file_path] = {}

        for frame in range(start, end + 1):
            frame_str = str(frame)
            if frame_str not in label_dict[file_path]:
                label_dict[file_path][frame_str] = []
            if ids not in label_dict[file_path][frame_str]:
                label_dict[file_path][frame_str].append(ids)

    for file_path, labels in label_dict.items():
        sorted_labels = dict(sorted(labels.items(), key=lambda x: int(x[0])))

        # 生成 JSON 内容
        json_content = {
            "label": sorted_labels,
            "ignore": {},
            "video_name": os.path.basename(os.path.dirname(file_path)),
            "sentence": " ".join(os.path.splitext(os.path.basename(file_path))[0].split("-")).capitalize()
        }

        # 写入 JSON 文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_content, f, ensure_ascii=False, indent=None, separators=(', ', ': '))

    print("所有 JSON 文件已生成！")

def generate_rephrased_expression(input_f, output):
    with open(input_f, "r", encoding="utf-8") as f:
        data = json.load(f)

    label_dict = {}
    # 遍历数据并生成文件
    for entry in data:
        video_name = entry["Video"]
        language_query = entry["Language Query"]
        start = int(entry["Start"])
        end = int(entry["End"])
        ids = int(entry["IDs"])
        raw_sentence = entry["Raw sentence"]

        # 创建视频文件夹
        video_path = os.path.join(output, video_name)
        os.makedirs(video_path, exist_ok=True)

        # 生成文件名（小写并用-连接）
        file_name = language_query.lower().replace(" ", "-") + ".json"
        file_path = os.path.join(video_path, file_name)

        # 生成 frame_id 对应的 object_ids 映射
        if file_path not in label_dict:
            label_dict[file_path] = {
                "labels": {},  # 存储 frame_id -> object_ids 的映射
                "raw_sentence": raw_sentence  # 存储对应的 raw_sentence
            }

        for frame in range(start, end + 1):
            frame_str = str(frame)
            if frame_str not in label_dict[file_path]["labels"]:
                label_dict[file_path]["labels"][frame_str] = []
            if ids not in label_dict[file_path]["labels"][frame_str]:
                label_dict[file_path]["labels"][frame_str].append(ids)

    for file_path, file_data in label_dict.items():
        labels = file_data["labels"]
        sorted_labels = dict(sorted(labels.items(), key=lambda x: int(x[0])))
        raw_sentence = file_data["raw_sentence"]
        # 生成 JSON 内容
        json_content = {
            "label": sorted_labels,
            "ignore": {},
            "video_name": os.path.basename(os.path.dirname(file_path)),
            "sentence": " ".join(os.path.splitext(os.path.basename(file_path))[0].split("-")).capitalize(),
            "raw_sentence": raw_sentence
        }

        # 写入 JSON 文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_content, f, ensure_ascii=False, indent=None, separators=(', ', ': '))

    print("Rephrased内容生成！")

def process_ovis():
    # 我们使用train_frame_in_image_name文件夹里的gt，保留了不连续的帧
    gt_train_dir = "/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/OVIS_GTs/train_frame_in_image_name"
    info_train_path = "/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/video_info_train.json"
    output_dir_train = "data/refer-ovis-v2/OVIS/labels_with_ids"
    generate_labels_with_ids(gt_train_dir, info_train_path, output_dir_train)

    gt_valid_dir = "/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/OVIS_GTs/val"
    info_valid_path = "/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/video_info_valid.json"
    output_dir_valid = "data/refer-ovis-v2/OVIS/labels_with_ids/valid"
    generate_labels_with_ids(gt_valid_dir, info_valid_path, output_dir_valid)

    input_ovis_training_file = "../Original/OVIS-training.json"
    output_ovis_training_path = "data/refer-ovis-v2/expression/training"
    input_ovis_valid_file = "../Original/OVIS-valid.json"
    output_ovis_valid_path = "data/refer-ovis-v2/expression/valid"

    clear_folder(output_ovis_training_path)
    clear_folder(output_ovis_valid_path)

    generate_original_expression(input_ovis_training_file, output_ovis_training_path)
    generate_original_expression(input_ovis_valid_file, output_ovis_valid_path)

    generate_rephrased_expression('unique_objects_ovis-training.json', output_ovis_training_path)
    generate_rephrased_expression('unique_objects_ovis-valid.json', output_ovis_valid_path)

process_ovis()

def process_mot17():
    gt_train_dir = "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/MOT17_GTs/train"
    gt_val_dir = "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/MOT17_GTs/val"
    info_path = "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/video_mot.json"
    output_dir_train = "data/refer-mot17-v2/MOT17/labels_with_ids"
    output_dir_valid = "data/refer-mot17-v2/MOT17/labels_with_ids/valid"
    generate_labels_with_ids(gt_train_dir, info_path, output_dir_train)
    generate_labels_with_ids(gt_val_dir, info_path, output_dir_valid)

    input_mot17_training_file = "../Original/MOT17-training.json"
    output_mot17_training_path = "data/refer-mot17-v2/expression/training"
    input_mot17_valid_file = "../Original/MOT17-valid.json"
    output_mot17_valid_path = "data/refer-mot17-v2/expression/valid"

    clear_folder(output_mot17_training_path)
    clear_folder(output_mot17_valid_path)

    generate_original_expression(input_mot17_training_file, output_mot17_training_path)
    generate_original_expression(input_mot17_valid_file, output_mot17_valid_path)

    generate_rephrased_expression('unique_objects_mot17-training.json', output_mot17_training_path)
    generate_rephrased_expression('unique_objects_mot17-valid.json', output_mot17_valid_path)

process_mot17()

def process_mot20():
    gt_train_dir = "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/MOT20_GTs/train"
    gt_val_dir = "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/MOT20_GTs/val"
    info_path = "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/video_mot.json"
    output_dir_train = "data/refer-mot20-v2/MOT20/labels_with_ids"
    output_dir_valid = "data/refer-mot20-v2/MOT20/labels_with_ids/valid"
    generate_labels_with_ids(gt_train_dir, info_path, output_dir_train)
    generate_labels_with_ids(gt_val_dir, info_path, output_dir_valid)

    input_mot20_training_file = "../Original/MOT20-training.json"
    output_mot20_training_path = "data/refer-mot20-v2/expression/training"
    input_mot20_valid_file = "../Original/MOT20-valid.json"
    output_mot20_valid_path = "data/refer-mot20-v2/expression/valid"

    clear_folder(output_mot20_training_path)
    clear_folder(output_mot20_valid_path)

    generate_original_expression(input_mot20_training_file, output_mot20_training_path)
    generate_original_expression(input_mot20_valid_file, output_mot20_valid_path)

    generate_rephrased_expression('unique_objects_mot20-training.json', output_mot20_training_path)
    generate_rephrased_expression('unique_objects_mot20-valid.json', output_mot20_valid_path)

# 生成后手动将expression/valid/MOT20-03（/MOT20-05）分成几个子集，以分块运行inference，可获得阶段性的部分结果。
process_mot20()
