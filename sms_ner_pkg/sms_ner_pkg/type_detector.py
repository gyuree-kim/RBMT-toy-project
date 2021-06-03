import os

def type_detector(message):
    type = ""
    num = "0"
    # 방문, 이용자, 식사하신 분,식사 후, 탑승자

    if "신규 확진자" in message and "방문자" not in message :
        type = "infected"
        for i, word in enumerate(message.split()) :
            if ("명" in word) and ("발생" in message.split()[i+1]) :
                num = str(word[:-1])
    elif "방문자" in message:
        type = "event"

    return type, int(num)