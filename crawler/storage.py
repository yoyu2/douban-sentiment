import json
import os


# =========================
# 创建目录
# =========================
def ensure_dir(path):

    if not os.path.exists(path):
        os.makedirs(path)


# =========================
# 保存 cleaned 数据
# =========================
def save_cleaned(
    movie_name,
    comment_type,
    comments
):

    folder = (
        f"data/cleaned/{movie_name}"
    )

    ensure_dir(folder)

    filepath = (
        f"{folder}/{comment_type}.json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            comments,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"cleaned 数据已保存: {filepath}")


# =========================
# 保存 analyzed 数据
# =========================
def save_analysis(
    movie_name,
    comment_type,
    analysis_data
):

    folder = (
        f"data/analyzed/{movie_name}"
    )

    ensure_dir(folder)

    filepath = (
        f"{folder}/{comment_type}_analysis.json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            analysis_data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"analysis 数据已保存: {filepath}")


# =========================
# 读取 JSON
# =========================
def load_json(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)
    
# =========================
# 保存统计结果
# =========================
def save_sentiment_statistics(
    movie_name,
    data
):

    folder = (
        f"data/statistics/{movie_name}"
    )

    ensure_dir(folder)

    filepath = (
        f"{folder}/sentiment.json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )
def save_keywords(
    movie_name,
    data
):

    folder = (
        f"data/statistics/{movie_name}"
    )

    ensure_dir(folder)

    filepath = (
        f"{folder}/keywords.json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )
def save_rating_distribution(
    movie_name,
    data
):

    folder = (
        f"data/statistics/{movie_name}"
    )

    ensure_dir(folder)

    filepath = (
        f"{folder}/rating_distribution.json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

def save_summary(
    movie_name,
    data
):

    folder = (
        f"data/statistics/{movie_name}"
    )

    ensure_dir(folder)

    filepath = (
        f"{folder}/summary.json"
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )