import os
import base64
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
    poster_url=None,
    movie_id=None,
    poster_path=None,
):

    # 读取本地海报文件（base64 编码后直接传输，ECS 端无需重复下载）
    poster_base64 = None
    if poster_path and os.path.exists(poster_path):
        with open(poster_path, "rb") as f:
            poster_base64 = base64.b64encode(f.read()).decode("utf-8")

    data = {
        "movie_name": movie_name,
        "comment_type": comment_type,
        "comments": comments,
        "analyzed_comments": analyzed_comments or [],
        "sentiment_stats": sentiment_stats,
        "rating_stats": rating_stats,
        "keyword_stats": keyword_stats,
        "summary": summary,
        "poster_url": poster_url,
        "movie_id": movie_id,
        "poster_base64": poster_base64,
    }

    try:
        response = requests.post(
            UPLOAD_URL,
            json=data
        )

        print("上传结果:", response.json())

    except Exception as e:
        print("上传失败:", e)
