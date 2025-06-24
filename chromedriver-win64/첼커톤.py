from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_article_text(url):
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
        time.sleep(2)  # 페이지 로딩 대기

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 여러 기사 구조 대응 (article, div, id/class 등)
        candidates = [
            {"tag": "article"},
            {"tag": "div", "attrs": {"id": "articleBody"}},
            {"tag": "div", "attrs": {"class": "news_body"}},
            {"tag": "div", "attrs": {"class": "article"}},
        ]

        for cand in candidates:
            if "attrs" in cand:
                content = soup.find(cand["tag"], cand["attrs"])
            else:
                content = soup.find(cand["tag"])
            if content:
                text = content.get_text(separator="\n", strip=True)
                if len(text) > 200:  # 짧은 광고 등 걸러냄
                    return text

        # fallback: 모든 <p> 태그 합치기
        paragraphs = soup.find_all("p")
        all_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return all_text if all_text else "본문 텍스트를 찾을 수 없습니다."

    finally:
        driver.quit()

# 예시 실행
if __name__ == "__main__":
    all_text = " "
    for i in range(3):
        url = input("기사 URL을 입력하세요: ")
        article_text = get_article_text(url)
        all_text += article_text
    print(all_text)
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
# ---------------------------------------해쉬테이블

    
# 텍스트 파일 읽기
def read_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    return text

# 텍스트 전처리 (특수문자, 구두점 등 불필요한 심볼 제거)
def preprocess_text(text: str,language) -> list[str]:
    if language == "영어":
        text = re.sub(r'[^a-zA-z\s]','', text)
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator).split()
    elif language == "한국어":
        okt = Okt()
        nouns = okt.nouns(text)  # 명사만 추출
        return nouns

# 단어 빈도 계산 (작성할 것!)
def count_words(words: list[str], stop_words: set[str], start_rank: int, end_rank: int) -> dict[str, int]:
    # 1. words 리스트의 단어의 빈도수를 HashOpenAddr 객체를 만들어 센다
    # 2. start_rank부터 end_rank까지의 단어와 빈도수만 저장된 dict 자료구조 selected_words를 리턴한다
    H = HashOpenAddr(17000)
    for word in words:
        k = H.search(word)
        if k == None:
            H.set(word,1)
        else:
            H.set(word,k+1)
    rank = []
    for i in range(17000):
        key = H.keys[i]
        val = H.values[i]
        if key in stop_words:
            continue
        if val != None:
            rank.append((key,val))
    
    rank.sort(key = lambda x:x[1], reverse=True)
    print(len(rank))
    select = rank[start_rank-1:end_rank]
    selected_words = dict(select)
    return selected_words

# Word Cloud 생성 및 출력
def generate_wordcloud(freq_dict: dict[str, int]) -> None:
    mask = np.array(Image.open(input("이미지파일명: ")))
    wordcloud = WordCloud(width=800, height=800, background_color='white',mask = mask)
    wordcloud.generate_from_frequencies(freq_dict)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Main 함수
def play() -> None:
    language = "한국어"
    if language == "영어":
        text = read_file(input("텍스트 파일명: "))  # 파일명을 적절히 변경
        words = preprocess_text(text,language)
        
        # stopwords 설정 및 추가
        stop_words = set(stopwords.words('english'))
        stop_words.update(['ye', 'said', 'll', 'the', 'thus', 'ay', 'till', 'whose', 'which', 'that', 'mine', 'let', 
        'thy', 'thee', 'that', 'upon', 'say', 'go', 'tis', 'st', 'us', 'one', 'will', 'thou', 'though', 'now', 
        'well', 'may', 'might', 'yet', 'much', 'must', 'way', 'long', 'sir', 'come', 'hath', 'shall','a','and','to','was','of','you','i'])

        # 랭킹 범위 입력 (예: 1위~200위: 자연수 입력)
        start_rank = int(input("시작 랭킹 입력: "))
        end_rank = int(input("끝 랭킹 입력: "))

        selected_words = count_words(words, stop_words, start_rank, end_rank)
        generate_wordcloud(selected_words)
        print(collision)

    elif language == "한국어":
        text = all_text  # 파일명을 적절히 변경
        
        # stopwords 설정 및 추가
        stop_words = set(['은','는','나','너','가','요','다','습니다','의','측','과','것','이','및','때','제','위','안','바','그','수','기타','정'])
        words = preprocess_text(text,language)
        # 랭킹 범위 입력 (예: 1위~200위: 자연수 입력)
        start_rank = int(input("시작 랭킹 입력: "))
        end_rank = int(input("끝 랭킹 입력: "))

        selected_words = count_words(words, stop_words, start_rank, end_rank)
        mask = np.array(Image.open(input("이미지파일명: ")))
        wordcloud = WordCloud(
            font_path='C:/Windows/Fonts/malgun.ttf',  #한글 폰트 위치 찾기 , wordcloud객체
            width=800,
            height=800, #크기지정
            background_color='white', #배경색
            mask = mask
        ).generate_from_frequencies(selected_words) #이 dict를 기반으로 생성 (객체생성 + 데이터 입력)

        plt.figure(figsize=(10, 10)) #그래프 크기와 관련
        plt.imshow(wordcloud) #imshow는 이미지를 띄우는 함수 (필수)
        plt.axis('off') #axis 필요 없음
        plt.show() #matplotlib을 사용..


play()