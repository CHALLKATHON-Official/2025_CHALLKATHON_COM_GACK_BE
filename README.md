# 2025_CHALLKATHON_-COM_GACK-_-BE-
6월 23일 회의내용
결과

1. 홈페이지 진입 시 비주얼/UX
‘2025년이 몇 % 지났다’
→ 상단(혹은 배경)에서 진행 바(progress bar) 혹은 움직이는 숫자로 시각화.
→ “2025년의 몇 %가 흘렀다”는 메시지와, 현재 날짜/시간을 함께 보여주는 것이 직관적.
→ 단순 숫자, 바, 혹은 물 흐르는 듯한 애니메이션(파티클)이 움직이며 시간의 흐름을 강조.

단어가 물 흐르듯 움직임
→ 워드클라우드 기반 애니메이션.
→ 각 단어는 “2025년 트렌드”로 선정된 키워드(예: AI, 저출산, 인플레이션, K-POP 등)로 구성.
→ 단어 크기는 영향력(검색량, 노출량, 소셜 언급량 등) 기반, 위치는 랜덤+부드러운 파도형 움직임.
→ UI적으로는 WebGL, Canvas, 혹은 D3.js 애니메이션 활용.

최신 트렌드 단어 강조
→ 홈 하단 혹은 오버레이로, “지금 가장 많이 언급되는 단어”를 최근 24시간/7일 기준으로 따로 큰 크기와 효과로 표시.

2. 상호작용(인터랙션) 디자인
단어를 ‘이동’시키면(끌어다 놓기 or 터치 후 드래그)
→ 그 단어와 논리적/연관성이 큰 단어(연관 검색어, 토픽 코사인 유사도 기반 등)를 연결선/하이라이트로 시각화.
→ 해당 단어를 중심으로, 주변 단어 영향력이 동적으로 변화(ex: 크기 증가, 색상 강조).
→ 추가 UX: 단어 옆에 “+”버튼을 누르면 연관 단어 클러스터가 펼쳐짐.

단어 클릭 시
→ 해당 단어의 나무위키 페이지로 새 창/탭 연결.
→ B급 감성: 클릭 시 애니메이션 효과(예: 뒤집히는 카드, 미묘한 밈 효과, 잡담/유머 메시지 팝업) 추가 가능.

3. 트렌드 기간/범위 설정
기간 필터
→ 상단/하단/사이드바에서 년/월/일 단위로 기간 범위 슬라이더 또는 달력 컴포넌트 제공.
→ 특정 연도를 선택하면, 그 해에 이슈였던 트렌드 단어들이 빠르게 변화하는 애니메이션(예: timeline scrub)으로 순식간에 바뀜.
→ 예: 2019년→2025년 빠르게 돌리면, 단어들의 등장/퇴장/크기변화가 타임랩스처럼 연출.

4. 단어 영향력 시각화
크기
→ 단어의 크기로 영향력(빈도, 언급량 등) 표현
→ 동일 크기 내에서는 색, 투명도, 애니메이션 속도 등으로 “급상승”, “장기 유지”, “폭락” 등 특성을 추가로 시각화할 수 있음.

5. 부가 요소 및 보완점
‘올해가 몇 % 지났나’ 정보
→ 날짜와 함께 노출: ‘2025년 6월 23일 기준, 올해는 49.5% 지났습니다’
→ Progress bar 또는 물결 애니메이션
→ 날짜별로 “최근 갑자기 많이 검색된 해(년도)” 추천은 부가 기능 정도로, 클릭 시 해당 연도로 타임슬라이드 이동.

데이터 신뢰성/출처 표시
→ 트렌드 데이터는 어디서, 어떤 방식(검색량, 뉴스, 커뮤니티 등)으로 수집했는지 명확하게 표기 필요.
→ 크롤링/AI 분석 등으로 부족할 경우, “이 사이트는 실험적/재미용”임을 명시해 책임 회피 필요.

논리적 오류 및 UX 위험성

**“단어 이동=연관 단어 변화”**에서, 임의 이동이 아니라 “드래그 후 drop”일 때만 영향력이 변하는 게 명확해야 함.

단순 클릭, 드래그 모두에 반응한다면 혼란/불편이 될 수 있음.

“B급 감성”은 어디까지나 UI/UX의 세부 디테일(컬러, 폰트, 이스터에그 등)로 구현해야 하고, 사용성 저해하면 안 됨.

6. 정리/전체 구조
메인화면

2025년 진행도(상단 progress bar)

트렌드 단어 워드클라우드 (물결 애니메이션)

최신 트렌드(오늘/이번주) 강조 영역

상호작용

단어 클릭: 나무위키(B급 연출)

단어 드래그/이동: 연관 단어 강조/확장, 영향력 시각적 변화

기간/연도 필터

연/월/일 슬라이더 → 애니메이션 기반 트렌드 변화 보기

부가정보

데이터 출처, 올해 % 진행 정보, 연도별 검색량 급증 추천 등

부족한 점 및 보완 제안
데이터 품질: 신뢰성 높은 데이터 소스 확보/명시 필요. 실시간 반영이 어렵다면, ‘샘플’ 데이터 혹은 AI 기반 예측 추가.

접근성: 애니메이션 과다로 사용성이 떨어질 위험, 텍스트/다크모드/저사양 옵션 제공 필요.

기술 검토: WebGL 등 무거운 기술은 최적화 필수.

서버/크롤링: 과거 트렌드, 실시간 데이터 반영 로직 구체화 필요(예: Naver, Google, Twitter API 등).

법적 이슈: 데이터 사용 정책, 나무위키 연동 관련 이용약관 등 체크 필요.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_article_text(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 안 띄우기
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_driver_path = "chromedriver.exe" 


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

        paragraphs = soup.find_all("p")
        all_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return all_text if all_text else "본문 텍스트를 찾을 수 없습니다."

    finally:
        driver.quit()

sep_text = []*6
if __name__ == "__main__":
    all_text = " "
    urls = ["https://www.chosun.com/","https://www.joongang.co.kr/","https://www.donga.com/","https://www.khan.co.kr/","https://www.pressian.com/","https://news.kbs.co.kr/news/pc/main/main.html"]
    #보수3 진보2 KBS(공영)1
    for i in range(6):
        print(i)
        url = urls[i] #여기에 이제, 신문사들의 main 홈페이지가 들어갈 예정
        article_text = get_article_text(url)
        all_text += article_text
        sep_text.append(article_text)
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
    ,'명','최근','지난','이후','통해','방','앱','무','치','단','재','응','세','또','또한','속보','셀','사회','향','이유','경향신문'
    , '기', '자', '해', '여러', '후회', '주중', '즉시','주제','강연서','언급','팩','황','다른','종합','준','순식간','얼마나','개월','첫','달'])
    counted_text = []
    sizeof_text = []

    for i in range(6):
        words = preprocess_text(sep_text[i],language)
        song,kim = count_words(words, stop_words, start_rank, end_rank)
        counted_text.append(song)
        sizeof_text.append(kim)
    words = {}
    for i in range(6):
        for j in counted_text[i]:
            if j in words:
                words[j] += int(counted_text[i][j] / sizeof_text[i]*10000)
            else:
                words[j] = int(counted_text[i][j] / sizeof_text[i]*10000)
        #저장 부분
    import pandas as pd
    df = pd.DataFrame(list(words.items()), columns=["단어", "점수"])
    df = df.sort_values(by="점수", ascending=False)  # 점수 기준 내림차순 정렬

    df.to_csv("신문사메인단어0626_1328.csv", index=False, encoding="utf-8-sig")
    print(words)

play()





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
        print(url)
        return content.get_text(strip=True) if content else "본문 없음"

    articlesS = []
    for entry in feed.entries[:15]:  # 최신 10개만

        url = entry.link
        articlesS.append(url)
        time.sleep(0.1)
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
            time.sleep(0.1)  # 페이지 로딩 대기

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
    '입력','재','기사','회원','전화번호','발행','구','새','액','주소','호','워드','학습','선정','무단','일자','번호','신청','배포','텍스트','클릭','쏙','골프'])
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
    "우려" : -200,
    "남성" : -200,
    "여성" : -200,
    "혐의" : -200,
    "대한민국" : -200,
    "서대문구" : -500,
    "종로구" : -500,
    "수집" : -500,
    "충정로" : -500,
    "검색어" : -400,
    "청계천로" : -500
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
df_score.to_csv("단어점수0626_1333.csv", index=False, encoding='utf-8-sig')
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
df_related.to_csv("연관단어점수0626_1333.csv", index=False, encoding='utf-8-sig')





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

# 정확한 경로 (확장자 .csv 주의!)
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
    Final_dict[i] = int(WSD[i] * 1)
for i in MWD:
    if i in Final_dict:
        Final_dict[i] += int(MWD[i] * 0.3)
    else:
        Final_dict[i] = int(MWD[i] * 0.3)
for i in GTD:
    if i in Final_dict:
        Final_dict[i] += int(GTD[i] * 0.5)
    else:
        Final_dict[i] = int(GTD[i] * 0.5)







penalize_words = [
    "사용", "기능", "이용", "정보", "문제", "설정", "크기", "작성", "지원", 
    "제공", "수집", "관리"
    ,"수사","경제","검토","절차","사실","거부",
    "확인", "가능", "적용", "선택", "검색", "키", "버튼"
    ,"대해","개인정보","조치","이번","스페셜","오전","무릎","둥지","예정"
    ,"요구","출석","특검","정치",'사건','사업'
]
much_words = [
    "대통령","내란","경제","수사","정부","서울","서울특별시","한국",'계획',"대한민국",'산업'
]
del_words =[
    "정보","처리","처","데","취소","건","이번","홍기","후원","시설","신문"
    ,"전국","예정","시","책","시도","처리","관련","신석호",'법','률','용','전체','기존','유지'
]

semi_words = ["윤","윤석열","특검","사업","형소법",'황새','정책','빌딩']
for i in semi_words:
    if i in Final_dict:
        Final_dict[i] = int(Final_dict[i] *0.7)
for i in penalize_words:
    if i in Final_dict:
        Final_dict[i] = int(Final_dict[i] *0.15)
for i in much_words:
    if i in Final_dict:
        Final_dict[i] = int(Final_dict[i] *0.5)
for i in del_words:
    if i in Final_dict:
        Final_dict[i] = 0

max_score = max(Final_dict.values()) #max에 의존하여 값을 모두 정규화

if max_score > 0:
    for k in Final_dict:
        Final_dict[k] = int(Final_dict[k] / max_score * 100)

period = "25-2"
category = "social"

# 변환
json_data = [
    {"word": k, "score": int(v), "period": period, "category": category}
    for k, v in Final_dict.items() if int(v) >= 15  # 원하는 조건도 필터링 가능
]

# 저장
json_path_extended = os.path.join(folder, "찐찐찐찐최종.json")
with open(json_path_extended, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)
