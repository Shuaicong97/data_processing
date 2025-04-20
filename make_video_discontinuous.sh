#!/bin/bash

# "86a88668" "af48b2f9" "2fb5a55b" 这三个里面有非连续的图片
paths=(
  "/nfs/data3/shuaicong/refer-ovis/OVIS/training/86a88668"
  "/nfs/data3/shuaicong/refer-ovis/OVIS/training/2fb5a55b"
  "/nfs/data3/shuaicong/refer-ovis/OVIS/valid/af48b2f9"
)
video_name="af48b2f9"
input_dir="/nfs/data3/shuaicong/refer-ovis/OVIS/valid/"
full_path="${input_dir}${video_name}"
output_dir="/nfs/data3/shuaicong/videos_by_images/ovis_discontinuous_V1"

# 确保输出目录存在
mkdir -p "$output_dir"

# 获取当前子文件夹的名字
folder_name=$(basename "$full_path")
echo $full_path

jpg_files=($(find "$full_path" -type f \( -iname "*.jpg" \)))

# 获取照片总数（*.jpg）
count=${#jpg_files[@]}

if [ "$count" -eq 0 ]; then
  echo "⚠️ 目录 $full_path 中没有找到jpg图片。"
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
  echo "结果有 $frames 张图片。"
  cp "$full_path/000236.jpg" "$full_path/000237.jpg"
  added_frame_path="$full_path/000237.jpg"
fi

# 生成输出文件名
output_file="${video_name}_0.0_${frames}.0.mp4"
output_path="$output_dir/$output_file"

echo "🖼️ 总照片数: $count"
echo "🎞️ 使用帧数: $frames"
echo "💾 输出文件: $output_path"

# 创建临时 list 文件（确保唯一性）
list_file="${output_dir}${folder_name}.txt"
> "$list_file"  # 清空或创建文件

# 写入前 $frames 个文件路径到 list 文件
for ((i = 0; i < frames; i++)); do
  echo "file '${jpg_files[$i]}'" >> "$list_file"
done

#  # 调用 ffmpeg
#  ffmpeg -framerate 1 -start_number 1 \
#    -i "$folder/%06d.jpg" \
#    -frames:v $frames -r 1 -pix_fmt yuv420p \
#    "$output_path"
# 调用 ffmpeg 使用 concat 模式
ffmpeg -r 1 -f concat -safe 0 -i "$list_file" \
  -pix_fmt yuv420p -r 1 "$output_path"

# 删除临时添加的帧
if [ -n "$added_frame_path" ]; then
  rm "$added_frame_path"
  echo "🧹 已删除添加的补帧: $added_frame_path"
fi

rm "$list_file"
