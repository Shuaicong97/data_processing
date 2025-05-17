import os
import json
from collections import defaultdict
from typing import Dict, List, Any, Optional
import time


def load_video_lengths(video_info_path):
    with open(video_info_path, 'r') as f:
        video_info = json.load(f)
    return {item['file_name']: item['length'] for item in video_info}


def load_annotations(annotation_path):
    with open(annotation_path, 'r') as f:
        return json.load(f)


def query_to_slug(query):
    return query.lower().replace(' ', '-')


def read_prediction_file(predict_path):
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
            track_data[obj_id][frame_id] = [float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])]
    return track_data


def build_spatial_array(track_frames, video_length):
    spatial = []
    for frame_id in range(video_length):
        if frame_id+1 in track_frames:
            spatial.append(track_frames[frame_id+1])
        else:
            spatial.append(None)
    return spatial


def load_temporal_predictions(jsonl_path):
    qid_to_temporal = {}
    with open(jsonl_path, 'r') as f:
        for line in f:
            item = json.loads(line)
            qid_to_temporal[item["qid"]] = item["pred_relevant_windows"]
    return qid_to_temporal


def process_annotation(ann, video_lengths, root_dir, qid_to_temporal, video_id_map):
    video_name = ann['Video']
    qid = int(ann['QID'])
    query_text = ann['Language Query']
    query_slug = query_to_slug(query_text)

    if video_name not in video_lengths:
        return None

    video_length = video_lengths[video_name]
    video_path = os.path.join(root_dir, video_name)
    query_path = os.path.join(video_path, query_slug)
    predict_file = os.path.join(query_path, 'predict.txt')

    if not os.path.exists(predict_file):
        return None

    video_id = video_id_map[video_name]
    track_data = read_prediction_file(predict_file)

    tracks = []
    temporal = qid_to_temporal[qid]
    for track_id, frames in track_data.items():
        spatial = build_spatial_array(frames, video_length)
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


def generate_submission(video_info_path, annotation_path, spatial_root_dir, temporal_pred_path, output_path):
    video_lengths = load_video_lengths(video_info_path)
    annotations = load_annotations(annotation_path)
    submission = {"queries": []}
    video_id_map = {}
    next_video_id = 1
    qid_to_temporal = load_temporal_predictions(temporal_pred_path)
    query_track_map = {}

    for ann in annotations:
        video_name = ann['Video']
        qid = int(ann['QID'])
        query_text = ann['Language Query']
        query_key = (video_name, query_text)

        if video_name not in video_id_map:
            video_id_map[video_name] = next_video_id
            next_video_id += 1

        result = process_annotation(
            ann,
            video_lengths,
            spatial_root_dir,
            qid_to_temporal,
            video_id_map,
        )
        if result:
            submission["queries"].append(result)

    with open(output_path, 'w') as f:
        json.dump(submission, f, separators=(',', ':'))


def generate_submission_for_dataset(video_info_path, annotation_path, spatial_root_dir, temporal_pred_path, dataset_name):
    video_lengths = load_video_lengths(video_info_path)
    annotations = load_annotations(annotation_path)
    qid_to_temporal = load_temporal_predictions(temporal_pred_path)

    submission = {"queries": []}
    video_id_map = {}
    next_video_id = 1

    # 聚合缓存结构
    query_track_map = {}

    for ann in annotations:
        video_name = ann['Video']
        qid = int(ann['QID'])
        query_text = ann['Language Query']
        query_key = (video_name, query_text)

        if video_name not in video_id_map:
            video_id_map[video_name] = next_video_id
            next_video_id += 1

        video_id = video_id_map[video_name]
        video_length = video_lengths.get(video_name)
        if video_length is None:
            continue

        video_path = os.path.join(spatial_root_dir, video_name)
        query_slug = query_to_slug(query_text)
        predict_file = os.path.join(video_path, query_slug, 'predict.txt')
        if not os.path.exists(predict_file):
            continue

        temporal_data = qid_to_temporal.get(qid, [])
        track_data = read_prediction_file(predict_file)

        if query_key not in query_track_map:
            query_track_map[query_key] = {
                "query_id": qid,
                "query": query_text,
                "video_id": video_id,
                "video_name": video_name,
                "video_length": video_length,
                "tracks": defaultdict(lambda: {"track_id": None, "spatial": None, "temporal": []})
            }

        for track_id, frames in track_data.items():
            spatial = build_spatial_array(frames, video_length)

            track = query_track_map[query_key]["tracks"][track_id]
            track["track_id"] = track_id
            track["spatial"] = spatial
            track["temporal"].extend(temporal_data)  # 多次拼接 temporal

    # 整理提交结构
    for entry in query_track_map.values():
        entry["tracks"] = list(entry["tracks"].values())
        submission["queries"].append(entry)

    return {
        "name": dataset_name,
        "queries": submission["queries"]
    }

def generate_all_datasets_submission(configs, output_path):
    datasets = []
    for config in configs:
        dataset = generate_submission_for_dataset(
            video_info_path=config["video_info_path"],
            annotation_path=config["annotation_path"],
            spatial_root_dir=config["spatial_root_dir"],
            temporal_pred_path=config["temporal_pred_path"],
            dataset_name=config["name"]
        )
        datasets.append(dataset)

    with open(output_path, 'w') as f:
        json.dump({"datasets": datasets}, f, separators=(',', ':'))

# 示例调用
if __name__ == "__main__":
    start_time = time.time()
    configs = [
        {
            "name": "OVIS",
            "video_info_path": "/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/video_info_valid.json",
            "annotation_path": "/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/OVIS-valid-doubled_qid.json",
            "spatial_root_dir": "/Users/shuaicongwu/Desktop/MA_resources/temprmot_results/ovis_with_checkpoint0_5_epochs_0.4_0.3_v4",
            "temporal_pred_path": "/Users/shuaicongwu/Desktop/MA_resources/flashvtg_results/ovis_internvideo2-video_tef-demo-2025-04-21-20-14-59/best_ovis_internvideo2_val_preds_nms_thd_0.7.jsonl"
        },
        {
            "name": "MOT17",
            "video_info_path": "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/video_mot.json",
            "annotation_path": "/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/MOT17-valid-doubled_qid.json",
            "spatial_root_dir": "...",
            "temporal_pred_path": "..."
        },
        {
            "name": "MOT20",
            "video_info_path": "/Users/shuaicongwu/PycharmProjects/data_processing/MOT/video_mot.json",
            "annotation_path": "/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased_data_with_qid/MOT20-valid-doubled_qid.json",
            "spatial_root_dir": "...",
            "temporal_pred_path": "..."
        }
    ]

    generate_all_datasets_submission(configs, output_path='valid_all_ground_truth.json')

    generate_submission_for_dataset(
        video_info_path='../../OVIS/video_info_valid.json',
        annotation_path='../../Rephrased data/OVIS-valid-doubled.json',
        spatial_root_dir='/Users/shuaicongwu/Desktop/MA_resources/temprmot_results/ovis_with_checkpoint0_5_epochs_0.4_0.3_v4',
        temporal_pred_path='/Users/shuaicongwu/Desktop/MA_resources/flashvtg_results/ovis_internvideo2-video_tef-demo-2025-04-21-20-14-59/best_ovis_internvideo2_val_preds_nms_thd_0.7.jsonl',
        output_path='submission.json'
    )
    end_time = time.time()
    print(f"Submission generated in {end_time - start_time:.2f} seconds.")