import re


def parse_hierarchy(text):
    records = []

    current_article = None
    current_paragraph = None

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # 条
        article_match = re.fullmatch(
            r"第([一二三四五六七八九十百千万零〇0-9]+)条",
            line
        )

        if article_match:
            current_article = article_match.group(1)
            current_paragraph = None
            continue

        # 款
        paragraph_match = re.fullmatch(
            r"第([一二三四五六七八九十百千万零〇0-9]+)款(.*)",
            line
        )

        if paragraph_match:
            current_paragraph = paragraph_match.group(1)
            paragraph_text = paragraph_match.group(2).strip()

            if paragraph_text:
                records.append({
                    "article": current_article,
                    "paragraph": current_paragraph,
                    "item": None,
                    "text": paragraph_text
                })

            continue

        # 项
        item_match = re.fullmatch(
            r"（([一二三四五六七八九十百千万零〇0-9]+)）(.*)",
            line
        )

        if item_match:
            records.append({
                "article": current_article,
                "paragraph": current_paragraph,
                "item": item_match.group(1),
                "text": item_match.group(2).strip()
            })

            continue


    return records


if __name__ == "__main__":
    with open("hierarchy_test.txt", "r", encoding="utf-8") as file:
        text = file.read()

    result = parse_hierarchy(text)

    for record in result:
        print(record)