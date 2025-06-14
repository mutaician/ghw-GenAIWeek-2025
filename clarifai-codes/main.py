import os
from clarifai.client import Model
from dotenv import load_dotenv

load_dotenv()

# Set your Personal Access Token (PAT) from .env
clarifai_pat = os.getenv("CLARIFAI_PAT")
if clarifai_pat:
    os.environ["CLARIFAI_PAT"] = clarifai_pat
else:
    raise EnvironmentError("CLARIFAI_PAT not found in .env file.")

# Initialize with model URL
model = Model(url="https://clarifai.com/meta/Llama-3/models/Llama-3_2-3B-Instruct")

response_stream = model.generate(
    prompt="What are the limitations of AI"
)

for text_chunk in response_stream:
    print(text_chunk, end="", flush=True)