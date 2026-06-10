import requests

from config import UPLOAD_URL


def upload_comments(
    movie_name,
    comment_type,
    comments,
    analyzed_comments=None,
    sentiment_stats=None,
    rating_stats=None,
    keyword_stats=None,
    summary=None,
):

    data = {
        "movie_name": movie_name,
        "comment_type": comment_type,
        "comments": comments,
        "analyzed_comments": analyzed_comments or [],
        "sentiment_stats": sentiment_stats,
        "rating_stats": rating_stats,
        "keyword_stats": keyword_stats,
        "summary": summary,
    }

    try:
        response = requests.post(
            UPLOAD_URL,
            json=data
        )

        print("上传结果:", response.json())

    except Exception as e:
        print("上传失败:", e)
