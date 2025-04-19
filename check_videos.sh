#!/bin/bash

# 设置目录路径
input_dir="/nfs/data3/shuaicong/refer-ovis/OVIS/valid"  # 包含子文件夹的目录
mp4_dir="/nfs/data3/shuaicong/videos_by_images/ovis"  # 存放 mp4 文件的目录

# 遍历父目录中的子文件夹
for folder in "$input_dir"/*/; do
  # 获取子文件夹名字
  folder_name=$(basename "$folder")

  # 查找与子文件夹名称对应的 mp4 文件的前缀
  # 假设 mp4 文件名格式为 001ca3cb_0.0_36.0.mp4，提取第一部分
  found=0
  for mp4_file in "$mp4_dir"/*.mp4; do
    # 提取 mp4 文件名的第一部分
    mp4_prefix=$(basename "$mp4_file" | cut -d'_' -f1)

    # 比较子文件夹名字与 mp4 文件的前缀
    if [ "$folder_name" == "$mp4_prefix" ]; then
      found=1
      break  # 找到匹配的 mp4 文件，跳出循环
    fi
  done

  # 如果没有找到匹配的 mp4 文件，则输出子文件夹的名字
  if [ $found -eq 0 ]; then
    echo "未找到匹配的 mp4 文件：$folder_name"
  fi
done
