import os
import json
from collections import defaultdict
from typing import Dict, List, Any, Optional
import time

# for OVIS valid set
def load_video_lengths(video_info_path):
    with open(video_info_path, 'r') as f:
        video_info = json.load(f)
    return {item['file_name']: item['length'] for item in video_info}


def load_annotations(annotation_path):
    with open(annotation_path, 'r') as f:
        return json.load(f)


def query_to_slug(query):
    return query.lower().replace(' ', '-')


def read_gt_file(predict_path):
    track_data = defaultdict(dict)
    if not os.path.exists(predict_path):
        return track_data

    with open(predict_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 6:
                continue
            frame_id = int(parts[0])
            obj_id = int(parts[1])
            x = int(parts[2])
            y = int(parts[3])
            w = int(parts[4])
            h = int(parts[5])
            track_data[obj_id][frame_id] = [x, y, w, h]
    return track_data


def build_spatial_array(track_frames, video_length):
    spatial = []
    for frame_id in range(video_length):
        if frame_id+1 in track_frames:
            spatial.append(track_frames[frame_id+1])
        else:
            spatial.append(None)
    return spatial

def build_temporal_lookup(annotation_path):
    with open(annotation_path, 'r') as f:
        annotations = json.load(f)

    temporal_lookup = {}

    for ann in annotations:
        video = ann["Video"]
        ids = ann["IDs"]
        query = ann["Language Query"]
        start_str = ann["Start"]
        end_str = ann["End"]

        if not start_str or not end_str:
            continue

        try:
            start = int(start_str)
            end = int(end_str)
        except ValueError:
            continue

        key = (video, ids, query)
        if key not in temporal_lookup:
            temporal_lookup[key] = []
        temporal_lookup[key].append([start, end])

    return temporal_lookup

def build_temporal_lookup_by_query(annotation_path):
    with open(annotation_path, 'r') as f:
        annotations = json.load(f)

    lookup_by_query = {}

    for ann in annotations:
        video = ann["Video"]
        ids = ann["IDs"]
        query = ann["Language Query"]
        start_str = ann["Start"]
        end_str = ann["End"]

        if not start_str or not end_str:
            continue

        try:
            start = int(start_str)
            end = int(end_str)
            ids = int(ids)
        except ValueError:
            continue

        key = (video, query)
        if key not in lookup_by_query:
            lookup_by_query[key] = []
        lookup_by_query[key].append((ids, [start, end]))

    return lookup_by_query

def load_temporal_ground_truth(jsonl_path):
    qid_to_temporal = {}
    with open(jsonl_path, 'r') as f:
        for line in f:
            item = json.loads(line)
            qid_to_temporal[item["qid"]] = item["pred_relevant_windows"]
    return qid_to_temporal


def process_annotation(ann, video_lengths, root_dir, temporal_lookup, video_id_map):
    video_name = ann['Video']
    qid = int(ann['QID'])
    query_text = ann['Language Query']
    query_slug = query_to_slug(query_text)

    if video_name not in video_lengths:
        return None

    video_length = video_lengths[video_name]
    video_path = os.path.join(root_dir, video_name)
    query_path = os.path.join(video_path, query_slug)
    gt_file = os.path.join(query_path, 'gt.txt')

    if not os.path.exists(gt_file):
        return None

    video_id = video_id_map[video_name]
    track_data = read_gt_file(gt_file)

    tracks = []
    for track_id, frames in track_data.items():
        spatial = build_spatial_array(frames, video_length)
        key = (video_name, str(track_id), query_text)
        temporal = temporal_lookup.get(key, [])

        tracks.append({
            "track_id": track_id,
            "spatial": spatial,
            "temporal": temporal
        })

    return {
        "query_id": qid,
        "query": query_text,
        "video_id": video_id,
        "video_name": video_name,
        "tracks": tracks
    }

# avoid same track appear multiple times based on times of [start,end]
def process_annotation_2(ann, video_lengths, root_dir, temporal_lookup, video_id_map, track_map):
    video_name = ann['Video']
    qid = int(ann['QID'])
    query_text = ann['Language Query']
    query_slug = query_to_slug(query_text)

    if video_name not in video_lengths:
        return

    video_length = video_lengths[video_name]
    video_path = os.path.join(root_dir, video_name)
    query_path = os.path.join(video_path, query_slug)
    gt_file = os.path.join(query_path, 'gt.txt')

    if not os.path.exists(gt_file):
        print(f'不存在gt_file：{gt_file}')
        return

    video_id = video_id_map[video_name]
    track_data = read_gt_file(gt_file)

    for track_id, frames in track_data.items():
        key = (video_name, query_text, track_id)
        spatial = build_spatial_array(frames, video_length)
        temporal = temporal_lookup.get((video_name, str(track_id), query_text), [])

        # 存储唯一轨迹信息
        if key not in track_map:
            track_map[key] = {
                "video_id": video_id,
                "video_name": video_name,
                "video_length": video_length,
                "query_id": qid,
                "query": query_text,
                "track_id": track_id,
                "spatial": spatial,
                "temporal": temporal
            }


def generate_submission(video_info_path, annotation_path, spatial_root_dir, output_path):
    video_lengths = load_video_lengths(video_info_path)
    annotations = load_annotations(annotation_path)
    submission = {"queries": []}
    video_id_map = {}
    next_video_id = 1
    temporal_lookup = build_temporal_lookup(annotation_path)

    for ann in annotations:
        video_name = ann['Video']
        if video_name not in video_id_map:
            video_id_map[video_name] = next_video_id
            next_video_id += 1

        result = process_annotation(
            ann,
            video_lengths,
            spatial_root_dir,
            temporal_lookup,
            video_id_map
        )
        if result:
            submission["queries"].append(result)

    with open(output_path, 'w') as f:
        json.dump(submission, f, separators=(',', ':'))


def generate_queries_for_dataset(video_info_path, annotation_path, spatial_root_dir, dataset_name):
    video_lengths = load_video_lengths(video_info_path)
    annotations = load_annotations(annotation_path)
    temporal_lookup = build_temporal_lookup(annotation_path)
    temporal_lookup_by_query = build_temporal_lookup_by_query(annotation_path)

    video_id_map = {}
    next_video_id = 1
    track_map = {}
    filled_tracks = {}

    for ann in annotations:
        video_name = ann['Video']
        query_text = ann['Language Query']
        qid = int(ann['QID'])

        if video_name not in video_id_map:
            video_id_map[video_name] = next_video_id
            next_video_id += 1

        prev_track_count = len(track_map)
        process_annotation_2(
            ann,
            video_lengths,
            spatial_root_dir,
            temporal_lookup,
            video_id_map,
            track_map
        )
        post_track_count = len(track_map)

        if post_track_count == prev_track_count:
            video_length = video_lengths.get(video_name)
            if video_length is None:
                continue

            key = (video_name, query_text)
            video_id = video_id_map[video_name]
            temporal_items = temporal_lookup_by_query.get(key, [])

            for track_id, temporal in temporal_items:
                track_key = (video_name, query_text, track_id)
                if track_key in track_map:
                    continue  # 已存在

                filled_tracks[track_key] = {
                    "video_id": video_id,
                    "video_name": video_name,
                    "video_length": video_length,
                    "query_id": qid,
                    "query": query_text,
                    "track_id": track_id,
                    "spatial": [None] * video_length,
                    "temporal": [temporal]
                }

    print('处理完annotations，合并中。。。')
    # 合并为唯一的 queries 结构
    merged_tracks = {**track_map, **filled_tracks}
    query_group = {}
    for (video_name, query_text, track_id), track_info in merged_tracks.items():
        key = (video_name, query_text)
        if key not in query_group:
            query_group[key] = {
                "query_id": track_info["query_id"],
                "query": track_info["query"],
                "video_id": track_info["video_id"],
                "video_name": track_info["video_name"],
                "video_length": track_info["video_length"],
                "tracks": []
            }
        query_group[key]["tracks"].append({
            "track_id": track_info["track_id"],
            "spatial": track_info["spatial"],
            "temporal": track_info["temporal"]
        })

    return {
        "name": dataset_name,
        "queries": list(query_group.values())
    }

def generate_all_datasets_submission(configs, output_path):
    datasets = []
    for config in configs:
        dataset = generate_queries_for_dataset(
            video_info_path=config["video_info_path"],
            annotation_path=config["annotation_path"],
            spatial_root_dir=config["spatial_root_dir"],
            dataset_name=config["name"]
        )
        datasets.append(dataset)
        print('处理完一个config。')

    with open(output_path, 'w') as f:
        json.dump({"datasets": datasets}, f, separators=(',', ':'))

# 示例调用
if __name__ == "__main__":
    start_time = time.time()
    # generate_submission(
    #     video_info_path='../../OVIS/video_info_valid.json',
    #     annotation_path='../../Rephrased data/OVIS-valid-doubled.json',
    #     spatial_root_dir='/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/svag_evaluation/ovis-gt/valid',
    #     output_path='ovis_valid_ground_truth.json'
    # )

    configs = [
        {
            "name": "OVIS",
            "video_info_path": "/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/video_info_valid.json",
            "annotation_path": "/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/OVIS-valid-doubled_qid.json",
            "spatial_root_dir": "/Users/shuaicongwu/PycharmProjects/data_processing/SVAGEval/gt-per-query/ovis/valid"
        },
        {
            "name": "MOT17",
            "video_info_path": "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/video_mot.json",
            "annotation_path": "/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/MOT17-valid-doubled_qid.json",
            "spatial_root_dir": "/Users/shuaicongwu/PycharmProjects/data_processing/SVAGEval/gt-per-query/mot17/valid"
        },
        {
            "name": "MOT20",
            "video_info_path": "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/video_mot.json",
            "annotation_path": "/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/MOT20-valid-doubled_qid.json",
            "spatial_root_dir": "/Users/shuaicongwu/PycharmProjects/data_processing/SVAGEval/gt-per-query/mot20/valid"
        }
    ]

    generate_all_datasets_submission(configs, output_path='valid_all_ground_truth.json')
    end_time = time.time()
    print(f"Submission generated in {end_time - start_time:.2f} seconds.")