import os
import re


def time_to_ms(time_str):
    """将时间字符串转换为毫秒"""
    h, m, s_ms = time_str.split(':')
    s, ms = s_ms.split(',')
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)


def get_last_timestamp(srt_file):
    """获取SRT文件的最后一个时间戳"""
    encodings = ["utf-8", "latin-1", "ISO-8859-1"]  # 尝试不同编码
    for encoding in encodings:
        try:
            with open(srt_file, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break  # 读取成功则退出循环
        except UnicodeDecodeError:
            continue  # 读取失败，尝试下一个编码

    time_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")
    last_time = None

    for line in lines:
        match = time_pattern.search(line)
        if match:
            last_time = match.group(2)  # 获取结束时间

    return last_time


def main():
    folder = "/nfs/data3/shuaicong/Hallucination_VLM/datasets/OpenDataLab___MovieNet/raw/files/subtitle"
    one_hour_ms = time_to_ms("01:00:00,000")

    file_count = 0
    for file in os.listdir(folder):
        if file.endswith(".srt"):
            file_count += 1
            if file_count % 50 == 0:
                print(f"Processed {file_count} files...")

            srt_path = os.path.join(folder, file)
            last_time = get_last_timestamp(srt_path)
            if last_time and time_to_ms(last_time) < one_hour_ms:
                print(file)

if __name__ == "__main__":
    main()
