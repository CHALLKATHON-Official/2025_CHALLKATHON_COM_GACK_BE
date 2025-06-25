import feedparser
import requests
from bs4 import BeautifulSoup
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

def take_txt(rss_url):
    feed = feedparser.parse(rss_url)
    def get_article_text(url): #기사의 링크만 가져오기 목적
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.find("div", {"class": "article_content"})
        return content.get_text(strip=True) if content else "본문 없음"

    articlesS = []
    for entry in feed.entries[:15]:  # 최신 10개만

        url = entry.link
        articlesS.append(url)
        time.sleep(0.5)
#articlesS에 객체 형태로 저장되어있음! => url 접근키는 .url
    articles = []
    for i in range(len(articlesS)):
        articles.append(articlesS[i])
    def get_article_textK(url):
        # 크롬 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 브라우저 안 띄우기
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # 크롬드라이버 경로 설정 (필요 시 수정)
        chrome_driver_path = "chromedriver.exe"  # 혹은 절대경로로 지정

        # 웹 드라이버 시작
        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(url)
            time.sleep(0.5)  # 페이지 로딩 대기

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # 여러 기사 구조 대응 (article, div, id/class 등)
            candidates = [
                {"tag": "article"},
                {"tag": "div", "attrs": {"id": "articleBody"}},
                {"tag": "div", "attrs": {"class": "news_body"}},
                {"tag": "div", "attrs": {"class": "article"}}
            ]

            for cand in candidates:
                if "attrs" in cand:
                    content = soup.find(cand["tag"], cand["attrs"])
                else:
                    content = soup.find(cand["tag"])
                if content:
                    text = content.get_text(separator="\n", strip=True)
                    if len(text) > 300:  # 짧은 광고 등 걸러냄
                        return text

            # fallback: 모든 <p> 태그 합치기
            paragraphs = soup.find_all("p")
            all_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
            return all_text if all_text else "본문 텍스트를 찾을 수 없습니다."

        finally:
            driver.quit()

    sep_text = []
    # 예시 실행
    if __name__ == "__main__":
        for i in articlesS:
            article_text = get_article_textK(i)
            sep_text.append(article_text)
        return sep_text
Arcs = []
Arcs.append(take_txt("https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml"))
Arcs.append(take_txt("http://rss.donga.com/total.xml"))
Arcs.append(take_txt("https://news.kbs.co.kr/include/aispeaker/rss/radioNews_g.xml"))
Arcs.append(take_txt("http://www.khan.co.kr/rss/rssdata/total_news.xml"))
Arcs.append(take_txt("https://www.pressian.com/api/v3/site/rss/news"))





#여기부터 단어 분석 시작!  [250624]

# Oenaddressing - linear probing 과제에서 작성한 해시테이블 클래스 작성할 것!
class HashOpenAddr:
    def __init__(self, size):
        global collision
        self.size = size
        self.keys = [None]*self.size
        self.values = [None]*self.size

    def __str__(self):
        s = ""
        for k in self:
            if k == None:
                t = "{0:5s}|".format("")
            else:
                t = "{0:-5d}|".format(k)
            s = s + t
        return s

    def __iter__(self):
        for i in range(self.size):
            yield self.keys[i]
                    
    def hash_function(self, key):
        key = hash(key)
        # 이 과제에서는 단순한 함수 사용: h(key) = key % self.size
        return key % self.size
            
    def find_slot(self, key):
        global collision
        loc = self.hash_function(key)
        k = loc
        while True:
            collision += 1
            if (self.keys[k] == None) or (self.keys[k] == key): #빈 칸이거나/key값 그대로 들어있다면, index를 return
                return k
            k = (k+1) % self.size
            if k == loc: #한 바퀴 다 돌았다면, None (빈 칸 없고, key도 없음)
                return None

    def set(self, key, value=None):
        k = self.find_slot(key)
        if k == None:
            return None
        self.keys[k] = key
        self.values[k] = value
        return k

    def remove(self, key): #i는 삽입 위치/j는 삽입 대상 위치/k는 해쉬값
        i = self.find_slot(key)
        if i == None or self.keys[i] != key:
            return False
        j = i
        while True:
            self.keys[i] = None
            self.values[i] = None
            while True:
                j = (j+1) % self.size
                if self.keys[j] == None: #이어진 칸이 없다면, 종료 (유일한 출구)
                    return key
                k = self.hash_function(self.keys[j])
                if not(i<k<=j or j<i<k or k<=j<i): #이동 불가인 j 등장. 해당 이후는 반드시 불가능 하므로 break
                    break #k=j의 의미는 올바른 위치에 있다는 의미이므로 not에 포함됨
            self.keys[i] = self.keys[j]
            self.values[i] = self.values[j]
            i = j #옮긴 j에서 다시 시작

    def search(self, key):
        i = self.find_slot(key)
        if self.keys[i] == key:
            return self.values[i]
        else: 
            return None

    def __getitem__(self, key):
        return self.search(key)
    def __setitem__(self, key, value):
        self.set(key, value)
# ---------------------------------------해쉬테이블

    

# 텍스트 전처리 (특수문자, 구두점 등 불필요한 심볼 제거)
def preprocess_text(text: str,language) -> list[str]:
    if language == "한국어":
        okt = Okt()
        nouns = okt.nouns(text)  # 명사만 추출
        return nouns

# 단어 빈도 계산 (작성할 것!)


import string
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
from konlpy.tag import Okt
from PIL import Image
import numpy as np

collision = 0

# Oenaddressing - linear probing 과제에서 작성한 해시테이블 클래스 작성할 것!
class HashOpenAddr:
    def __init__(self, size):
        global collision
        self.size = size
        self.keys = [None]*self.size
        self.values = [None]*self.size

    def __str__(self):
        s = ""
        for k in self:
            if k == None:
                t = "{0:5s}|".format("")
            else:
                t = "{0:-5d}|".format(k)
            s = s + t
        return s

    def __iter__(self):
        for i in range(self.size):
            yield self.keys[i]
                    
    def hash_function(self, key):
        key = hash(key)
        # 이 과제에서는 단순한 함수 사용: h(key) = key % self.size
        return key % self.size
            
    def find_slot(self, key):
        global collision
        loc = self.hash_function(key)
        k = loc
        while True:
            collision += 1
            if (self.keys[k] == None) or (self.keys[k] == key): #빈 칸이거나/key값 그대로 들어있다면, index를 return
                return k
            k = (k+1) % self.size
            if k == loc: #한 바퀴 다 돌았다면, None (빈 칸 없고, key도 없음)
                return None

    def set(self, key, value=None):
        k = self.find_slot(key)
        if k == None:
            return None
        self.keys[k] = key
        self.values[k] = value
        return k

    def remove(self, key): #i는 삽입 위치/j는 삽입 대상 위치/k는 해쉬값
        i = self.find_slot(key)
        if i == None or self.keys[i] != key:
            return False
        j = i
        while True:
            self.keys[i] = None
            self.values[i] = None
            while True:
                j = (j+1) % self.size
                if self.keys[j] == None: #이어진 칸이 없다면, 종료 (유일한 출구)
                    return key
                k = self.hash_function(self.keys[j])
                if not(i<k<=j or j<i<k or k<=j<i): #이동 불가인 j 등장. 해당 이후는 반드시 불가능 하므로 break
                    break #k=j의 의미는 올바른 위치에 있다는 의미이므로 not에 포함됨
            self.keys[i] = self.keys[j]
            self.values[i] = self.values[j]
            i = j #옮긴 j에서 다시 시작

    def search(self, key):
        i = self.find_slot(key)
        if self.keys[i] == key:
            return self.values[i]
        else: 
            return None

    def __getitem__(self, key):
        return self.search(key)
    def __setitem__(self, key, value):
        self.set(key, value)
# ---------------------------------------해쉬테이블 Arcs에 5개씩 5개 들어있음! 

# 텍스트 전처리 (특수문자, 구두점 등 불필요한 심볼 제거)
def preprocess_text(text: str,language) -> list[str]:
    if language == "한국어":
        okt = Okt()
        nouns = okt.nouns(text)  # 명사만 추출
        return nouns

# 단어 빈도 계산 (작성할 것!)
def count_words(words: list[str], stop_words: set[str], start_rank: int, end_rank: int) -> dict[str, int]:
    # 1. words 리스트의 단어의 빈도수를 HashOpenAddr 객체를 만들어 센다
    # 2. start_rank부터 end_rank까지의 단어와 빈도수만 저장된 dict 자료구조 selected_words를 리턴한다
    H = HashOpenAddr(20000)
    for word in words:
        k = H.search(word)
        if k == None:
            H.set(word,1)
        else:
            H.set(word,k+1)
    rank = []
    for i in range(20000):
        key = H.keys[i]
        val = H.values[i]
        if key in stop_words:
            continue
        if val != None:
            rank.append((key,val))
    
    rank.sort(key = lambda x:x[1], reverse=True)
    select = rank[start_rank-1:end_rank]
    selected_words = dict(select)
    return selected_words,len(rank)

# Main 함수
def play() -> None:
    start_rank = 1
    end_rank = 200
    language = "한국어"
    
    # stopwords 설정 및 추가
    stop_words = set(['고','중','스','씨','은','는','나','너','가','요','다',
    '습니다','의','측','과','것','이','및','때','제','위','안','바','그',
    '수','기타','정','폭','때문','등','더','주','라며','또',
    '로','매우','뒤','율','날','곳','전','저','후','말','며','도','지금','당시','약','이후','팀','남','회','로서','순','년','장','관'
    ,'명','최근','지난','이후','통해','탁','단','김용','기자','사','돔','루','역사상','임','뉴스','섹터','구독','를','임','공유','복사'
    ,'창','방','사사건건','퍼','가기','국','꼭','인','중계방송','크랩','위해','도움말','모습','방송','무','짝','부','재방송',
    '톡','살','뉴스라인','센터','선','타이어','세','넥센','김','김','스포츠조선','개','맷','붙여넣기','등록','편집','내','맘','댓글','닉네임','추천',
    '입력','재','기사','회원','전화번호','주소','일자','번호','신청','배포','텍스트','클릭','쏙','골프'])
    counted_text = []
    sizeof_text = []

    for i in range(len(Arcs)):
        for j in range(len(Arcs[i])):
            words = preprocess_text(Arcs[i][j], language)
            song, kim = count_words(words, stop_words, start_rank, end_rank)
            # song은 dict → value 기준으로 내림차순 정렬
            if len(song) <10:
                continue
            sorted_song = dict(sorted(song.items(), key=lambda item: item[1], reverse=True))
            counted_text.append(sorted_song)
            sizeof_text.append(kim)

    return counted_text, sizeof_text


T, S = play() #각 크기에 맞게 점수화 하기
word_score = {}

now = 0
for i in T:
    for j in i:
        if j in word_score:
            word_score[j] += int((i[j]/S[now]*1000))
        else:
            word_score[j] = int((i[j]/S[now]*1000))
    now+=1
# 딕셔너리 정렬 (원본)
sorted_word_score = dict(sorted(word_score.items(), key=lambda item: item[1], reverse=True))
print(sorted_word_score)  # 75개의 기사가 합쳐진 score

# 딕셔너리를 DataFrame으로 변환
df_score = pd.DataFrame(list(sorted_word_score.items()), columns=['단어', '점수'])

# 특정 단어 점수 조정
adjustments = {
    "서울특별시": -700,
    "서울": -600,
    "수집": -440,
    "이용": -410,
    "키": -400,
    "사용": -400,
    "기능": -390,
    "응원": -300,
    "공감": -390,
    "금지": -386,
    "방지": -360,
    "스팸성": -360,
    "검색어": -350,
    "크기": -360,
    "게시": -350,
    "설정": -350,
    "글자": -340,
    "프레": -250,
    "시안": -250,
    "응답": -200,
    "맞춤": -250,
    "한국": -100,
    "만": -130,
    "강": -130,
    "향": -130,
    "지역": -160,
}

# 적용
for word, delta in adjustments.items():
    if word in df_score['단어'].values:
        df_score.loc[df_score['단어'] == word, '점수'] += delta
    else:
        print(f"단어 '{word}'는 데이터에 존재하지 않음")

# 조정 후 점수 기준으로 다시 정렬
df_score = df_score.sort_values(by="점수", ascending=False)

# 저장
df_score.to_csv("단어점수.csv", index=False, encoding='utf-8-sig')
print("저장 완료: 단어점수.csv (정렬 포함)")


#여기서부터 연관어 처리!

#T는 데이터 세트 (5칸짜리 리스트 내 15개씩 딕셔너리(단어개수 분석됨)이 들어있다.) S는 총 개수(여기서 의미 없을듯)
def Related_words():
    rel_list = []
    for i in range(len(T)):
        str_only = {k: v for k, v in T[i].items() if isinstance(k, str)}
        sorted_dict = sorted(str_only.items(), key=lambda item: item[1], reverse=True)
        rel_list.append(sorted_dict[:5])  # (key, value) 쌍 그대로 저장
    return rel_list

    return rel_list
print(Related_words())

# 관련 단어 리스트 가져오기
related_list = Related_words()  # [(단어, 점수), ...] 리스트가 여러 개

# 행 구성
rows = []
for group in related_list:
    row = []
    for word, score in group:
        row.extend([word, score])
    # 5개 미만일 경우 빈 칸 채움 (안전하게)
    while len(row) < 10:
        row.extend(["", ""])
    rows.append(row)

# 열 이름 생성
columns = []
for i in range(1, 6):
    columns.append(f'연관단어{i}')
    columns.append(f'점수{i}')

# 데이터프레임 생성 및 저장
df_related = pd.DataFrame(rows, columns=columns)
df_related.to_csv("연관단어점수.csv", index=False, encoding='utf-8-sig')
