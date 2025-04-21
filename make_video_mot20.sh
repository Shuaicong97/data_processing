#!/bin/bash

# 设置输入目录（可通过参数传入，默认当前目录）
input_dir="/nfs/data3/shuaicong/refer-mot20/MOT20/training"
output_dir="/nfs/data3/shuaicong/videos_by_images/mot20_videos_V1"

# 确保输出目录存在
mkdir -p "$output_dir"

# 遍历所有子文件夹
for folder in "$input_dir"/*/; do
  # 获取当前子文件夹的名字
  folder_name=$(basename "$folder")
  img_folder="${folder}/img1"

  # 检查img1文件夹是否存在
  if [ ! -d "$img_folder" ]; then
    echo "⚠️ 跳过 $folder_name：未找到 img1 文件夹。"
    continue
  fi

  # 获取照片总数（*.jpg）
  count=$(ls "$img_folder"/*.jpg 2>/dev/null | wc -l)

  if [ "$count" -eq 0 ]; then
    echo "⚠️ 目录 $img_folder 中没有找到jpg图片。"
    continue  # 跳过当前文件夹
  fi

  last_frame=$(printf "%06d" "$count")
  added_frame_path=""

  # 判断奇偶决定使用多少帧
  if [ $((count % 2)) -eq 0 ]; then
    frames=$count
  else
    frames=$((count + 1))
    next_frame=$(printf "%06d" "$frames")
    cp "$img_folder/${last_frame}.jpg" "$img_folder/${next_frame}.jpg"
    added_frame_path="$img_folder/${next_frame}.jpg"
  fi

  # 生成输出文件名
  output_file="${folder_name}_0.0_${frames}.0.mp4"
  output_path="$output_dir/$output_file"

  echo "🖼️ 总照片数: $count"
  echo "🎞️ 使用帧数: $frames"
  echo "💾 输出文件: $output_path"

  # 调用 ffmpeg
  ffmpeg -framerate 1 -start_number 1 \
    -i "$img_folder/%06d.jpg" \
    -frames:v $frames -r 1 -pix_fmt yuv420p \
    "$output_path"

  # 删除临时添加的帧
  if [ -n "$added_frame_path" ]; then
    rm "$added_frame_path"
    echo "🧹 已删除添加的补帧: $added_frame_path"
  fi

done