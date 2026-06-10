import time

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
from sentiment import analyze_comments
from movie_stats import (
    generate_sentiment_statistics,
    generate_rating_distribution,
    generate_keywords,
    generate_summary
)


def build_url(movie_id, start):
    """根据影片 ID 和起始位置构造豆瓣评论页 URL"""
    return (
        f"https://movie.douban.com/subject/{movie_id}/comments"
        f"?start={start}&limit=20&status=P&sort=new_score"
    )


def crawl(movie_name, movie_id, comment_type="latest"):
    """爬取指定影片的评论，完成清洗和情感分析"""
    all_comments = []
    all_analyzed = []

    for page in range(MAX_PAGES):

        start = page * PAGE_SIZE

        url = build_url(movie_id, start)

        print("=" * 50)
        print(f"正在爬取: {url}")

        html = fetch_page(url)

        if not html:
            print("页面获取失败")
            continue

        raw_comments = parse_comments(html)

        comments = clean_comments(raw_comments)
        save_cleaned(
            movie_name=movie_name,
            comment_type=comment_type,
            comments=comments
        )

        analyzed_comments = analyze_comments(comments)
        save_analysis(
            movie_name=movie_name,
            comment_type=comment_type,
            analysis_data=analyzed_comments
        )

        print(f"当前页获取 {len(comments)} 条评论")

        all_comments.extend(comments)
        all_analyzed.extend(analyzed_comments)

        # 防止请求太快
        time.sleep(2)

    print("=" * 50)
    print(f"总共获取 {len(all_comments)} 条评论")

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
    print(f"开始爬取: {movie_name} (ID={movie_id}, {comment_type})")
    print()

    comments, analyzed = crawl(movie_name, movie_id, comment_type)

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

    # 上传到后端（后端只落盘，不重复分析）
    upload_comments(
        movie_name=movie_name,
        comment_type=comment_type,
        comments=comments,
        sentiment_stats=sentiment_stats,
        rating_stats=rating_stats,
        keyword_stats=keyword_stats,
        summary=summary,
    )


if __name__ == "__main__":
    main()
