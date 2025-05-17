import json


def get_average_video_length(video_json, info_json):
    # 加载 video.json 和 info.json
    with open(video_json, 'r') as f:
        video_list = json.load(f)

    with open(info_json, 'r') as f:
        info_list = json.load(f)

    # 构建 file_name 到 length 的映射
    file_length_map = {item['file_name']: item['length'] for item in info_list}

    # 初始化总长度
    total_video_length = 0
    matched_count = 0

    # 遍历 video 列表，累计长度
    for video_id in video_list:
        if video_id in file_length_map:
            total_video_length += file_length_map[video_id]
            matched_count += 1
        else:
            print(f"未找到 video_id 对应的长度: {video_id}")

    # 计算平均长度
    if matched_count > 0:
        print(f"总共有 {matched_count} 个视频，总长度为 {total_video_length}")
        average_length = total_video_length / matched_count
        print(f"平均视频长度为: {average_length}")
    else:
        print("未匹配到任何视频长度信息")

    return total_video_length, matched_count


total_video_length_train, matched_count_train = get_average_video_length('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/ours_unique_training_videos.json',
                                '/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/video_info_train.json')
total_video_length_valid, matched_count_valid = get_average_video_length('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/ours_unique_valid_videos.json',
                                '/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/video_info_valid.json')
total_length_all = total_video_length_train + total_video_length_valid
total_count_all = matched_count_train + matched_count_valid
# 总共有 533 个视频，总长度为 36991
# 平均视频长度为: 69.4015009380863
# 总共有 137 个视频，总长度为 8377
# 平均视频长度为: 61.14598540145985
# 总共有 670 个视频，总长度为 45368
# 平均视频长度为: 67.7134328358209
print(f"总共有 {total_count_all} 个视频，总长度为 {total_length_all}")
average_length_all = total_length_all / total_count_all
print(f"平均视频长度为: {average_length_all}")

mot17_train = ['MOT17-02', 'MOT17-04', 'MOT17-05', 'MOT17-09', 'MOT17-10', 'MOT17-11', 'MOT17-13']
mot17_valid = ['MOT17-01', 'MOT17-03', 'MOT17-06', 'MOT17-07', 'MOT17-08', 'MOT17-12', 'MOT17-14']

mot20_train = ['MOT20-01', 'MOT20-02']
mot20_valid = ['MOT20-03', 'MOT20-05']

def get_average_video_length_by_array(video_array, info_json):
    # 假设 info.json 已经存在
    with open(info_json, 'r') as f:
        info_list = json.load(f)

    # 构建 file_name 到 length 的映射
    file_length_map = {item['file_name']: item['length'] for item in info_list}

    # 累加视频总长度
    total_video_length = 0
    matched_count = 0

    # 遍历 mot17_train，查找对应的 length
    for video_id in video_array:
        if video_id in file_length_map:
            total_video_length += file_length_map[video_id]
            matched_count += 1
        else:
            print(f"未找到视频 {video_id} 的长度信息")

    # 计算平均长度
    if matched_count > 0:
        print(f"总共有 {matched_count} 个视频，总长度为 {total_video_length}")
        average_length = total_video_length / matched_count
        print(f"平均视频长度为: {average_length}")
    else:
        print("未匹配到任何视频长度信息")

    return total_video_length, matched_count

info_file = '/Users/shuaicongwu/PycharmProjects/data_processing/MOT/video_mot.json'
total_video_length_mot17_train, matched_count_mot17_train = get_average_video_length_by_array(mot17_train, info_file)
total_video_length_mot17_valid, matched_count_mot17_valid = get_average_video_length_by_array(mot17_valid, info_file)
total_length_all_mot17 = total_video_length_mot17_train + total_video_length_mot17_valid
total_count_all_mot17 = matched_count_mot17_train + matched_count_mot17_valid
# 总共有 7 个视频，总长度为 5316
# 平均视频长度为: 759.4285714285714
# 总共有 7 个视频，总长度为 5919
# 平均视频长度为: 845.5714285714286
# 总共有 14 个视频，总长度为 11235
# 平均视频长度为: 802.5
print(f"总共有 {total_count_all_mot17} 个视频，总长度为 {total_length_all_mot17}")
average_length_all_mot17 = total_length_all_mot17 / total_count_all_mot17
print(f"平均视频长度为: {average_length_all_mot17}")

total_video_length_mot20_train, matched_count_mot20_train = get_average_video_length_by_array(mot20_train, info_file)
total_video_length_mot20_valid, matched_count_mot20_valid = get_average_video_length_by_array(mot20_valid, info_file)
total_length_all_mot20 = total_video_length_mot20_train + total_video_length_mot20_valid
total_count_all_mot20 = matched_count_mot20_train + matched_count_mot20_valid
# 总共有 2 个视频，总长度为 3211
# 平均视频长度为: 1605.5
# 总共有 2 个视频，总长度为 5720
# 平均视频长度为: 2860.0
# 总共有 4 个视频，总长度为 8931
# 平均视频长度为: 2232.75
print(f"总共有 {total_count_all_mot20} 个视频，总长度为 {total_length_all_mot20}")
average_length_all_mot20 = total_length_all_mot20 / total_count_all_mot20
print(f"平均视频长度为: {average_length_all_mot20}")
