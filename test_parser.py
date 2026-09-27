import json

from parse_law import parse_law_structure


with open("real_law1.txt", "r", encoding="utf-8") as file:
    text = file.read()


result = parse_law_structure(text)


output_file = "laws/cn/constitution/versions/2018/articles.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)


print("法律文本解析完成。")
print("共解析", len(result), "条。")
print("结果已保存到 articles.json")