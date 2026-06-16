import os
import sys
import time

# 确保可以 import backend 下的模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    MAX_PAGES,
    PAGE_SIZE
)

from fetcher import fetch_page
from parser import parse_comments
from uploader import upload_comments
from cleaner import clean_comments
from storage import (
    save_cleaned,
    save_analysis,
    save_sentiment_statistics,
    save_keywords,
    save_rating_distribution,
    save_summary
)
from backend.llm_service import analyze_sentiment
from sentiment import analyze_comments, analyze_comments_with_snownlp
from movie_stats import (
    generate_sentiment_statistics,
    generate_rating_distribution,
    generate_keywords,
    generate_summary
)
from movie_meta import fetch_and_save_poster, load_movie_meta


def build_url(movie_id, start):
    """根据影片 ID 和起始位置构造豆瓣评论页 URL"""
    return (
        f"https://movie.douban.com/subject/{movie_id}/comments"
        f"?start={start}&limit=20&status=P&sort=new_score"
    )


def crawl(movie_name, movie_id, comment_type="latest", analysis_mode="llm"):
    """
    爬取指定影片的评论，完成清洗和情感分析。

    analysis_mode:
        "llm"     — 调用大模型精准分析（慢，准确度高）
        "snownlp" — snownlp 模型分析（较快，准确度较高，离线可用）
        "local"   — 本地关键词匹配快速分析（最快，准确度较低）
    """
    all_comments = []
    all_analyzed = []

    failed_pages = 0

    total_pages = MAX_PAGES
    for page in range(MAX_PAGES):

        # 显示进度
        progress_pct = (page + 1) / total_pages * 100
        bar_len = 30
        filled = int(bar_len * (page + 1) / total_pages)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(
            f"\r  进度: [{bar}] {page + 1}/{total_pages} 页 "
            f"({progress_pct:.0f}%)  "
            f"已获取 {len(all_comments)} 条",
            end="",
            flush=True,
        )

        start = page * PAGE_SIZE

        url = build_url(movie_id, start)

        html = fetch_page(url)

        if not html:
            failed_pages += 1
            continue

        raw_comments = parse_comments(html)

        comments = clean_comments(raw_comments)
        save_cleaned(
            movie_name=movie_name,
            comment_type=comment_type,
            comments=comments
        )

        # 根据模式选择情感分析方式
        if analysis_mode == "local":
            analyzed_comments = analyze_comments(comments)
        elif analysis_mode == "snownlp":
            analyzed_comments = analyze_comments_with_snownlp(comments)
        else:
            analyzed_comments = []
            for comment in comments:
                sentiment_result = analyze_sentiment(comment["content"])
                analyzed_comments.append({
                    **comment,
                    "sentiment": sentiment_result
                })

        save_analysis(
            movie_name=movie_name,
            comment_type=comment_type,
            analysis_data=analyzed_comments
        )

        all_comments.extend(comments)
        all_analyzed.extend(analyzed_comments)

        # 防止请求太快
        time.sleep(2)

    print()  # 进度行换行

    print(f"爬取完成：{len(all_comments)} 条评论（{MAX_PAGES} 页，{failed_pages} 页失败）")

    # 获取并保存影片海报
    fetch_and_save_poster(movie_name, movie_id)

    return all_comments, all_analyzed


def main():

    print("=" * 50)
    print("  豆瓣影评爬虫")
    print("=" * 50)

    movie_name = input("请输入影片名称: ").strip()
    if not movie_name:
        print("影片名称不能为空")
        return

    movie_id = input("请输入豆瓣影片 ID (如 1292052): ").strip()
    if not movie_id:
        print("影片 ID 不能为空")
        return

    comment_type = input("评论类型 (hot / latest, 默认 latest): ").strip()
    if comment_type not in ("hot", "latest"):
        comment_type = "latest"

    print()
    print("情感分析模式：")
    print("  [1] 大模型精准分析（慢，准确度高，需联网）")
    print("  [2] snownlp 模型分析（较快，准确度较高，离线可用）")
    print("  [3] 本地词典快速分析（最快，准确度较低，离线可用）")
    mode_choice = input("请选择 (1/2/3, 默认 1): ").strip()
    if mode_choice == "3":
        analysis_mode = "local"
    elif mode_choice == "2":
        analysis_mode = "snownlp"
    else:
        analysis_mode = "llm"

    comments, analyzed = crawl(movie_name, movie_id, comment_type, analysis_mode)

    if not comments:
        print("没有获取到评论")
        return

    # 生成统计（本地落盘）
    sentiment_stats = generate_sentiment_statistics(analyzed)
    save_sentiment_statistics(movie_name=movie_name, data=sentiment_stats)

    rating_stats = generate_rating_distribution(analyzed)
    save_rating_distribution(movie_name=movie_name, data=rating_stats)

    keyword_stats = generate_keywords(analyzed)
    save_keywords(movie_name=movie_name, data=keyword_stats)

    summary = generate_summary(analyzed)
    save_summary(movie_name=movie_name, data=summary)

    # 读取海报信息（由 crawl 内部 fetch_and_save_poster 保存）
    meta = load_movie_meta(movie_name) or {}
    poster_url = meta.get("poster_url")
    poster_path = meta.get("poster_local")

    # 上传到后端（海报文件直接 base64 传输，ECS 端无需重复下载豆瓣 CDN）
    upload_comments(
        movie_name=movie_name,
        comment_type=comment_type,
        comments=comments,
        analyzed_comments=analyzed,
        sentiment_stats=sentiment_stats,
        rating_stats=rating_stats,
        keyword_stats=keyword_stats,
        summary=summary,
        poster_url=poster_url,
        movie_id=movie_id,
        poster_path=poster_path,
    )


if __name__ == "__main__":
    main()
