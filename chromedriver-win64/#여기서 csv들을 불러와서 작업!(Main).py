import pandas as pd
import os

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

print(word_score)
print(rel_words)
print(main_words)

