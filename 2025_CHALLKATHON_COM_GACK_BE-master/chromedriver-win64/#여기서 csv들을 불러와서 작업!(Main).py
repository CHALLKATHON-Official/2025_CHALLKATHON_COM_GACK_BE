import pandas as pd
import os
import re
import time
import schedule
import json
from konlpy.tag import Okt

def read_csv_file(file_path, encoding='utf-8-sig'):
    try:
        df = pd.read_csv(file_path, encoding=encoding) #index_col=0 옵션을 제거함으로써 KeyError 해결 ("트렌드"컬럼이 일반 컬럼으로 남아있게되어서 오류 발생 안함)
        print(f" {os.path.basename(file_path)} 불러오기 성공")
        return df
    except Exception as e:
        print(f" {file_path} 읽기 실패:", e)
        return None

# 정확한 경로
folder = r"C:\Users\legen\2025_CHALLKATHON_COM_GACK_BE\2025_CHALLKATHON_COM_GACK_BE-master\chromedriver-win64"
word_score = read_csv_file(os.path.join(folder, "단어점수.csv"))
rel_words = read_csv_file(os.path.join(folder, "연관단어점수.csv"))
main_words = read_csv_file(os.path.join(folder, "신문사메인단어.csv"))
google_trend = read_csv_file(os.path.join(folder, "구글트렌드.csv"))

print(word_score)
print(rel_words)
print(main_words)
print(google_trend)
#=====================================================================================================================

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 1000)

okt = Okt()

def normalize(text):
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", "", text.strip().lower())

def convert_score(value):
    if pd.isna(value) or not isinstance(value, str):
        return 0
    value = value.replace(" ", "")
    score_mapping = {
        "100+": 100, "200+": 200, "500+": 500, "1000+": 1000,
        "5000+": 5000, "1만+": 10000, "2만+": 20000,
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


def preprocess_text(text):
    return okt.nouns(text)

def count_words(words, stop_words):
    from collections import defaultdict
    freq = defaultdict(int)
    for word in words:
        if word not in stop_words:
            freq[word] += 1
    return dict(freq)

def compute_score(internal_freq, external_score, max_internal_freq):
    norm_internal = internal_freq / max_internal_freq if max_internal_freq > 0 else 0
    norm_external = min(external_score / 10000, 1.0)
    return round(0.7 * norm_internal + 0.3 * norm_external, 3)

def merge_data(internal_dict, external_list):
    merged = {}
    external_dict = {normalize(item["단어"]): item["수치점수"] for item in external_list}
    max_internal_freq = max(internal_dict.values()) if internal_dict else 1
    for word, freq in internal_dict.items():
        norm_word = normalize(word)
        ext_score = external_dict.get(norm_word, 0)
        score = compute_score(freq, ext_score, max_internal_freq)
        merged[norm_word] = score
    return merged

def extract_related_keyword_scores_expanded(df, final_scores_keys):
    related_score_dict = {}
    for main_word in final_scores_keys:
        related_words_set = set()
        main_word_norm = normalize(main_word)
        for _, row in df.iterrows():
            trend = str(row.get("트렌드", "")).strip()
            related_raw = str(row.get("트렌드 분석", "")).strip()
            trend_norm = normalize(trend)
            related_raw_norm = normalize(related_raw)

            if main_word_norm == trend_norm or main_word_norm in related_raw_norm:
                words = [w.strip() for w in related_raw.split(",") if w.strip()]
                for w in words:
                    w_norm = normalize(w)
                    # 자기 자신은 제외
                    if w_norm != main_word_norm:
                        related_words_set.add(w.replace(" ", ""))  # 공백 제거해서 저장

        related_words_list = list(related_words_set)
        score_dict = {}
        for idx, word in enumerate(related_words_list):
            score = round(max(1.0 - idx * 0.1, 0.1), 2)
            score_dict[word] = score
        related_score_dict[main_word] = score_dict
    return related_score_dict

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# 카테고리 기준 정의
def guess_category(word):
    categories = {
        "정치": ["대통령", "장관", "의원", "정부", "선거", "국회", "총선", "정권", "청와대", "병역", "예비군", "장병"],
        "경제": ["주식", "투자", "증권", "금융", "코스피", "코스닥", "경제", "부동산", "환율", "공매도", "적금", "가상화폐", "한은"],
        "스포츠": ["축구", "리그", "선수", "골", "챔피언스리그", "야구", "홈런", "KBO", "MLB", "NBA", "경기", "올림픽", "메달"],
        "연예": ["배우", "영화", "드라마", "촬영", "가수", "음악", "앨범", "콘서트", "예능", "아이돌", "연예인", "팬", "뮤직", "AI콘서트"],
        "기술": ["IT", "인공지능", "AI", "로봇", "소프트웨어", "하드웨어", "기능", "설정", "알고리즘", "코딩", "앱", "컴퓨터", "이차전지", "사용", "이용", "수집"],
        "사회": ["사건", "사회", "사고", "법원", "검찰", "경찰", "공감", "게시", "검색어", "서울", "강남", "서초", "마포", "부산", "해운대", "광안리", "화재", "실종", "재판", "폭행", "교통사고", "일타강사", "마약"],
        "과학": ["과학", "연구", "실험", "이론", "물리", "화학", "생물", "기초과학", "연구원"],
        "건강": ["의료", "병원", "건강", "질병", "백신", "감기", "코로나", "치료", "의사", "약"],
        "환경": ["환경", "기후", "지구온난화", "탄소", "에너지", "재생에너지", "오염", "미세먼지", "지진", "폭우"]
    }

    word_lower = str(word).lower().replace(" ", "")
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw.lower().replace(" ", "") in word_lower:
                return cat
    return None

#  경로 지정
file1 = r"C:\Users\legen\단어점수0625_2200.csv"
file2 = r"C:\Users\legen\단어점수0626_1333.csv"

# CSV 불러오기
df1 = pd.read_csv(file1, encoding='utf-8-sig')
df2 = pd.read_csv(file2, encoding='utf-8-sig')

# 1차 분류
df1["분류"] = df1["단어"].apply(guess_category)
df2["분류"] = df2["단어"].apply(guess_category)

# 분류되지 않은 단어 추출
etc1 = df1[df1["분류"].isna()]
etc2 = df2[df2["분류"].isna()]
etc_all = pd.concat([etc1, etc2]).reset_index(drop=True)

# 클러스터링 기반 보완 분류
vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 3))
X = vectorizer.fit_transform(etc_all["단어"].astype(str).tolist())

k = 9
kmeans = KMeans(n_clusters=k, random_state=42)
labels = kmeans.fit_predict(X)

cluster_to_category = {
    0: "기술",
    1: "사회",
    2: "정치",
    3: "경제",
    4: "건강",
    5: "연예",
    6: "환경",
    7: "스포츠",
    8: "과학"
}
etc_all["분류"] = [cluster_to_category[l] for l in labels]

#df1, df2에 결과 반영
for idx in etc_all.index:
    word = str(etc_all.loc[idx, "단어"])
    category = etc_all.loc[idx, "분류"]

    df1.loc[df1["단어"].astype(str) == word, "분류"] = category
    df2.loc[df2["단어"].astype(str) == word, "분류"] = category

#최종 저장
df1.to_csv(r"C:\Users\legen\단어점수0625_분류완료.csv", index=False, encoding='utf-8-sig')
df2.to_csv(r"C:\Users\legen\단어점수0626_분류완료.csv", index=False, encoding='utf-8-sig')

print(" 기타 없이 모든 단어 분류 완료! 두 CSV 파일에 최종 저장됨.")


def get_search_volume(norm_word, df):
    for i, trend in enumerate(df["트렌드"]):
        trend_norm = normalize(trend)
        if norm_word in trend_norm or trend_norm in norm_word:
            raw_score = df["검색량"].iloc[i]
            print(f"찾음: {norm_word} -> {raw_score}")
            return convert_score(raw_score)
    print(f"못 찾음: {norm_word}")
    return None

def play_from_google_csv():
    print("\n[실행] Google 트렌드 CSV 기반 키워드 분석 시작...")

    stop_words = set([
        '은','는','나','너','가','요','다','습니다','의','측','과','것','이','및','때',
        '제','위','안','바','그','수','기타','정','좀','더','또한','그리고',
        '알','뉴스','보기','사람','이유','대한'
    ])

    try:
        df = google_trend
    except Exception as e:
        print(f"[오류] CSV 로드 실패: {e}")
        return

    df["수치점수"] = df["검색량"].apply(convert_score)

    all_keywords = ",".join(df["트렌드 분석"].dropna())
    all_words = preprocess_text(all_keywords)
    internal_freq = count_words(all_words, stop_words)

    external_list = [
        {"단어": trend.strip(), "수치점수": score}
        for trend, score in zip(df["트렌드"], df["수치점수"])
    ]

    final_scores = merge_data(internal_freq, external_list)

    seen = set()
    sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    top_n = []
    for k, v in sorted_scores:
        if k not in seen:
            top_n.append((k, v))
            seen.add(k)

    trend_list = df["트렌드"].astype(str).tolist()
    trend_norm_list = [normalize(t) for t in trend_list]

    related_score_dict = extract_related_keyword_scores_expanded(df, [k for k, _ in top_n])

    result_list = []
    added_words = set()

    for norm_word, score in top_n:
        matched_trends = [t for t in trend_list if norm_word == normalize(t) or norm_word in normalize(t)]
        original_word = matched_trends[0] if matched_trends else norm_word

        if original_word in added_words:
            continue
        added_words.add(original_word)

        internal = internal_freq.get(original_word, 0)
        external = next((x["수치점수"] for x in external_list if normalize(x["단어"]) == norm_word), 0)
        final_score = score
        related_words = related_score_dict.get(norm_word, {})

        #여기서 카테고리 지정 (None이나 정보없음 방지)
        category_guess = guess_category(original_word)
        category_str = category_guess if category_guess else "미분류"

        result_list.append({
            "word": original_word,
            "internal_freq": internal,
            "external_score": external,
            "final_score": final_score,
            "search_volume": get_search_volume(norm_word, df),
            "related_keywords": related_words,
            "category": category_str
        })

    #상위 50개 중 유효 카테고리만 필터링
    valid_categories = {"정치", "경제", "사회", "연예", "스포츠", "기술", "건강", "환경", "과학"}
    top_50_cleaned = [
        r for r in sorted(result_list, key=lambda x: x["final_score"], reverse=True)
        if r["category"] in valid_categories
    ][:50]

    top_50_json = [{
        "word": r["word"],
        "score": round(r["final_score"], 3),
        "period": "2024",
        "category": r["category"]
    } for r in top_50_cleaned]

    #JSON 객체 1줄씩 저장
    os.makedirs("output", exist_ok=True)
    with open("output/top_50_keywords_2024.json", "w", encoding="utf-8") as f:
        for r in top_50_json:
            json_line = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
            f.write(json_line + "\n")

    print("top_50_keywords_2024.json 저장 완료 (한 줄씩 JSON 50개)")

    # 콘솔 요약 출력
    print("\n[Top 50 Keywords 요약 출력]")
    for r in top_50_json:
        print(f"word: {r['word']}, score: {r['score']}, period: {r['period']}, category: {r['category']}")

    return result_list, related_score_dict

def merge_three_scores(my_scores_dict, teammate_scores_df, news_scores_df):
    teammate_scores = {}
    for _, row in teammate_scores_df.iterrows():
        w = normalize(str(row.name))
        try:
            teammate_scores[w] = float(row.iloc[0])
        except:
            teammate_scores[w] = 0

    news_scores = {}
    for _, row in news_scores_df.iterrows():
        w = normalize(str(row.name))
        try:
            news_scores[w] = float(row.iloc[0])
        except:
            news_scores[w] = 0

    all_words = set(my_scores_dict.keys()) | set(teammate_scores.keys()) | set(news_scores.keys())
    merged_scores = {}
    for word in all_words:
        s1 = my_scores_dict.get(word, 0)
        s2 = teammate_scores.get(word, 0)
        s3 = news_scores.get(word, 0)
        merged_scores[word] = round((s1 + s2 + s3) / 3, 3)

    return merged_scores

def merge_related_keywords(my_related_dict, teammate_related_dict):
    merged_related = {}

    all_keys = set(my_related_dict.keys()) | set(teammate_related_dict.keys())
    for word in all_keys:
        rel1 = my_related_dict.get(word, {})
        rel2 = teammate_related_dict.get(word, {})

        merged_sub = {}
        all_rel_words = set(rel1.keys()) | set(rel2.keys())
        for rel_word in all_rel_words:
            score1 = rel1.get(rel_word, 0)
            score2 = rel2.get(rel_word, 0)
            merged_sub[rel_word] = round((score1 + score2) / 2, 3)

        merged_related[word] = merged_sub

    return merged_related

def run_all():
    result_list, my_related_dict = play_from_google_csv()

    teammate_related_dict = {}  # 팀원 연관단어 있으면 넣기

    my_scores_dict = {normalize(r['word']): r['final_score'] for r in result_list}

    merged_scores = merge_three_scores(my_scores_dict, word_score, main_words)

    merged_related = merge_related_keywords(my_related_dict, teammate_related_dict)

    print("\n[통합 점수 전체 출력]")
    for w, s in sorted(merged_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"{w}: {s}")


    os.makedirs("output", exist_ok=True)
    pd.DataFrame([{"word": w, "merged_score": s} for w, s in merged_scores.items()])\
        .to_csv("output/merged_scores.csv", index=False, encoding="utf-8-sig")

    with open("output/merged_related_keywords.json", "w", encoding="utf-8") as f:
        json.dump(merged_related, f, ensure_ascii=False, indent=2)

    print("[완료] 병합 결과 저장 완료!")

def save_top50_keywords_by_category(df1, df2):
    import json, os

    print("[실행] 상위 50 키워드 카테고리별 저장 시작...")

    # 1. 두 개 데이터프레임 합치기
    merged_df = pd.concat([df1, df2], ignore_index=True)

    # 2. 점수 정리
    merged_df["점수"] = pd.to_numeric(merged_df["점수"], errors="coerce").fillna(0)
    merged_df = merged_df.sort_values(by="점수", ascending=False)

    # 3. 유효 카테고리만 추출
    valid_categories = {
        "정치", "경제", "사회", "연예", "스포츠", "기술", "건강", "환경", "과학"
    }
    filtered_df = merged_df[merged_df["분류"].isin(valid_categories)].copy()

    # 4. 상위 50개만 선택
    top_50_df = filtered_df.head(50)

    # 5. 카테고리별 그룹핑
    grouped = top_50_df.groupby("분류")

    # 6. JSONL 파일 저장
    os.makedirs("output", exist_ok=True)
    output_path = "output/top_50_keywords_by_category_2024.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for category, group in grouped:
            print(f"\n# {category} 카테고리 ({len(group)}개)")
            for _, row in group.iterrows():
                json_obj = {
                    "word": row["단어"],
                    "score": round(row["점수"], 3),
                    "period": "2024",
                    "category": category
                }
                f.write(json.dumps(json_obj, ensure_ascii=False) + "\n")
                print(json.dumps(json_obj, ensure_ascii=False))

    print(f"\n {output_path} 저장 완료 (카테고리별 정렬 포함)")


if __name__ == "__main__":
    play_from_google_csv()
    schedule.every(10).minutes.do(play_from_google_csv)
    print("[대기] 10분마다 자동 실행 중... Ctrl+C로 중단")
    while True:
        schedule.run_pending()
        time.sleep(1)
