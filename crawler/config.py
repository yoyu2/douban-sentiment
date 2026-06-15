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

# 后端接口
UPLOAD_URL = "http://47.113.193.26/api/upload"


# 请求头
HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    "Cookie":'***REMOVED***'
}