import os

def generate_refer_train(input_folder, output_file, type):
    # 用于保存文件路径的列表
    txt_files = []

    # 遍历目录及其子目录
    for root, dirs, files in os.walk(input_folder):
        # 定义目标目录 排除里面的valid
        dirs[:] = [d for d in dirs if d != 'valid']

        for file in files:
            if file.endswith('.txt'):  # 判断是否是 txt 文件
                # 获取从 OVIS 开始的路径部分
                relative_path = os.path.relpath(root, input_folder)
                full_path = os.path.join(type, relative_path, file)
                txt_files.append(full_path)

    txt_files.sort(key=lambda x: (x.split('/')[1], int(x.split('/')[-1].split('.')[0])))

    # 将所有文件路径写入 refer-x.train 文件
    with open(output_file, 'w') as f:
        for txt_file in txt_files:
            adjusted_path = txt_file.replace(f'{type}/', f'{type}/training/').replace('.txt', '.jpg')
            f.write(adjusted_path + '\n')

    print(f"所有txt文件路径已保存至 'refer-{type.lower()}.train' 文件中。")

generate_refer_train('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-ovis/OVIS/labels_with_ids',
                     'refer-ovis.train', 'OVIS')
# generate_refer_train('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-mot17/MOT17/labels_with_ids',
#                      'refer-mot17.train', 'MOT17')
# generate_refer_train('/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-mot20/MOT20/labels_with_ids',
#                      'refer-mot20.train', 'MOT20')
