import os




# 定义文件夹路径和输出文件名
folder_paths = [
    '../data/refer-mot17/expression/MOT17-01',
    '../data/refer-mot17/expression/MOT17-03',
    '../data/refer-mot17/expression/MOT17-06',
    '../data/refer-mot17/expression/MOT17-07',
    '../data/refer-mot17/expression/MOT17-08',
    '../data/refer-mot17/expression/MOT17-12',
    '../data/refer-mot17/expression/MOT17-14'
]
output_file = "seqmap_mot17.txt"

folder_paths = [
    '../data/refer-mot20/expression/MOT20-03',
    '../data/refer-mot20/expression/MOT20-05'
]
output_file = "seqmap_mot20.txt"



def generate_seqmap_for_ovis():
    folder_paths_ovis = '/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-ovis/expression/valid'
    output_file_ovis = "seqmap_ovis.txt"

    with open(output_file_ovis, "w") as f:
        if not os.path.exists(folder_paths_ovis):
            print(f"路径不存在: {folder_paths_ovis}")
        else:
            # 遍历一级子文件夹
            for folder_name in os.listdir(folder_paths_ovis):
                folder_path = os.path.join(folder_paths_ovis, folder_name)
                if not os.path.isdir(folder_path):
                    continue  # 忽略非文件夹

                json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
                for file_name in json_files:
                    name_without_extension = os.path.splitext(file_name)[0]
                    f.write(f"{folder_name}+{name_without_extension}\n")

    print(f"文件 {output_file_ovis} 已成功创建！")


def generate_seqmap_for_mot():
    # 遍历文件夹，获取所有json文件名
    try:
        with open(output_file, "w") as f:
            for folder_path in folder_paths:
                if not os.path.exists(folder_path):
                    print(f"路径不存在: {folder_path}")
                    continue

                folder_name = os.path.basename(folder_path)
                json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
                for file_name in json_files:
                    name_without_extension = os.path.splitext(file_name)[0]
                    f.write(f"{folder_name}+{name_without_extension}\n")
        print(f"文件 {output_file} 已成功创建！")
    except Exception as e:
        print(f"发生错误: {e}")


def save_json_filenames(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for folder_name in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder_name)
            if os.path.isdir(folder_path):  # 确保是文件夹
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.json'):
                        name_without_extension = os.path.splitext(file_name)[0]
                        entry = f"{folder_name}+{name_without_extension}\n"
                        f.write(entry)

# 使用示例
# root_directory = "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/refer-ovis/expression/valid"
# output_file = "seqmap_ovis.txt"
# save_json_filenames(folder_paths, output_file)
generate_seqmap_for_ovis()

# 读取两个文件
with open('seqmap_ovis.txt', 'r') as f1, open('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/seqmap_ovis.txt', 'r') as f2:
    set1 = set(line.strip() for line in f1)  # 原始 ovis.txt
    set2 = set(line.strip() for line in f2)  # 新生成 output_ovis.txt

# 找出 ovis.txt 中有但 output_ovis.txt 中没有的项
missing_in_output = set1 - set2
# 也可以找出 output 中有但原始中没有的项（如果需要）
extra_in_output = set2 - set1

# 打印或保存结果
print("以下项在 seqmap_ovis.txt 中有，但在 output_ovis.txt 中缺失：")
for item in sorted(missing_in_output):
    print(item)

# 可选：写入文件
with open('missing_items.txt', 'w') as f:
    for item in sorted(missing_in_output):
        f.write(item + '\n')
