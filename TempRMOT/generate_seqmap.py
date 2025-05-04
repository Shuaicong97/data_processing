import os

def generate_seqmap(valid_json_folder, output_file):
    with open(output_file, "w") as f:
        if not os.path.exists(valid_json_folder):
            print(f"路径不存在: {valid_json_folder}")
        else:
            # 遍历一级子文件夹
            for folder_name in os.listdir(valid_json_folder):
                folder_path = os.path.join(valid_json_folder, folder_name)
                if not os.path.isdir(folder_path):
                    continue  # 忽略非文件夹

                json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
                for file_name in json_files:
                    name_without_extension = os.path.splitext(file_name)[0]
                    f.write(f"{folder_name}+{name_without_extension}\n")

    print(f"文件 {output_file} 已成功创建！")

valid_json_folder_ovis = '/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-ovis/expression/valid'
generate_seqmap(valid_json_folder_ovis, 'seqmap_ovis.txt')
# valid_json_folder_mot17 = '/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-mot17/expression/valid'
# generate_seqmap(valid_json_folder_mot17, 'seqmap_mot17.txt')
# valid_json_folder_mot20 = '/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-mot20/expression/valid'
# generate_seqmap(valid_json_folder_mot20, 'seqmap_mot20.txt')

def check_diff(file1, file2):
    # 读取两个文件
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        set1 = set(line.strip() for line in f1)
        set2 = set(line.strip() for line in f2)

    # 找出 ovis.txt 中有但 output_ovis.txt 中没有的项
    missing_in_output = set1 - set2
    # 也可以找出 output 中有但原始中没有的项（如果需要）
    extra_in_output = set2 - set1

    # 打印或保存结果
    print("以下项在 file1 中有，但在 file2 中缺失：")
    for item in sorted(missing_in_output):
        print(item)

# check_diff('seqmap_mot17.txt', '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/seqmap_mot17.txt')
