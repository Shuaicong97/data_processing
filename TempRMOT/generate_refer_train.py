import os

# 定义目标目录 排除里面的valid
directory_A = '/Users/shuaicongwu/PycharmProjects/data_processing/TempRMOT/data/refer-ovis/OVIS/labels_with_ids'

# 用于保存文件路径的列表
txt_files = []

# 遍历目录及其子目录
for root, dirs, files in os.walk(directory_A):
    dirs[:] = [d for d in dirs if d != 'valid']

    for file in files:
        if file.endswith('.txt'):  # 判断是否是 txt 文件
            # 获取从 OVIS 开始的路径部分
            relative_path = os.path.relpath(root, directory_A)
            full_path = os.path.join('OVIS', relative_path, file)
            txt_files.append(full_path)

txt_files.sort(key=lambda x: (x.split('/')[1], int(x.split('/')[-1].split('.')[0])))

# 将所有文件路径写入 refer-ovis.train 文件
with open('refer-ovis.train', 'w') as f:
    for txt_file in txt_files:
        adjusted_path = txt_file.replace('OVIS/', 'OVIS/training/').replace('.txt', '.jpg')
        f.write(adjusted_path + '\n')

print("所有txt文件路径已保存至 'refer-ovis.train' 文件中。")

