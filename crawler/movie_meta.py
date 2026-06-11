import os
import sys
import json
import requests
from bs4 import BeautifulSoup

# 确保无论从哪里运行都能找到 crawler 包以及 data 目录
_META_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_META_DIR)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

POSTERS_DIR = os.path.join(_PROJECT_ROOT, "data", "posters")
MOVIES_DIR = os.path.join(_PROJECT_ROOT, "data", "movies")

from crawler.config import HEADERS


# =========================
# 获取海报图片 URL
# =========================
def fetch_poster_url(movie_id):
    """从豆瓣影片主页获取海报图片 URL"""
    url = f"https://movie.douban.com/subject/{movie_id}/"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            print(f"  获取影片主页失败，状态码: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # 豆瓣海报图片有 rel="v:image" 属性
        img = soup.find("img", rel="v:image")
        if img and img.get("src"):
            return img["src"]

        # fallback: 找 class=nbgnbg 下的 img
        a_tag = soup.find("a", class_="nbgnbg")
        if a_tag:
            img = a_tag.find("img")
            if img and img.get("src"):
                return img["src"]

        print("  未找到海报图片")
        return None

    except Exception as e:
        print(f"  获取海报异常: {e}")
        return None


# =========================
# 下载海报图片到本地
# =========================
def download_poster(movie_name, poster_url):
    """下载海报到本地，绕过豆瓣的 referrer 检查"""
    os.makedirs(POSTERS_DIR, exist_ok=True)

    filepath = os.path.join(POSTERS_DIR, f"{movie_name}.jpg")

    try:
        # 豆瓣图片 CDN 需要 Referer 头，否则返回 418
        img_headers = {**HEADERS, "Referer": "https://movie.douban.com/"}
        img_response = requests.get(
            poster_url,
            headers=img_headers,
            timeout=15
        )

        if img_response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(img_response.content)
            print(f"  海报已下载: {filepath}")
            return filepath
        else:
            print(f"  海报下载失败，状态码: {img_response.status_code}")
            return None

    except Exception as e:
        print(f"  海报下载异常: {e}")
        return None


# =========================
# 保存影片元数据
# =========================
def save_movie_meta(movie_name, movie_id, poster_url):
    """保存影片元数据到 data/movies/<movie_name>/meta.json"""
    folder = os.path.join(MOVIES_DIR, movie_name)
    os.makedirs(folder, exist_ok=True)

    data = {
        "name": movie_name,
        "id": movie_id,
        "poster_url": poster_url,
        "poster_local": os.path.join(POSTERS_DIR, f"{movie_name}.jpg")
    }

    filepath = os.path.join(folder, "meta.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  影片元数据已保存: {filepath}")


# =========================
# 读取影片元数据
# =========================
def load_movie_meta(movie_name):
    """读取影片元数据"""
    filepath = os.path.join(MOVIES_DIR, movie_name, "meta.json")

    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# 完整流程：获取并保存海报
# =========================
def fetch_and_save_poster(movie_name, movie_id):
    """获取海报 URL、下载图片、保存元数据"""

    # 先检查本地是否已经有海报
    local_path = os.path.join(POSTERS_DIR, f"{movie_name}.jpg")
    meta_path = os.path.join(MOVIES_DIR, movie_name, "meta.json")

    if os.path.exists(local_path) and os.path.exists(meta_path):
        print(f"  海报已存在，跳过")
        return load_movie_meta(movie_name)

    print(f"  正在获取 {movie_name} 的海报...")
    poster_url = fetch_poster_url(movie_id)

    if poster_url:
        download_poster(movie_name, poster_url)
        save_movie_meta(movie_name, movie_id, poster_url)
    else:
        # 即使没有海报也保存基本信息
        save_movie_meta(movie_name, movie_id, None)

    return load_movie_meta(movie_name)
