import json
import spacy
from matplotlib import pyplot as plt
from collections import Counter

from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
from wordcloud import WordCloud

nlp = spacy.load("en_core_web_lg")


# Original data for #Tracks
mot17_training_original = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-training.json'
mot17_valid_original = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT17-valid.json'
mot20_training_original = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT20-training.json'
mot20_valid_original = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/MOT20-valid.json'
ovis_training_original = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/OVIS-training.json'
ovis_valid_original = '/Users/shuaicongwu/PycharmProjects/data_processing/Original/OVIS-valid.json'
original = [mot17_training_original, mot17_valid_original, mot20_training_original, mot20_valid_original, ovis_training_original, ovis_valid_original]

# Rephrased data for #Queries
mot17_training_rephrased = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-training-doubled.json'
mot17_valid_rephrased = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT17-valid-doubled.json'
mot20_training_rephrased = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-training-doubled.json'
mot20_valid_rephrased = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/MOT20-valid-doubled.json'
ovis_training_rephrased = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json'
ovis_valid_rephrased = '/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json'
rephrased = [mot17_training_rephrased, mot17_valid_rephrased, mot20_training_rephrased, mot20_valid_rephrased, ovis_training_rephrased, ovis_valid_rephrased]
paths_mot17 = [mot17_training_rephrased, mot17_valid_rephrased]
paths_mot20 = [mot20_training_rephrased, mot20_valid_rephrased]
paths_ovis = [ovis_training_rephrased, ovis_valid_rephrased]

def count_of_json_objects(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    print(f"{file_path} JSON 对象数量：{len(data)}")
    return len(data)

def count_sum_of_json_objects(path_list):
    sum = 0
    for file in path_list:
        sum += count_of_json_objects(file)
    return sum

# MOT17: 775+698=1473, MOT20: 2275+1670=3975, OVIS: 3685+678=4363
# SUM: 9781 #Tracks
# print(f'original 文件对象总数是：{count_sum_of_json_objects(original)}')
# MOT17: 1538+1397=2935, MOT20: 4544+3403=7947, OVIS: 7352+1356=8708
# SUM: 19590 #Queries
# print(f'original 文件对象总数是：{count_sum_of_json_objects(rephrased)}')

def count_number_of_videos(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    unique_videos = set(item['Video'] for item in data)

    print(f'{file_path} 有 {len(unique_videos)} 个不同的Video')
    return len(unique_videos)

def count_sum_of_videos(path_list):
    sum = 0
    for file in path_list:
        sum += count_number_of_videos(file)
    return sum

# MOT17: 7+7=14, MOT20: 2+2=4, OVIS: 533+137=670
# SUM: 688
# print(f'Ours所用视频的数量是：{count_sum_of_videos(original)}')


# 使用rephrased中唯一的queries来动词数量和频率，词云，和表格里的#Tracks, #Queries无关
def get_all_unique_queries(file_paths):
    unique_queries = set()
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                unique_queries.add(item['Language Query'])
    return unique_queries

unique_queries_all = get_all_unique_queries(rephrased)
unique_queries_mot17 = get_all_unique_queries(paths_mot17)
unique_queries_mot20 = get_all_unique_queries(paths_mot20)
unique_queries_ovis = get_all_unique_queries(paths_ovis)
# print(f'There are in total {len(unique_queries_all)} different kinds of queries in All.')  # 7861
# print(f'There are in total {len(unique_queries_mot17)} different kinds of queries in MOT17.')  # 1255
# print(f'There are in total {len(unique_queries_mot20)} different kinds of queries in MOT20.')  # 1127
# print(f'There are in total {len(unique_queries_ovis)} different kinds of queries in OVIS.')  # 5497


# word count of query and its frequency
def get_word_count_distribution(unique_queries, output_path):
    word_count_distribution = {}

    # Count word frequencies in the queries
    for query in unique_queries:
        word_count = len(query.split())
        if word_count in word_count_distribution:
            word_count_distribution[word_count] += 1
        else:
            word_count_distribution[word_count] = 1

    # Plotting the distribution
    x = list(word_count_distribution.keys())  # Word counts (x-axis)
    y = list(word_count_distribution.values())  # Query counts (y-axis)

    plt.figure(figsize=(10, 6))
    plt.bar(x, y)
    plt.xlabel('Word Count per Query')
    plt.ylabel('Count of Queries')
    plt.title('Distribution of Query Word Count')
    plt.xticks(x)  # Ensure each word count has its own tick on the x-axis

    plt.savefig(output_path, format='png', dpi=300)
    print(f"结果已保存到 {output_path}")

# get_word_count_distribution(unique_queries_all, '/Users/shuaicongwu/PycharmProjects/data_processing/results/visualization/word_count_distribution_all.png')


def get_verb_and_frequency_from_sentences(dataset, sentences, output_file_path):
    # take a long time to finish computing
    verbs_list = []

    for sentence in sentences:
        doc = nlp(sentence)
        # type of verbs is <list>
        verbs = [token for token in doc if token.pos_ == "VERB" and token.dep_ != "AUX"]
        # print(sentence, "Detected Verbs:", verbs)

        # if any(verb.text in ('left', 'rightward') for verb in verbs):
        #     print(f"跳过的句子: {sentence}, {verbs}")
        #     continue

        walk_verbs = ['walk', 'walks', 'walking', 'walked']
        ignore_verbs = ['left', 'rightward']

        # 如果 'walk' 系列动词在 verbs 中，并且还有其他动词，移除 'walk' 系列动词
        if any(verb.text in walk_verbs for verb in verbs) and len(verbs) > 1:
            verbs = [verb for verb in verbs if verb.text not in walk_verbs]
            # print(verbs, sentence)

        # 如果 'ignore_verbs' 系列动词在 verbs 中，并且还有其他动词，移除 'ignore_verbs' 系列动词
        # 如果没有其他动词，则也移除
        if any(verb.text in ignore_verbs for verb in verbs):
            verbs = [verb for verb in verbs if verb.text not in ignore_verbs]
            # print(f'remove left and rightward verbs from {sentence}')

        filtered_verbs = []
        for i, cur_verb in enumerate(verbs):
            cur_verb_index = cur_verb.i

            # 查找 cur_verb 前一个单词
            if cur_verb_index > 0:
                pre_verb = doc[cur_verb_index - 1]

                # 如果 pre_verb 是动词并且在 verbs 中，说明是连续动词，应该跳过当前动词
                if pre_verb.pos_ == "VERB" and pre_verb in verbs:
                    continue  # 跳过当前动词

            # 如果没有移除，则保留当前动词
            filtered_verbs.append(cur_verb.text)

        verbs_list.extend(filtered_verbs)


    # count frequency of the words
    item_frequency = Counter(verbs_list)
    print(f'The number of different verbs (include tense) in {dataset}: {len(item_frequency)}')

    sorted_items = sorted(item_frequency.items(), key=lambda x: (-x[1], x[0]))

    data_dict = {}

    for item, frequency in sorted_items:
        data_dict[item] = frequency

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)

# 在结果处手动添加 {"sprints": 6, "brushes": 2}到all和ovis => 900 不要再次运行啦！以免达不到900
# get_verb_and_frequency_from_sentences('all', unique_queries_all, '/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_ours_all.json') # 898->900
# get_verb_and_frequency_from_sentences('mot17', unique_queries_mot17, '/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_mot17.json') # 260
# get_verb_and_frequency_from_sentences('mot20', unique_queries_mot20, '/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_mot20.json') # 212
# get_verb_and_frequency_from_sentences('ovis', unique_queries_ovis, '/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_ovis.json') # 763->765

def compare_two_json(file1, file2):
    # 读取两个 JSON 文件
    with open(file1, 'r') as f1:
        verbs1 = json.load(f1)
    with open(file2, 'r') as f2:
        verbs2 = json.load(f2)

    # 将动词键转换为集合
    set1 = set(verbs1.keys())
    set2 = set(verbs2.keys())

    # 找出 verbs1 中有但 verbs2 中没有的动词
    extra_in_1 = set1 - set2

    # 找出 verbs2 中有但 verbs1 中没有的动词
    extra_in_2 = set2 - set1

    # 输出结果
    print("verbs1 中多出来的动词：", extra_in_1)
    print("verbs2 中多出来的动词：", extra_in_2)

# compare_two_json('/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_ours_all.json', '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/verbs_json/verbs/verbs_ours_all.json')

# top50_verbs
def convert_verbs_to_base(json_file, output_file, output_path):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lemmatizer = WordNetLemmatizer()
    base_verbs = {}

    for word, freq in data.items():
        base_form = lemmatizer.lemmatize(word, wordnet.VERB)  # 转换为原形
        if base_form in base_verbs:
            base_verbs[base_form] += freq  # 归一化后合并计数
        else:
            base_verbs[base_form] = freq

    # 按频率降序排序
    sorted_base_verbs = dict(sorted(base_verbs.items(), key=lambda item: item[1], reverse=True))

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_base_verbs, f, ensure_ascii=False, indent=4)

    print(f"转换完成，结果已保存到 {output_file}")
    print(f"输出 JSON 长度: {len(sorted_base_verbs)}")  # 493

    # 绘制前 50 个结果的柱状图
    top_50 = list(sorted_base_verbs.items())[:50]
    words, freqs = zip(*top_50)

    plt.figure(figsize=(15, 6))
    plt.bar(words, freqs, color='skyblue')
    # plt.xlabel("Verbs")
    plt.ylabel("Count")
    plt.title("Actions")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)

    # plt.show()


# convert_verbs_to_base('/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_ours_all.json',
#                       '/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_base_all.json',
#                       '/Users/shuaicongwu/PycharmProjects/data_processing/results/visualization/top50_verbs.png')

# word cloud
verbs_ours_all = '/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_ours_all.json'
verbs_mot17 = '/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_mot17.json'
verbs_mot20 = '/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_mot20.json'
verbs_ovis = '/Users/shuaicongwu/PycharmProjects/data_processing/results/verbs/verbs_ovis.json'

def draw_wordcloud(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    font_path = '/Library/Fonts/Arial.ttf'
    wordcloud = WordCloud(width=1600, height=800, background_color='white', font_path=font_path,
                          scale=2).generate_from_frequencies(data)

    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight', pad_inches=0.05)
    # plt.show()


draw_wordcloud(verbs_ours_all, '/Users/shuaicongwu/PycharmProjects/data_processing/results/visualization/wordcloud_ours_all.png')
draw_wordcloud(verbs_mot17, '/Users/shuaicongwu/PycharmProjects/data_processing/results/visualization/wordcloud_mot17.png')
draw_wordcloud(verbs_mot20, '/Users/shuaicongwu/PycharmProjects/data_processing/results/visualization/wordcloud_mot20.png')
draw_wordcloud(verbs_ovis, '/Users/shuaicongwu/PycharmProjects/data_processing/results/visualization/wordcloud_ovis.png')

