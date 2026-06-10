from openai import OpenAI


client = OpenAI(

    api_key="***REMOVED***",

    base_url="https://api.deepseek.com"
)


# =========================
# 单条评论情感分析
# =========================
def analyze_sentiment(text):

    prompt = f"""
请分析下面影评的情感倾向。

只返回以下三种之一：

positive
negative
neutral

影评：
{text}
"""

    response = client.chat.completions.create(

        model="deepseek-chat",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.1
    )

    result = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    return result