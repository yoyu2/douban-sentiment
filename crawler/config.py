import os

# =========================
# 豆瓣电影配置
# =========================

MOVIE_ID = "1292052"

BASE_URL = (
    f"https://movie.douban.com/subject/"
    f"{MOVIE_ID}/comments"
)

# 爬取页数
MAX_PAGES = 20

# 每页20条
PAGE_SIZE = 20

# =========================
# 用户自定义配置（从项目根目录 .env 或环境变量读取）
# =========================

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_env_file():
    """加载项目根目录下的 .env 文件（不依赖第三方库）。"""
    env_path = os.path.join(_PROJECT_ROOT, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()

# 后端上传接口（默认本机后端）
UPLOAD_URL = os.environ.get("UPLOAD_URL", "http://127.0.0.1:8000/api/upload")

# 豆瓣登录 Cookie（可选，不填则请求可能被限流/反爬）
_DOUBAN_COOKIE = os.environ.get("DOUBAN_COOKIE", "")

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Cookie": _DOUBAN_COOKIE,
}
