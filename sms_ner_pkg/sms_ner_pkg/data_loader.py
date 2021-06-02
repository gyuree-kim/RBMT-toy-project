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
        names=['chosung', 'hash'],
        # index_col=0
    )
    keys = df['chosung']
    values = df['hash']

    # 첫글자 초성 추출
    first_chosung = ""
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    for w in list(name[0].strip()):
        if '가' <= w <= '힣':
            # 588개 마다 초성이 바뀜.
            ch = (ord(w) - ord('가')) // 588
            first_chosung += CHOSUNG_LIST[ch]

    # 초성 인덱스 추출
    keys = list(keys)
    keys[-1] = 'NULL'
    for i, key in enumerate(keys):
        if first_chosung == key:
            index = values[i]
            next_index = values[i+1]

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

def subway_loader(name):
    file_path = './sms_ner_pkg/data/dictionary/subway_station_names.xlsx'
    return _read_subway_file(file_path, name)

def store_loader():
    dir_path = './sms_ner_pkg/data/dictionary/store_names'
    return _read_store_files(dir_path)

def store_loader_with_city(city):
    file_path = './sms_ner_pkg/data/dictionary/store_data' + city + '.csv'
    df = pd.read_csv(file_path)
    return df

def sms_data_loader():
    file_path = './sms_ner_pkg/data/input/sms_data.txt'
    return _read_sms_file(file_path)
