from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": "https://cdn.1stopbedrooms.com/media/i/raw/catalog/product/t/u/tulen-reclining-sofa-in-gray_qb1188631_53.jpg",
                },
            ],
        }
    ],
    max_tokens=300,
)

print(response.choices[0])
