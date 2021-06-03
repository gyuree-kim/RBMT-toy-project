from sms_ner_pkg.type_detector import type_detector as type_detector
from sms_ner_pkg.date_detector import DateDetector as DateDetector
from sms_ner_pkg.time_detector import TimeDetector as TimeDetector
from sms_ner_pkg.location_detector import loc_detector as location_detector

message = "[서울시청] 06.02(수) 00시 기준 서울시 신규 확진자 258명 발생. 자치구별 현황 및 동선 등은 bitly.co/617T참고하시기 바랍니다."
# message = "[중대본] 5.15~5.27 서울시 노원구 한글비석로48길 9, 지하1층 공간카페 방문자는 가까운 보건소에서 코로나19 검사를 받으시기바랍니다"

type, num = type_detector(message)
dateDetector = DateDetector()
date = dateDetector.date_detector(message)
timeDetector = TimeDetector()
time = timeDetector.time_detector(message)
location = location_detector([message], type)

if not date : print("date not found")
elif not location: print("location not found")
elif not time :
    result = [type, date[0], "", location, num]
    print(result)
else :
    result = [type, date[0], time[0], location, num]
    print(result)
