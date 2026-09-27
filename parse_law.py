import re


CHINESE_NUMBERS = {
    "〇": 0,
    "零": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "百": 100,
    "千": 1000
}


def chinese_to_number(text):
    total = 0
    section = 0

    for char in text:
        value = CHINESE_NUMBERS.get(char)

        if value is None:
            continue

        if value >= 10:
            if section == 0:
                section = 1

            total += section * value
            section = 0
        else:
            section = section * 10 + value

    return total + section


def number_to_chinese(number):
    """把整数转换成常用的中文数字。"""

    digits = {
        0: "〇",
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九"
    }

    if number < 10:
        return digits[number]

    if number < 20:
        return "十" + (digits[number - 10] if number > 10 else "")

    if number < 100:
        tens = number // 10
        ones = number % 10

        result = digits[tens] + "十"

        if ones:
            result += digits[ones]

        return result

    if number < 1000:
        hundreds = number // 100
        remainder = number % 100

        result = digits[hundreds] + "百"

        if remainder == 0:
            return result

        if remainder < 10:
            return result + "零" + digits[remainder]

        if remainder < 20:
            return result + "零十" + (
                digits[remainder - 10]
                if remainder > 10
                else ""
            )

        tens = remainder // 10
        ones = remainder % 10

        result += digits[tens] + "十"

        if ones:
            result += digits[ones]

        return result

    return str(number)


def make_record(
    chapter,
    section,
    article,
    article_number,
    paragraph,
    paragraph_number,
    item,
    item_number,
    text
):
    return {
        "chapter": chapter,
        "section": section,
        "article": article,
        "article_number": article_number,
        "paragraph": paragraph,
        "paragraph_number": paragraph_number,
        "item": item,
        "item_number": item_number,
        "text": text
    }


def split_items(line):
    """
    把一行中连续出现的多个项拆开。

    例如：
    （三）AAA；（四）BBB；

    会变成：
    （三）AAA；
    （四）BBB；
    """

    pattern = r"(?=（[一二三四五六七八九十百千万零〇0-9]+）)"

    parts = re.split(pattern, line)

    return [part.strip() for part in parts if part.strip()]


def parse_law_structure(text):
    records = []

    current_chapter = None
    current_section = None
    current_article = None
    current_article_number = None

    current_paragraph = None
    current_paragraph_number = None

    current_item = None
    current_item_number = None

    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # 章
        chapter_match = re.fullmatch(
            r"(第[一二三四五六七八九十百千万零〇0-9]+章.*)",
            line
        )

        if chapter_match:
            current_chapter = chapter_match.group(1).strip()

            current_section = None
            current_article = None
            current_article_number = None
            current_paragraph = None
            current_paragraph_number = None
            current_item = None
            current_item_number = None

            continue

        # 节
        section_match = re.fullmatch(
            r"(第[一二三四五六七八九十百千万零〇0-9]+节.*)",
            line
        )

        if section_match:
            current_section = section_match.group(1).strip()

            current_article = None
            current_article_number = None
            current_paragraph = None
            current_paragraph_number = None
            current_item = None
            current_item_number = None

            continue

        # 条
        article_match = re.fullmatch(
            r"第([一二三四五六七八九十百千万零〇0-9\s]+)条(.*)",
            line
        )

        if article_match:
            current_article = article_match.group(1).replace(" ", "")
            current_article_number = chinese_to_number(
                current_article
            )

            current_paragraph = None
            current_paragraph_number = None
            current_item = None
            current_item_number = None

            article_text = article_match.group(2).strip()

            if article_text:
                current_paragraph_number = 1
                current_paragraph = number_to_chinese(1)

                records.append(
                    make_record(
                        current_chapter,
                        current_section,
                        current_article,
                        current_article_number,
                        current_paragraph,
                        current_paragraph_number,
                        None,
                        None,
                        article_text
                    )
                )

            continue

        # 明确标记的款
        paragraph_match = re.fullmatch(
            r"第([一二三四五六七八九十百千万零〇0-9]+)款(.*)",
            line
        )

        if paragraph_match:
            current_paragraph = paragraph_match.group(1)
            current_paragraph_number = chinese_to_number(
                current_paragraph
            )

            current_item = None
            current_item_number = None

            paragraph_text = paragraph_match.group(2).strip()

            if paragraph_text:
                records.append(
                    make_record(
                        current_chapter,
                        current_section,
                        current_article,
                        current_article_number,
                        current_paragraph,
                        current_paragraph_number,
                        None,
                        None,
                        paragraph_text
                    )
                )

            continue

        # 项
        if re.search(
            r"（[一二三四五六七八九十百千万零〇0-9]+）",
            line
        ):
            item_parts = split_items(line)

            for item_part in item_parts:

                item_match = re.fullmatch(
                    r"（([一二三四五六七八九十百千万零〇0-9]+)）(.*)",
                    item_part
                )

                if not item_match:
                    continue

                current_item = item_match.group(1)

                current_item_number = chinese_to_number(
                    current_item
                )

                item_text = item_match.group(2).strip()

                records.append(
                    make_record(
                        current_chapter,
                        current_section,
                        current_article,
                        current_article_number,
                        current_paragraph,
                        current_paragraph_number,
                        current_item,
                        current_item_number,
                        item_text
                    )
                )

            continue

        # 普通正文
        if current_article is not None:

            # 当前条还没有任何正文
            if current_paragraph_number is None:

                current_paragraph_number = 1
                current_paragraph = number_to_chinese(1)

            else:
                current_paragraph_number += 1
                current_paragraph = number_to_chinese(
                    current_paragraph_number
                )

            current_item = None
            current_item_number = None

            records.append(
                make_record(
                    current_chapter,
                    current_section,
                    current_article,
                    current_article_number,
                    current_paragraph,
                    current_paragraph_number,
                    None,
                    None,
                    line
                )
            )

    return records


if __name__ == "__main__":

    sample_text = """
第一章 总纲

第一条 这是第一条第一款。
这是第一条第二款。

第二条
这是第二条第一款。
这是第二条第二款。

第三条
第一款 这是第三条第一款。
第二款 这是第三条第二款。
第三款
（一）这是第三款第一项。
（二）这是第三款第二项。

第六十三条
（一）第一项内容；（二）第二项内容；（三）第三项内容；（四）第四项内容。
"""

    result = parse_law_structure(sample_text)

    for record in result:
        print(record)