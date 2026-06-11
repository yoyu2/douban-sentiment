"""
为已有的影片批量下载海报，无需重新爬取评论。

用法：
    1. 在下方 MOVIE_IDS 字典中填入影片名称和对应的豆瓣 ID
    2. 运行: python fetch_posters.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crawler.movie_meta import fetch_and_save_poster

# ============================================================
# 填写影片名称 → 豆瓣 ID 的映射
# 豆瓣影片 ID 可以在影片主页 URL 中找到，例如：
#   https://movie.douban.com/subject/1292052/  → ID 为 1292052
# ============================================================
MOVIE_IDS = {
    "肖申克的救赎": "1292052",
    "阿甘正传": "1292720",
    "疯狂动物城":"25662329",
    "给阿嬷的情书":"37116446",
    # 在下面添加更多影片...
    # "影片名称": "豆瓣ID",
}


def main():
    if not MOVIE_IDS:
        print("请先在脚本中填写 MOVIE_IDS 字典（影片名 → 豆瓣ID）")
        return

    success = 0
    fail = 0

    for name, mid in MOVIE_IDS.items():
        print(f"\n{'=' * 40}")
        print(f"处理: {name} (ID: {mid})")
        meta = fetch_and_save_poster(name, mid)
        if meta and meta.get("poster_url"):
            success += 1
        else:
            fail += 1

    print(f"\n{'=' * 40}")
    print(f"完成: {success} 部成功, {fail} 部失败")


if __name__ == "__main__":
    main()
