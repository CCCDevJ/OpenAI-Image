import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
# print(OPENAI_FREE_KEY)

payload = {"model": "gpt-3.5-turbo",
           "messages": [
               {"role": "system",
                "content": [{"type": "text",
                             "text": "You are a cool image analyst.  Your goal is to describe what is in this image."}],
                },
               {
                   "role": "user",
                   "content": [
                       {
                           "type": "text",
                           "text": "Give me all information about image like what is dimentions of objects in image, height, widhth, capacity, color of object, type of furniture used, matirial used in image etc."
                       },
                       {
                           "type": "image_url",
                           "image_url": {
                               "url": "https://cdn.1stopbedrooms.com/media/i/raw/catalog/product/t/u/tulen-reclining-sofa-in-gray_qb1188631_53.jpg"
                           }
                       }
                   ]
               }
           ],
           "max_tokens": 500
           }

headers = {"Authorization": f"Bearer {OPENAI_KEY}",
           "Content-Type": "application/json"}

response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)
r = response.json()
print(r)
print(r["choices"][0]["message"]["content"])
