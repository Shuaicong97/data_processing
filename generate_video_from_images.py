import cv2
import os

def images_to_video(image_folder, output_video, fps=1):
    """将指定文件夹中的图片合成为视频"""
    images = [img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))]
    images.sort()  # 按文件名排序

    if not images:
        print(f"文件夹 {image_folder} 内无图片，跳过...")
        return

    # 读取第一张图片获取宽高
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    h, w, layers = frame.shape

    # 定义视频编码器（MP4格式）
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    video = cv2.VideoWriter(output_video, fourcc, fps, (w, h))

    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"警告: 无法读取 {image_path}，跳过该帧")
            continue
        video.write(frame)

    video.release()
    print(f"✅ 视频已保存: {output_video}")

def process_train_folder(train_folder, output_folder, fps=1):
    """遍历 train 目录，每个子文件夹生成一个视频"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # 确保输出目录存在

    for subfolder in os.listdir(train_folder):
        subfolder_path = os.path.join(train_folder, subfolder)
        if os.path.isdir(subfolder_path):  # 仅处理文件夹
            output_video_path = os.path.join(output_folder, f"{subfolder}.mp4")
            print(f"🎬 处理视频: {subfolder}")
            images_to_video(subfolder_path, output_video_path, fps)

# 设定目录
train_dir = "/nfs/data3/shuaicong/refer-ovis/OVIS/training"  # 你的 train 目录
valid_dir = "/nfs/data3/shuaicong/refer-ovis/OVIS/valid"  # 你的 train 目录
train_output_dir = "/nfs/data3/shuaicong/data_processing/videos_ovis/training"  # 生成的视频存放目录
valid_output_dir = "/nfs/data3/shuaicong/data_processing/videos_ovis/valid"  # 生成的视频存放目录

# 执行转换
# process_train_folder(train_dir, train_output_dir, fps=1)
process_train_folder(valid_dir, valid_output_dir, fps=1)
