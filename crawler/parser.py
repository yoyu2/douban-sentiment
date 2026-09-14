from bs4 import BeautifulSoup

def parse_comments(html):
    soup = BeautifulSoup(html, "html.parser")

    comments = []

    items = soup.find_all("div", class_="comment-item")

    for item in items:

        # 评论内容
        content_tag = item.find("span", class_="short")

        # 时间
        time_tag = item.find("span", class_="comment-time")

        # 评分
        rating_tag = item.find("span", class_=lambda x: bool(x and "rating" in x))

        content = (
            content_tag.get_text(strip=True)
            if content_tag else ""
        )

        comment_time = (
            time_tag.get_text(strip=True)
            if time_tag else ""
        )

        rating = (
            rating_tag["class"][0]
            if rating_tag else "unknown"
        )

        if content:
            comments.append({
                "content": content,
                "time": comment_time,
                "rating": rating
            })

    return comments