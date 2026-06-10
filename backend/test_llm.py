from llm_service import analyze_sentiment


texts = [

    "这部电影驱散了我的困意",

    "剧情看开头就猜得出结尾",

    "中不溜吧"
]


for text in texts:

    result = analyze_sentiment(text)

    print(f"\n评论: {text}")

    print(f"情感: {result}")