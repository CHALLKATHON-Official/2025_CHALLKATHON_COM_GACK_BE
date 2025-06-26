import pandas as pd
import os
import re
import time
import schedule
import json
from konlpy.tag import Okt

def read_csv_file(file_path, encoding='utf-8-sig'):
    try:
        df = pd.read_csv(file_path, index_col=0, encoding=encoding)
        print(f" {os.path.basename(file_path)} 불러오기 성공")
        return df
    except Exception as e:
        print(f" {file_path} 읽기 실패:", e)
        return None

# 정확한 경로 (확장자 `.csv` 주의!)
folder = "C:/Users/katdi/OneDrive/바탕 화면/chromedriver-win64"
word_score = read_csv_file(os.path.join(folder, "단어점수0626_1333.csv"))
rel_words = read_csv_file(os.path.join(folder, "연관단어점수0625_2200.csv")) #단어1, 점수1, 단어2, 점수2, ...
main_words = read_csv_file(os.path.join(folder, "신문사메인단어0625_2200.csv"))
google_trend = read_csv_file(os.path.join(folder, "구글트렌드.csv"))
#=====================================================================================================================

def convert_score(value):
    if pd.isna(value) or not isinstance(value, str):
        return 0
    value = value.replace(" ", "")
    score_mapping = {
        "100+": 10, "200+": 20, "500+": 50, "1000+": 100,
        "5000+": 500, "1만+": 1000, "2만+": 2000,
    }
    if value in score_mapping:
        base_score = score_mapping[value]
        if base_score >= 1000:
            return int(base_score * 0.65)
        else:
            return base_score
    if "만+" in value:
        try:
            base_score = int(float(value.replace("만+", "")) * 10000)
            if base_score >= 1000:
                return int(base_score * 0.65)
            return base_score
        except:
            return 0
    if "천+" in value:
        try:
            base_score = int(float(value.replace("천+", "")) * 1000)
            if base_score >= 1000:
                return int(base_score * 0.65)
            return base_score
        except:
            return 0
    if value.endswith("+"):
        try:
            base_score = int(value.replace("+", ""))
            if base_score >= 1000:
                return int(base_score * 0.65)
            return base_score
        except:
            return 0
    return 0

google_trend["점수"] = google_trend["검색량"].apply(convert_score)

print("=====================연관어========================")

WSD = word_score["점수"].to_dict()
MWD = main_words["점수"].to_dict()
GTD = google_trend["점수"].to_dict()

Final_dict = {}
for i in WSD:
    Final_dict[i] = int(WSD[i] * 1.5)
for i in MWD:
    if i in Final_dict:
        Final_dict[i] += int(MWD[i] * 0.4)
    else:
        Final_dict[i] = int(MWD[i] * 0.4)
for i in GTD:
    if i in Final_dict:
        Final_dict[i] += int(GTD[i] * 0.2)
    else:
        Final_dict[i] = int(GTD[i] * 0.1)
Final_dict["대통령"] = int(Final_dict["대통령"]/4)
Final_dict["경제"] = int(Final_dict["경제"]/3)
Final_dict["재난"] = int(Final_dict["재난"]/1.3)
Final_dict["서울특별시"] = int(Final_dict["서울특별시"]/1.3)
Final_dict["의원"] = int(Final_dict["의원"]/1.3)
Final_dict["교육"] = int(Final_dict["교육"]/2)
Final_dict["사업"] = int(Final_dict["사업"]/1.3)
Final_dict["특검"] = int(Final_dict["특검"]/1.3)
Final_dict["정부"] = int(Final_dict["정부"]/1.3)
Final_dict["응원"] = int(Final_dict["정부"]/1.3)
Final_dict["교"] = 0
Final_dict["무릎"] = int(Final_dict["무릎"]/2)
Final_dict["계획"] = int(Final_dict["계획"]/1.5)
Final_dict["이번"] = int(Final_dict["이번"]/1.5)
Final_dict["후원"] = int(Final_dict["후원"]/1.5)
Final_dict["스페셜"] = int(Final_dict["스페셜"]/2)
Final_dict["수사"] = int(Final_dict["수사"]/5)
Final_dict["대해"] = 0
Final_dict["요구"] = 0
Final_dict["조사"] = int(Final_dict["조사"]/4)


Final_dict["공감"] = int(Final_dict["공감"]/1.5)
Final_dict["확대"] = int(Final_dict["확대"]/1.5)
Final_dict["상품권"] = int(Final_dict["상품권"]/1.5)
Final_dict["홍기"] = int(Final_dict["홍기"]/1.5)
Final_dict["지원"] = int(Final_dict["지원"]/1.5)
Final_dict["전체"] = int(Final_dict["전체"]/1.5)

Final_dict["검색어"] = 0
Final_dict["금지"] = 0
Final_dict["전체"] = int(Final_dict["전체"]/1.5)

Final_dict["사용"] = 0
Final_dict["이용"] = 0
Final_dict["수집"] = 0
Final_dict["기능"] = 0
Final_dict["글자"] = 0
Final_dict["설정"] = 0
Final_dict["스팸성"] = 0
Final_dict["방지"] = 0
Final_dict["크기"] = 0
Final_dict["게시"] = 0
Final_dict["시"] = 0
Final_dict["두"] = 0
Final_dict["교"] = 0 
Final_dict["프레"] = 0
Final_dict["시안"] = 0
Final_dict["키"] = 0
Final_dict["중이"] = 0
Final_dict["길"] = 0
Final_dict["달"] = 0

Final_dict["대표"] = int(Final_dict["대표"]/1.5)
Final_dict["사회"] = int(Final_dict["사회"]/1.5)
Final_dict["관련"] = int(Final_dict["관련"]/1.5)
Final_dict["이상"] = int(Final_dict["이상"]/1.5)
Final_dict["전체"] = int(Final_dict["전체"]/1.5)  # 재확인용
Final_dict["정책"] = int(Final_dict["정책"]/1.5)
Final_dict["시설"] = int(Final_dict["시설"]/1.5)
Final_dict["평가"] = int(Final_dict["평가"]/1.5)
Final_dict["대상"] = int(Final_dict["대상"]/1.5)
Final_dict["기준"] = int(Final_dict["기준"]/1.5)
Final_dict["문화"] = int(Final_dict["문화"]/1.5)
Final_dict["운영"] = int(Final_dict["운영"]/1.5)
Final_dict["가구"] = int(Final_dict["가구"]/1.5)
Final_dict["기획"] = int(Final_dict["기획"]/1.5)
Final_dict["활용"] = int(Final_dict["활용"]/1.5)
Final_dict["요구"] = int(Final_dict["요구"]/1.5)
Final_dict["목적"] = int(Final_dict["목적"]/1.5)
Final_dict["공개"] = int(Final_dict["공개"]/1.5)
Final_dict["계좌"] = int(Final_dict["계좌"]/1.5)
Final_dict["세계"] = int(Final_dict["세계"]/1.5)
Final_dict["시민"] = int(Final_dict["시민"]/1.5)
Final_dict["특검"] = int(Final_dict["특검"]/2)
Final_dict["대표"] = 0

Final_dict["조사"] = int(Final_dict["조사"] / 1.5)
Final_dict["응원"] = int(Final_dict["응원"] / 2)  
Final_dict["악수"] = int(Final_dict["악수"] / 2)
Final_dict["스페셜"] = int(Final_dict["스페셜"] / 3)  
Final_dict["청소년"] = int(Final_dict["청소년"] / 1.5)
Final_dict["서울특별시"] = int(Final_dict["서울특별시"] / 2)  
Final_dict["의원"] = int(Final_dict["의원"] / 2) 
Final_dict["개인정보"] = 0
Final_dict["신문"] = int(Final_dict["신문"] / 1.5)
Final_dict["지원"] = int(Final_dict["지원"] / 2) 
Final_dict["연설"] = int(Final_dict["연설"] / 1.5)
Final_dict["빌딩"] = int(Final_dict["빌딩"] / 3) 
Final_dict["전국"] = int(Final_dict["전국"] / 3)  

Final_dict["사회"] = int(Final_dict["사회"] / 2)
Final_dict["정책"] = int(Final_dict["정책"] / 2)
Final_dict["사업"] = int(Final_dict["사업"] / 2)
Final_dict["대표"] = int(Final_dict["대표"] / 1.5)
Final_dict["국민"] = int(Final_dict["국민"] / 1.5)
Final_dict["대상"] = int(Final_dict["대상"] / 1.5)
Final_dict["세계"] = int(Final_dict["세계"] / 1.5)
Final_dict["관련"] = int(Final_dict["관련"] / 2)
Final_dict["전체"] = int(Final_dict["전체"] / 2)
Final_dict["계획"] = int(Final_dict["계획"] / 2)
Final_dict["확대"] = int(Final_dict["확대"] / 1.5)

Final_dict["기능"] = int(Final_dict["기능"] / 3)
Final_dict["사용"] = int(Final_dict["사용"] / 3)
Final_dict["설정"] = int(Final_dict["설정"] / 3)
Final_dict["글자"] = int(Final_dict["글자"] / 3)
Final_dict["크기"] = int(Final_dict["크기"] / 3)
Final_dict["게시"] = int(Final_dict["게시"] / 3)
Final_dict["프레"] = int(Final_dict["프레"] / 3)
Final_dict["시안"] = int(Final_dict["시안"] / 3)
Final_dict["스팸성"] = int(Final_dict["스팸성"] / 3)
Final_dict["방지"] = int(Final_dict["방지"] / 3)

Final_dict["연설"] = int(Final_dict["연설"] / 2)
Final_dict["청소년"] = int(Final_dict["청소년"] / 2)
Final_dict["빌딩"] = int(Final_dict["빌딩"] / 2)
Final_dict["시설"] = int(Final_dict["시설"] / 2)
Final_dict["신문"] = int(Final_dict["신문"] / 2)
Final_dict["내란"] = int(Final_dict["신문"] / 3)
Final_dict["치료"] = int(Final_dict["치료"] / 4)
Final_dict["지급"] = int(Final_dict["지급"] / 4)

common_words = [
    "서울", "서울시", "서울특별시", "정부", "국회", "국민", "정치", "경제", "사회",
    "교육", "산업", "기업", "국가", "정책", "청년", "시민", "경찰", "병원", "시간", "사업",
    "사업자", "관련", "정보", "제도", "조사", "시대", "시설", "공감", "지원", "계획", "대표",
    "세계", "문화", "활용", "기준", "대상", "도시", "국내", "정책", "입장", "내용", "결과", "행사"
]

for word in common_words:
    if word in Final_dict:
        Final_dict[word] = int(Final_dict[word] / 3) 

generic_words = [
    "이번", "이상", "단계", "가장", "힘", "정보", "내용", "사실", "제공", "시간",
    "참여", "건", "일", "새", "기획", "추가", "확인", "활동", "사람", "모두", "전환", "시장"
]

for word in generic_words:
    if word in Final_dict:
        Final_dict[word] = int(Final_dict[word] / 3)

selective_words = [
    "검찰", "법원", "청소년", "연설", "출석", "출범", "기각", "소환", "기자", "인터넷",
    "연구", "기관", "위원회", "복지", "사고", "경기", "전쟁", "사건", "발표", "문제", "내용", "수사"
]

for word in selective_words:
    if word in Final_dict:
        Final_dict[word] = int(Final_dict[word] / 3)
        

output = pd.DataFrame(list(Final_dict.items()), columns=['단어', '점수'])

output  = output.sort_values(by='점수', ascending=False)

output.to_csv("트렌드_점수_결과.csv", index=False, encoding='utf-8-sig')


file_name = "트렌드_점수_결과.json"

with open(file_name, "w", encoding="utf-8") as f:
    json.dump(Final_dict, f, ensure_ascii=False, indent=2)