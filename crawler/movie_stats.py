# statistics.py

import jieba
from collections import Counter


# =========================
# 停用词
# =========================
STOPWORDS = {
    # 语气词 / 助词
    "的", "了", "在", "是", "有", "和", "与", "或",
    "着", "过", "被", "把", "让", "给", "对", "从",
    "到", "之", "等", "所", "其", "为", "及", "以",
    # 人称
    "我", "你", "他", "她", "它", "自己", "别人",
    "我们", "你们", "他们", "她们", "它们",
    "人们", "大家", "有人", "每个人",
    # 指代
    "这", "那", "这个", "那个", "这些", "那些",
    "这部", "这种", "那种", "这样", "那样",
    "这里", "那里", "哪部", "哪种", "这次",
    # 副词
    "很", "太", "都", "也", "就", "还", "又",
    "再", "才", "只", "能", "会", "不",
    "很", "非常", "真的", "特别", "多么",
    "没有", "已经", "曾经", "正在", "还是",
    "总是", "一直", "一定", "可能", "也许",
    "必须", "应该", "可以", "比较", "更加",
    "不是", "没", "什么", "怎么", "那么", "这么",
    "要么", "如果", "因为", "所以", "但是",
    "不过", "就是", "只是", "然后", "虽然", "而且",
    "无法", "一切", "一样",
    # 时间
    "时候", "现在", "以前", "以后", "之后",
    "最后", "开始", "一直", "终于", "已经",
    "今天", "昨天", "明天", "当时",
    # 数量 / 程度
    "一个", "一部", "一种", "很多", "很少",
    "整个", "某些", "任何", "全部", "有些",
    "有点", "一点", "一下",
    # 感觉 / 表达
    "觉得", "认为", "感觉", "觉得", "知道",
    "想到", "看到", "听到", "可能", "也许",
    "应该", "确实", "当然",
    # 评论通用词
    "电影", "影片", "片子", "这部片",
    "剧情", "导演", "演员", "豆瓣",
    "好看", "不错", "一般",
    # 英文高频噪声
    "the", "a", "an", "is", "are", "of", "in", "to", "it", "and",
    "that", "this", "be", "for", "on", "was", "can", "so", "with",
    "but", "if", "or", "no", "its", "all", "as", "not", "I", "you",
    "he", "she", "we", "they", "his", "her", "my", "me", "has",
    "have", "been", "will", "would", "should", "could", "more",
    "very", "just", "like", "one", "when", "about", "than",
    "also", "had", "it's", "don't", "there", "their",
    "too", "i", "s",
}


# =========================
# 情感统计
# sentiment.json
# =========================
def generate_sentiment_statistics(comments):

    total = len(comments)

    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for comment in comments:

        sentiment = comment.get("sentiment", "neutral")

        if sentiment == "positive":
            positive_count += 1

        elif sentiment == "negative":
            negative_count += 1

        else:
            neutral_count += 1

    return {

        "total_comments": total,

        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,

        "positive_ratio": round(
            positive_count / total,
            2
        ) if total else 0,

        "negative_ratio": round(
            negative_count / total,
            2
        ) if total else 0,

        "neutral_ratio": round(
            neutral_count / total,
            2
        ) if total else 0
    }


# =========================
# 评分分布
# rating_distribution.json
# =========================
def generate_rating_distribution(comments):

    ratings = Counter()

    for comment in comments:

        rating = comment.get("rating")

        if rating is not None:

            ratings[str(rating)] += 1

    return {

        "1": ratings.get("1", 0),
        "2": ratings.get("2", 0),
        "3": ratings.get("3", 0),
        "4": ratings.get("4", 0),
        "5": ratings.get("5", 0)
    }


# =========================
# 关键词统计
# keywords.json
# =========================
def generate_keywords(
        comments,
        top_n=50
):

    words = []

    for comment in comments:

        content = comment.get("content", "")

        word_list = jieba.lcut(content)

        for word in word_list:

            word = word.strip()

            # 去掉空字符串
            if not word:
                continue

            # 去掉单字
            if len(word) < 2:
                continue

            # 去掉停用词
            if word in STOPWORDS:
                continue

            words.append(word)

    counter = Counter(words)

    top_words = counter.most_common(top_n)

    result = []

    for word, count in top_words:

        result.append({
            "word": word,
            "count": count
        })

    return result


# =========================
# 首页摘要统计（推荐）
# summary.json
# =========================
def generate_summary(comments):

    total = len(comments)

    if total == 0:

        return {
            "total_comments": 0,
            "average_rating": 0,
            "main_sentiment": "neutral"
        }

    total_rating = 0
    rated_count = 0  # 实际有评分的评论数（未知评分不计入）

    positive = 0
    negative = 0
    neutral = 0

    for comment in comments:

        rating = comment.get("rating")
        if rating is not None:
            total_rating += rating
            rated_count += 1

        sentiment = comment.get(
            "sentiment",
            "neutral"
        )

        if sentiment == "positive":
            positive += 1

        elif sentiment == "negative":
            negative += 1

        else:
            neutral += 1

    average_rating = round(
        total_rating / rated_count,
        2
    ) if rated_count else 0

    sentiment_map = {
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }

    main_sentiment = max(
        sentiment_map,
        key=sentiment_map.get
    )

    return {

        "total_comments": total,

        "average_rating": average_rating,

        "main_sentiment": main_sentiment
    }