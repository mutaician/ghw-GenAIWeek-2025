
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.clarifai.com/v2/ext/openai/v1",
    api_key="6da7e0a6b6b54bc285c21ef2f91427a7",
)
response = client.chat.completions.create(
    model="https://clarifai.com/meta/Llama-3/models/Llama-3_2-3B-Instruct",
    messages=[
        {"role": "developer", "content": "Talk like a pirate."},
        {
            "role": "user",
            "content": "How do I check if a Python object is an instance of a class?",
        },
    ],
    temperature=0.7,
    stream=False, # stream=True also works, just iterator over the response
)
print(response)
