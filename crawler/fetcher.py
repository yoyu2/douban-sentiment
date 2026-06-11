import requests
import time

from config import HEADERS


session = requests.Session()


def fetch_page(url):
    try:
        response = session.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 200:
            return response.text

        return None

    except Exception as e:
        print("请求异常:", e)
        return None