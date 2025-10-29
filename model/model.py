import os
from config import HUGGINGFACEHUB_API_TOKEN
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HUGGINGFACEHUB_API_TOKEN,
)

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1:novita",
    messages=[
        {
            "role": "user",
            "content": "ты говоришь по русски?"
        }
    ],
)

print(completion.choices[0].message)