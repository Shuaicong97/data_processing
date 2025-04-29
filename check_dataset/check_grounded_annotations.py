import csv

def check(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            query = row['Language Query']
            if query and not query[0].isupper():
                print(query)

# print('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS(Ashiq).csv')
# check('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS(Ashiq).csv')
# print('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS(Seenat).csv')
# check('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS(Seenat).csv')
# print('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS-Test(Ashiq).csv')
# check('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS-Test(Ashiq).csv')
# print('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS-Test(Seenat).csv')
# check('/Users/shuaicongwu/PycharmProjects/data_processing/OVIS/Latest_Sheet/Grounded Tracking Annotations - OVIS-Test(Seenat).csv')
