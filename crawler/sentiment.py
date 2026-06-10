# =========================
# 情感关键词
# =========================

POSITIVE_WORDS = [
    "好看",
    "精彩",
    "感动",
    "经典",
    "震撼",
    "喜欢",
    "推荐",
    "优秀",
    "牛",
    "完美"
]

NEGATIVE_WORDS = [
    "难看",
    "无聊",
    "垃圾",
    "失望",
    "尴尬",
    "烂",
    "差",
    "无语",
    "拖沓",
    "看不懂"
]


# =========================
# 分析单条评论
# =========================
def analyze_comment(comment):

    content = comment["content"]

    positive_count = 0
    negative_count = 0

    # 正向词统计
    for word in POSITIVE_WORDS:

        if word in content:
            positive_count += 1

    # 负向词统计
    for word in NEGATIVE_WORDS:

        if word in content:
            negative_count += 1

    # 情感判断
    if positive_count > negative_count:

        sentiment = "positive"

    elif negative_count > positive_count:

        sentiment = "negative"

    else:

        sentiment = "neutral"

    # 简单分数
    total = positive_count + negative_count

    if total == 0:
        score = 0.5
    else:
        score = positive_count / total

    return {
        **comment,
        "sentiment": sentiment,
        "score": round(score, 2)
    }


# =========================
# 分析评论列表
# =========================
def analyze_comments(comments):

    results = []

    for comment in comments:

        analyzed = analyze_comment(comment)

        results.append(analyzed)

    return results