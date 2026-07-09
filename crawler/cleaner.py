import re


# =========================
# 去除 emoji
# =========================
def remove_emoji(text):

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE
    )

    return emoji_pattern.sub("", text)


# =========================
# 清洗单条评论
# =========================
def clean_comment(comment):

    content = comment.get("content", "")
    rating = comment.get("rating", "")
    comment_time = comment.get("time", "")

    # 去空格
    content = content.strip()

    # 去换行
    content = content.replace("\n", "")

    # 去 emoji
    content = remove_emoji(content)

    # 去多余空格
    content = re.sub(r"\s+", " ", content)

    # 评分标准化
    rating_map = {
        "allstar10": 1,
        "allstar20": 2,
        "allstar30": 3,
        "allstar40": 4,
        "allstar50": 5
    }

    rating = rating_map.get(rating, None)  # 未知评分 → None，避免被当成 0 分拉低统计

    return {
        "content": content,
        "rating": rating,
        "time": comment_time
    }


# =========================
# 判断是否垃圾评论
# =========================
def is_valid_comment(comment):

    content = comment["content"]

    # 太短
    if len(content) < 2:
        return False

    # 无意义字符
    invalid_text = [
        "...",
        "。。。",
        "哈哈",
        "呵呵"
    ]

    if content in invalid_text:
        return False

    return True


# =========================
# 清洗评论列表
# =========================
def clean_comments(comments):

    cleaned_comments = []

    seen = set()

    for comment in comments:

        cleaned = clean_comment(comment)

        content = cleaned["content"]

        # 去重
        if content in seen:
            continue

        seen.add(content)

        # 过滤垃圾评论
        if not is_valid_comment(cleaned):
            continue

        cleaned_comments.append(cleaned)

    return cleaned_comments