import json
from collections import OrderedDict


def convert_charades_form(input_file, output_file):
    # 指定字段的输出顺序
    field_order = ["qid", "query", "duration", "vid", "relevant_windows"]

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            obj = json.loads(line)
            filtered_obj = OrderedDict()
            for key in field_order:
                if key in obj:
                    filtered_obj[key] = obj[key]
            outfile.write(json.dumps(filtered_obj) + '\n')

convert_charades_form('/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/All/MOT17/mot17_train_release_no_ids.jsonl',
                      '/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/charades_sta_format/mot17_train_release_sta.jsonl')
convert_charades_form('/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/All/MOT17/mot17_val_release_no_ids.jsonl',
                      '/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/charades_sta_format/mot17_val_release_sta.jsonl')
convert_charades_form('/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/All/MOT20/mot20_train_release_no_ids.jsonl',
                      '/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/charades_sta_format/mot20_train_release_sta.jsonl')
convert_charades_form('/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/All/MOT20/mot20_val_release_no_ids.jsonl',
                      '/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/charades_sta_format/mot20_val_release_sta.jsonl')
convert_charades_form('/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/All/OVIS/ovis_train_release_no_ids.jsonl',
                      '/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/charades_sta_format/ovis_train_release_sta.jsonl')
convert_charades_form('/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/All/OVIS/ovis_val_release_no_ids.jsonl',
                      '/Users/shuaicongwu/PycharmProjects/data_processing/FlashVTG/charades_sta_format/ovis_val_release_sta.jsonl')