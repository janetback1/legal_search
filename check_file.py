from clean_text import clean_html

with open("constitution_2018.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

cleaned = clean_html(raw_text)

print("清洗前字符数：", len(raw_text))
print("清洗后字符数：", len(cleaned))

print("\n最后500个字符：")
print(cleaned[-500:])