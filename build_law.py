print("BUILD LAW START - CONFIG TEST")

import json
import os

from clean_text import clean_html
from parse_law import parse_law_structure


CONFIG_FILE = "law_config.json"
INDEX_FILE = "law_index.json"

print("CONFIG FILE:", CONFIG_FILE)


# 读取法律配置
with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = json.load(file)


INPUT_FILE = config["input_file"]
OUTPUT_FILE = config["output_file"]


# 读取原始法律文本
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    raw_text = file.read()


# 清洗文本
clean_text = clean_html(raw_text)


# 解析法律结构
result = parse_law_structure(clean_text)


# 如果输出目录不存在，就自动创建
output_dir = os.path.dirname(OUTPUT_FILE)

if output_dir:
    os.makedirs(output_dir, exist_ok=True)

# 保存法律正文结构
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(
        result,
        file,
        ensure_ascii=False,
        indent=2
    )


# 读取法律索引
with open(INDEX_FILE, "r", encoding="utf-8") as file:
    index = json.load(file)


# 查找当前法律是否已经存在
law_exists = False

for law in index["laws"]:
    if law["law_id"] == config["law_id"]:
        law_exists = True

        law["title"] = config["title"]
        law["jurisdiction"] = config["jurisdiction"]
        law["document_type"] = config["document_type"]
        law["current_version"] = config["version"]
        law["status"] = config["status"]

        break

# 如果不存在，就添加
if not law_exists:
    index["laws"].append(
        {
            "law_id": config["law_id"],
            "title": config["title"],
            "jurisdiction": config["jurisdiction"],
"document_type": config["document_type"],
"current_version": config["version"],
"status": config["status"]
        }
    )


# 保存索引
with open(INDEX_FILE, "w", encoding="utf-8") as file:
    json.dump(
        index,
        file,
        ensure_ascii=False,
        indent=2
    )


print("法律数据库构建完成。")
print("法律：", config["title"])
print("版本：", config["version"])
print("解析条目数：", len(result))
print("输出文件：", OUTPUT_FILE)
print("法律索引已更新。")