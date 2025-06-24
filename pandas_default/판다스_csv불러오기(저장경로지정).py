import numpy as np
import pandas as pd
import os
from tabulate import tabulate

# OneDrive + 한글 바탕화면 예시
desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "바탕 화면")
if not os.path.exists(desktop):
    os.makedirs(desktop)

file_path = os.path.join(desktop, "trending_KR_1d_20250623-1613.csv")

df = pd.read_csv(file_path, index_col = 0)
print(df)

df.to_excel("mytable.xlsx", index=False)
df.to_html("mytable.html", index=False)

excel_path = "mytable.xlsx"
os.startfile(excel_path)