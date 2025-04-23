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
            start = float(start_str)
            end = float(end_str)
        except ValueError:
            continue

        key = (video, ids, query)
        if key not in temporal_lookup:
            temporal_lookup[key] = []
        temporal_lookup[key].append([start, end])

    return temporal_lookup

def load_temporal_ground_truth(jsonl_path):
    qid_to_temporal = {}
    with open(jsonl_path, 'r') as f:
        for line in f:
            item = json.loads(line)
            qid_to_temporal[item["qid"]] = item["pred_relevant_windows"]
    return qid_to_temporal


def process_annotation(ann, video_lengths, root_dir, temporal_lookup, video_id_map, next_video_id):
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

    if video_name not in video_id_map:
        video_id_map[video_name] = next_video_id
        next_video_id += 1

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


def generate_submission(video_info_path, annotation_path, spatial_root_dir, output_path):
    video_lengths = load_video_lengths(video_info_path)
    annotations = load_annotations(annotation_path)
    submission = {"queries": []}
    video_id_map = {}
    next_video_id = 1
    temporal_lookup = build_temporal_lookup(annotation_path)

    for ann in annotations:
        result = process_annotation(
            ann,
            video_lengths,
            spatial_root_dir,
            temporal_lookup,
            video_id_map,
            next_video_id
        )
        if result:
            video_name = result["video_name"]
            if video_name not in video_id_map:
                video_id_map[video_name] = next_video_id
                next_video_id += 1
            result["video_id"] = video_id_map[video_name]
            submission["queries"].append(result)

    with open(output_path, 'w') as f:
        json.dump(submission, f, separators=(',', ':'))


# 示例调用
if __name__ == "__main__":
    start_time = time.time()
    generate_submission(
        video_info_path='../../OVIS/video_info_valid.json',
        annotation_path='../../Rephrased data/OVIS-valid-doubled.json',
        spatial_root_dir='/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/svag_evaluation/ovis-gt/valid',
        output_path='ovis_valid_ground_truth.json'
    )
    end_time = time.time()
    print(f"Submission generated in {end_time - start_time:.2f} seconds.")