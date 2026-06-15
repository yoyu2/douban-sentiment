"""
本地词典情感分析 —— 基于关键词匹配，无需网络调用，速度快。
适合快速预览，准确度不如大模型。
"""

# =========================
# 情感关键词
# =========================

POSITIVE_WORDS = [
    "好看", "精彩", "感动", "经典", "震撼", "喜欢", "推荐",
    "优秀", "牛", "完美", "不错", "很棒", "出色", "伟大",
    "深刻", "惊艳", "赞", "良心", "神作", "最爱", "值得",
    "享受", "热血", "温暖", "治愈", "满分", "厉害", "绝了",
    "吹爆", "封神", "巅峰", "顶级", "炸裂",
]

NEGATIVE_WORDS = [
    "难看", "无聊", "垃圾", "失望", "尴尬", "烂", "差",
    "无语", "拖沓", "看不懂", "浪费时间", "催眠", "糟糕",
    "平庸", "烂片", "吐槽", "恶心", "浮夸", "空洞", "造作",
    "尴尬", "俗套", "狗血", "翻车", "灾难", "劝退",
]


# =========================
# 分析单条评论
# =========================
def analyze_comment(comment):
    """
    返回带 sentiment 和 score 的评论。
    score 基于关键词匹配比例，仅作参考。
    """
    content = comment.get("content", "")

    positive_count = 0
    negative_count = 0

    for word in POSITIVE_WORDS:
        if word in content:
            positive_count += 1

    for word in NEGATIVE_WORDS:
        if word in content:
            negative_count += 1

    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    total = positive_count + negative_count
    score = positive_count / total if total else 0.5

    return {
        **comment,
        "sentiment": sentiment,
        "score": round(score, 2),
    }


# =========================
# 分析评论列表
# =========================
def analyze_comments(comments):
    results = []
    for comment in comments:
        results.append(analyze_comment(comment))
    return results


# =========================
# snownlp 情感分析 —— 纯 Python，无需联网，准确度比关键词高
# =========================
def analyze_comments_with_snownlp(comments):
    """
    使用 snownlp 批量分析评论情感。
    snownlp 返回 0~1 的分数，越接近 1 越正面。
    """
    from snownlp import SnowNLP

    results = []
    for comment in comments:
        content = comment.get("content", "")
        s = SnowNLP(content)
        score = s.sentiments

        if score > 0.6:
            sentiment = "positive"
        elif score < 0.4:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        results.append({
            **comment,
            "sentiment": sentiment,
            "score": round(score, 2),
        })

    return results
