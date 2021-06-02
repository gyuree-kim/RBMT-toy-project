import time

class DateDetector():
    def __init__(self):
        self.dates = []
        self.words = [] #각 문장별로 문장의 단어들을 저장
        self.dateWords = [
            '오늘', '내일', '모레', '글피', '주말', '휴일'
            '월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일',
            '월욜', '화욜', '수욜', '목욜', '금욜', '토욜', '일욜',
            '이번주', '다음주', '이번 주', '다음 주', '담주'
        ]
        self.targetWords = ['월', '일', '뒤', '후']

    def getDates(self):
        return self.dates

    def addDate(self, date):
        if date :
            if '뒤' in date or '후' in date:
                self.dates[-1] = self.dates[-1]+date
            else : self.dates.append(date)

    def hasNumbers(self, word):
        return any(char.isdigit() for char in word)

    def isDateFormat(self, input):
        try:
            time.strptime(input, '%m.%d')
            return True
        except ValueError:
            return False

    # 날짜와 관련된 단어인지 유효성 검사
    def isValid(self, word, idx):
        if '월' in word or '일' in word:
            return self.hasNumbers(word)
        if '뒤' in word or '후' in word:
            if self.hasNumbers(word):
                return True
            elif self.words[idx-1] in self.dates:
                return True
        else : return False

    # 단어에 포함된 특수문자 제거
    def deleteSpecialCharacters(self, word):
        word = ''.join(char for char in word if char.isalnum())
        return word

    # 각 문장에 포함된 날짜와 관련된 단어를 dates에 추가
    def date_detector(self, message):
        words = message.split()
        self.words = words
        for word in words:
            # 정규식 검사
            index = word.index('~') if '~' in word else word.index('-') if '-' in word else 0
            if index != 0: # 기간으로 주어지는 경우
                start, end = word[:index], word[index + 1:]
                if self.isDateFormat(start) and self.isDateFormat(end):
                    self.addDate(start + "-" + end)
                    continue
            else:
                if "(" in word: word = str(word[:word.index("(")])
                if self.isDateFormat(str(word)):
                    self.addDate(word)
                    continue

            # dateWords 내의 단어가 있는지 검사
            done = False
            for dateWord in self.dateWords:
                if dateWord in word:
                    _dateWord = self.deleteSpecialCharacters(dateWord) #특수문자 삭제
                    self.addDate(_dateWord)
                    done = True
            if done: continue

            # targetWords 내의 단어가 있는지 검사
            for targetWord in self.targetWords:
                if targetWord in word:
                    idx = words.index(word)
                    if self.isValid(word,idx):
                        _word = self.deleteSpecialCharacters(word) #특수문자 삭제
                        self.addDate(_word.split('에')[0]) #조사 삭제

        return self.getDates()
