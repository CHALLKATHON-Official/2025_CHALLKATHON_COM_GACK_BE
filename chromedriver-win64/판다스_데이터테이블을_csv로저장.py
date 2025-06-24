import os

# OneDrive + 한글 바탕화면 예시
desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "바탕 화면")
if not os.path.exists(desktop):
    os.makedirs(desktop)

file_path = os.path.join(desktop, "my_data.txt")
data =''
while(1):
    now = input("저장할 내용을 입력하세요: ")
    if now == "exit":
        break
    data += now

with open(file_path, "w", encoding="utf-8") as f:
    f.write(data)
print(f"저장 완료: {file_path}")

with open(file_path, "r", encoding="utf-8") as f:
    loaded = f.read()
print("불러온 내용:", loaded)
