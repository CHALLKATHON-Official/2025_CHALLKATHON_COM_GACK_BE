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
word_score = read_csv_file(os.path.join(folder, "단어점수.csv"))
rel_words = read_csv_file(os.path.join(folder, "연관단어점수.csv")) #단어1, 점수1, 단어2, 점수2, ...
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
        return score_mapping[value]
    if "만+" in value:
        try:
            return int(float(value.replace("만+", "")) * 10000)
        except:
            return 0
    if "천+" in value:
        try:
            return int(float(value.replace("천+", "")) * 1000)
        except:
            return 0
    if value.endswith("+"):
        try:
            return int(value.replace("+", ""))
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


def guess_category(word):
    categories = {
        "정치": ["국방부장관", "장관", "의원", "정치", "정부", "안규백"],
        "스포츠": ["맨시티", "축구", "야구", "선수", "쇼헤이", "오타니"],
        "연예": ["배우", "가수", "영화", "드라마"],
        "경제": ["주식", "투자", "가격", "증권", "금융"],
    }
    word_lower = word.lower()
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw.lower() in word_lower:
                return cat
    return "기타"

def get_search_volume(norm_word, df):
    for i, trend in enumerate(df["트렌드"]):
        trend_norm = normalize(trend)
        # 부분 매칭: norm_word가 trend_norm 안에 있거나 trend_norm이 norm_word 안에 있으면 매칭
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
    added_words = set()  # 원본 단어 중복 체크용

    for norm_word, score in top_n:
        matched_trends = [t for t in trend_list if norm_word == normalize(t) or norm_word in normalize(t)]
        original_word = matched_trends[0] if matched_trends else norm_word

        # 중복 단어면 건너뛰기
        if original_word in added_words:
            continue
        added_words.add(original_word)

        internal = internal_freq.get(original_word, 0)
        external = next((x["수치점수"] for x in external_list if normalize(x["단어"]) == norm_word), 0)
        final_score = score
        related_words = related_score_dict.get(norm_word, {})

        category_str = "정보없음"
        for i, trend_norm in enumerate(trend_norm_list):
            if norm_word == trend_norm or normalize(original_word) == trend_norm:
                if "카테고리" in df.columns and pd.notna(df["카테고리"].iloc[i]):
                    category_str = str(df["카테고리"].iloc[i])
                else:
                    category_str = guess_category(original_word)
                break

        search_volume = get_search_volume(norm_word, df)

        result_list.append({
            "word": original_word,
            "internal_freq": internal,
            "external_score": external,
            "final_score": final_score,
            "search_volume": search_volume,
            "related_keywords": related_words,
            "category": category_str
        })

    print("\n[분석 결과 요약]")
    for r in result_list:
        print(f"word: {r['word']}, score: {r['final_score']}, search_volume: {r['search_volume']}, category: {r['category']}")

    print("\n[연관어 및 점수]")
    for r in result_list:
        print(f"{r['word'].replace(' ', '')}:")
        for k, v in r["related_keywords"].items():
            print(f"  {k.replace(' ', '')} -> {v}")


    os.makedirs("output", exist_ok=True)
    pd.DataFrame([{
        "word": r["word"],
        "internal_freq": r["internal_freq"],
        "external_score": r["external_score"],
        "final_score": r["final_score"],
        "search_volume": r["search_volume"],
        "category": r["category"]
    } for r in result_list]).to_csv("output/final_scores.csv", index=False, encoding="utf-8-sig")

    with open("output/result_for_frontend.json", "w", encoding="utf-8") as f:
        json.dump(result_list, f, ensure_ascii=False, separators=(',', ':'))

    with open("output/related_keywords.json", "w", encoding="utf-8") as f:
        json.dump(related_score_dict, f, ensure_ascii=False, indent=2)

    print("[완료] 모든 결과 저장 완료!")
    return result_list, related_score_dict


if __name__ == "__main__":
    play_from_google_csv()
    schedule.every(10).minutes.do(play_from_google_csv)
    print("[대기] 10분마다 자동 실행 중... Ctrl+C로 중단")
    while True:
        schedule.run_pending()
        time.sleep(1)
