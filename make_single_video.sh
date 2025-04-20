#!/bin/bash

# 特别的是 cfff47c3 里的图片从000171.jpg开始
input_dir="/nfs/data3/shuaicong/refer-ovis/OVIS/valid/cfff47c3"
output_dir="/nfs/data3/shuaicong/videos_by_images/ovis_V1"

# 确保输出目录存在
mkdir -p "$output_dir"

# 获取当前子文件夹的名字
folder_name=$(basename "input_dir")

jpg_files=($(find "$input_dir" -type f \( -iname "*.jpg" \)))

# 获取照片总数（*.jpg）
count=${#jpg_files[@]}

if [ "$count" -eq 0 ]; then
  echo "⚠️ 目录 $input_dir 中没有找到jpg图片。"
  exit 1
fi

last_frame=$(printf "%06d" "$count")
added_frame_path=""

# 判断奇偶决定使用多少帧
if [ $((count % 2)) -eq 0 ]; then
  frames=$count
else
  frames=$((count + 1))
  next_frame=$(printf "%06d" "$frames")
  cp "$folder/${last_frame}.jpg" "$folder/${next_frame}.jpg"
  added_frame_path="$folder/${next_frame}.jpg"
fi

# 生成输出文件名
output_file="cfff47c3_0.0_${frames}.0.mp4"
output_path="$output_dir/$output_file"

echo "🖼️ 总照片数: $count"
echo "🎞️ 使用帧数: $frames"
echo "💾 输出文件: $output_path"

# 调用 ffmpeg
ffmpeg -framerate 1 -start_number 171 \
  -i "$input_dir/%06d.jpg" \
  -frames:v $frames -r 1 -pix_fmt yuv420p \
  "$output_path"

# 删除临时添加的帧
if [ -n "$added_frame_path" ]; then
  rm "$added_frame_path"
  echo "🧹 已删除添加的补帧: $added_frame_path"
fi