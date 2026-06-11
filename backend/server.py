import os
import sys
from urllib.parse import unquote

# 无论从哪里运行 server.py，都把项目根目录加到 path
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from sanic import Sanic
from sanic_cors import CORS
from sanic.response import json as json_response, file as file_response
from crawler.storage import (
    load_json,
    save_cleaned,
    save_analysis,
    save_sentiment_statistics,
    save_keywords,
    save_rating_distribution,
    save_summary,
)
from crawler.movie_meta import load_movie_meta

app = Sanic("douban-sentiment")
CORS(app)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@app.get("/")
async def health(request):
    return json_response({"msg": "server is running"})


@app.get("/api/posters/<movie_name>")
async def get_poster(request, movie_name):
    """返回本地缓存的影片海报图片"""
    movie_name = unquote(movie_name)
    poster_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "posters",
        f"{movie_name}.jpg"
    )
    if os.path.exists(poster_path):
        return await file_response(poster_path)
    return json_response({"error": "poster not found"}, status=404)


@app.get("/api/movies")
async def list_movies(request):
    """列出所有已分析的影片，含海报信息"""
    stats_dir = os.path.join(DATA_DIR, "statistics")
    movies = []
    if os.path.exists(stats_dir):
        for name in sorted(os.listdir(stats_dir)):
            meta = load_movie_meta(name)
            movies.append({
                "name": name,
                "poster": f"/api/posters/{name}" if meta and meta.get("poster_url") else None,
            })
    return json_response({"movies": movies})


@app.get("/api/movies/<movie_name>/statistics")
async def get_statistics(request, movie_name):
    """返回影片完整统计数据"""

    movie_name = unquote(movie_name)

    base = os.path.join(
        DATA_DIR,
        "statistics",
        movie_name
    )

    result = {}

    for key, filename in [
        ("sentiment", "sentiment.json"),
        ("rating_distribution", "rating_distribution.json"),
        ("keywords", "keywords.json"),
    ]:

        path = os.path.join(base, filename)

        if os.path.exists(path):
            result[key] = load_json(path)

    summary_path = os.path.join(base, "summary.json")

    if os.path.exists(summary_path):
        result["summary"] = load_json(summary_path)

    if not result:
        return json_response(
            {"error": "movie not found"},
            status=404
        )

    # 附加海报信息
    meta = load_movie_meta(movie_name)
    if meta and meta.get("poster_url"):
        result["poster"] = f"/api/posters/{movie_name}"

    return json_response(result)
@app.get("/api/movies/<movie_name>/comments")
async def get_comments(request, movie_name):
    movie_name = unquote(movie_name)

    """返回分析后的评论，支持 sentiment 和 type 筛选"""
    comment_type = request.args.get("type", "latest")
    sentiment_filter = request.args.get("sentiment")

    path = os.path.join(
        DATA_DIR, "analyzed", movie_name,
        f"{comment_type}_analysis.json"
    )

    if not os.path.exists(path):
        return json_response({"error": "comments not found"}, status=404)

    comments = load_json(path)

    if sentiment_filter:
        comments = [
            c for c in comments
            if c.get("sentiment") == sentiment_filter
        ]

    return json_response({
        "movie_name": movie_name,
        "comment_type": comment_type,
        "count": len(comments),
        "comments": comments,
    })


@app.post("/api/upload")
async def upload(request):
    """
    接收爬虫上传的完整数据包，只落盘不重复分析
    """
    data = request.json

    if not data:
        return json_response({"error": "invalid data"}, status=400)

    movie_name = data.get("movie_name", "unknown")
    comment_type = data.get("comment_type", "latest")
    comments = data.get("comments", [])

    if not comments:
        return json_response({"error": "no comments provided"}, status=400)

    save_cleaned(movie_name, comment_type, comments)

    analyzed = data.get("analyzed_comments", [])
    if analyzed:
        save_analysis(movie_name, comment_type, analyzed)

    if data.get("sentiment_stats"):
        save_sentiment_statistics(movie_name, data["sentiment_stats"])

    if data.get("rating_stats"):
        save_rating_distribution(movie_name, data["rating_stats"])

    if data.get("keyword_stats"):
        save_keywords(movie_name, data["keyword_stats"])

    if data.get("summary"):
        save_summary(movie_name, data["summary"])

    return json_response({
        "status": "success",
        "count": len(comments),
        "summary": data.get("summary"),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
