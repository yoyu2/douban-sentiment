import os

from openai import OpenAI


# =========================
# 大模型接口配置（用户自行提供）
# =========================
# 在项目根目录的 .env 文件中填写（或直接设置环境变量）：
#   LLM_API_KEY  = 你的 API Key（必填）
#   LLM_BASE_URL = API 服务地址（可选，默认 https://api.deepseek.com）
#   LLM_MODEL    = 模型名称（可选，默认 deepseek-chat）
#
# 支持所有 OpenAI 兼容接口（DeepSeek / OpenAI / Moonshot / 通义千问 等），
# 只需修改 base_url 和 model 即可切换。

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"

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


def _get_client():
    """根据配置创建 OpenAI 兼容客户端，返回 (client, model)。"""
    api_key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "未配置大模型 API Key。请在项目根目录的 .env 文件中设置 "
            "LLM_API_KEY=你的密钥，或设置环境变量 LLM_API_KEY。"
        )
    base_url = os.environ.get("LLM_BASE_URL") or DEFAULT_BASE_URL
    model = os.environ.get("LLM_MODEL") or DEFAULT_MODEL
    return OpenAI(api_key=api_key, base_url=base_url), model


# =========================
# 单条评论情感分析
# =========================
def analyze_sentiment(text):
    client, model = _get_client()

    prompt = (
        "请分析下面影评的情感倾向。\n\n"
        "只返回以下三种之一：\n\n"
        "positive\nnegative\nneutral\n\n"
        f"影评：\n{text}\n"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.1,
    )

    result = response.choices[0].message.content.strip().lower()

    if result not in ("positive", "negative", "neutral"):
        print(f"  ⚠ 模型返回非预期结果: {result!r}，按 neutral 处理")
        return "neutral"

    return result
