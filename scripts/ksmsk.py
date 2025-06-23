from pytrends.request import TrendReq
from datetime import datetime
import pandas as pd
import os


keywords = ["이스라엘", "이란"] #예시
pytrends = TrendReq(hl='ko', tz=540)
pytrends.build_payload(keywords, timeframe='now 1-H')
data = pytrends.interest_over_time()
latest = data.iloc[-1][keywords]


now = datetime.now().strftime('%Y-%m-%d %H:%M')
df = pd.DataFrame([
    {"단어": word, "빈도수": int(latest[word]), "시간": now, "출처": "google"}
    for word in keywords
])

df["관심도 점수"] = df["빈도수"] * 4.2


os.makedirs("output", exist_ok=True)
df.to_csv("output/keywords_today.csv", index=False, encoding="utf-8-sig")
print(" 자동 수집 및 저장 완료!")
