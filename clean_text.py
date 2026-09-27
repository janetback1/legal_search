import re
from html import unescape


def clean_html(html):
    # 删除 HTML 标签
    text = re.sub(r"<[^>]+>", " ", html)

    # 转换 HTML 实体
    text = unescape(text)

    # 把不换行空格统一成普通空格
    text = text.replace("\xa0", " ")

    # 删除中文字符之间的排版空格
    text = re.sub(
        r"(?<=[\u4e00-\u9fff])[ \t]+(?=[\u4e00-\u9fff])",
        "",
        text
    )

    # 删除中文标点前面的多余空格
    text = re.sub(
        r"[ \t]+([，。；：！？、）】》])",
        r"\1",
        text
    )

    # 删除中文左括号、书名号后的多余空格
    text = re.sub(
        r"([（【《])\s+",
        r"\1",
        text
    )

    # 连续空格压缩成一个空格
    text = re.sub(r"[ \t]+", " ", text)

    # 去除每一行首尾空格
    text = "\n".join(
        line.strip()
        for line in text.splitlines()
    )

    return text.strip()


if __name__ == "__main__":
    sample_html = """
    <div>人民民 主专政</div>
    <div>中国 特色社会主义</div>
    <div>人民代 表大会</div>
    <div>审判机 关</div>
    <div>国家监察机 关 、审判机关</div>
    <div>国徽 、首都</div>
    """

    result = clean_html(sample_html)

    print(result)