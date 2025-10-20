# import transformers
# import torch

# model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

# pipeline = transformers.pipeline(
#     "text-generation",
#     model=model_id,
#     model_kwargs={"torch_dtype": torch.bfloat16},
#     device_map="auto",
# )

# messages = [
#     {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
#     {"role": "user", "content": "Who are you?"},
# ]

# outputs = pipeline(
#     messages,
#     max_new_tokens=256,
# )
# # Вместо print(outputs[0]["generated_text"][-1])
# with open('model/generated_text.txt', 'w', encoding='utf-8') as f:
#     f.write(outputs[0]["generated_text"][-1])


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