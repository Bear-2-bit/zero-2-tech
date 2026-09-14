import json

from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url="https://api.deepseek.com",
)


SYSTEM_PROMPT = """
你是一个学习任务拆解助手。

用户会给出一个学习目标。

请把目标拆解成 4 到 8 个清晰、可执行、按顺序排列的学习步骤。

必须严格输出 JSON。

JSON 格式如下：

{
  "steps": [
    "步骤1",
    "步骤2",
    "步骤3"
  ]
}

不要输出 Markdown。
不要输出解释。
只返回 JSON。
"""


def decompose_goal(goal: str) -> list[str]:
    response = client.chat.completions.create(
        model=settings.deepseek_model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": goal,
            },
        ],
        response_format={
            "type": "json_object"
        },
        max_tokens=800,
        extra_body={
            "thinking": {
                "type": "disabled"
            }
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "DeepSeek returned empty content"
        )

    data = json.loads(content)

    steps = data.get("steps")

    if not isinstance(steps, list):
        raise ValueError(
            "Invalid DeepSeek response format"
        )

    return steps