# -*- coding: utf-8 -*-
import os
import pandas as pd

def _get_hash_value(file_path, name):
    index = ""
    next_index = ""

    # read hash table file
    sheet_name = 'hash_table'
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        # index_col=0
    )
    keys = df.iloc[:,0]
    values = df.iloc[:,1]

    # 첫글자 초성 추출
    first_chosung = ""
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    for w in list(name[0].strip()):
        # 영어인 경우 구분해서 작성함.
        if '가' <= w <= '힣':
            # 588개 마다 초성이 바뀜.
            ch = (ord(w) - ord('가')) // 588
            first_chosung += CHOSUNG_LIST[ch]
    #print(first_chosung)

    # 초성 인덱스 추출
    for i in range(len(keys)):
        if first_chosung in keys[i] :
            index = values[i]
            next_index = values[i+1]
    #(index, next_index)

    return [index-2, next_index-2]

def _read_subway_file(file_path, name):
    station_names = []
    index = _get_hash_value(file_path, name)
    # index = [128,300]

    sheet_name = '지하철역_명칭'
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    station_names = df.iloc[index[0]:index[1],0] #0열 선택

    return station_names

def _read_store_files(dir_path):
    data = []

    # read all files in 'store_names' dir
    file_list = os.listdir(dir_path)
    for file in file_list:
        file_path = dir_path + '/' + file
        df = pd.read_csv(file_path)
        data.append([file.replace('.csv',''), df])

    return df

def _read_sms_file(file_path):
    sentences = []
    for line in open(file_path, encoding="cp949"):
        line = line.strip()
        if line:
            line = line.split('   ')
            sentences.append(line[len(line) - 1])
    return sentences

# def _read_data_file(file_path, train=True):
#     sentences = []
#     sentence = [[], [], []]
#     for line in open(file_path, encoding="cp949"):
#         line = line.strip()
#         if line == "":
#             sentences.append(sentence)
#             sentence = [[], [], []]
#         else:
#             idx, ejeol, ner_tag = line.split("\t")
#             sentence[0].append(int(idx))
#             sentence[1].append(ejeol)
#             if train:
#                 sentence[2].append(ner_tag)
#             else:
#                 sentence[2].append("-")
#
#     return sentences

def subway_loader(root_path, name):
    file_path = os.path.join(root_path, 'subway_station_names.xlsx')
    return _read_subway_file(file_path, name)

def store_loader(root_path):
    dir_path = os.path.join(root_path, 'dictionary\store_names')
    return _read_store_files(dir_path)

def store_loader_with_city(root_path, city):
    file_name = city + '.csv'
    file_path = os.path.join(root_path, 'dictionary\store_data'+file_name)
    df = pd.read_csv(file_path)
    return df

def sms_data_loader(root_path):
    root_path += '\input'
    file_path = os.path.join(root_path, 'sms_data.txt')
    return _read_sms_file(file_path)

# def test_data_loader(root_path):
#     # [ idx, ejeols, nemed_entitis ] each sentence
#     file_path = os.path.join(root_path, 'test.txt')
#     return _read_data_file(file_path, False)
#
# def data_loader(root_path):
#     # [ idx, ejeols, nemed_entitis ] each sentence
#     file_path = os.path.join(root_path, 'train.txt')
#     return _read_data_file(file_path)

if __name__ == "__main__":
    # os.chdir(r'C:\Users\ghio1\PycharmProjects\senior-project-2021\sms_ner_pkg\sms_ner_pkg\data')
    # current_path = os.getcwd()
    subway_loader("data\\dictionary", "마포")