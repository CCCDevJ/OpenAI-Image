from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from openai import OpenAI
import base64
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set up OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Setup model
# model = "gpt-4o"
model = "gpt-4o-mini"

# Open AI Client
client = OpenAI(api_key=openai_api_key)


# Endpoint to analyze image from URL
@app.post("/analyze-url/")
async def analyze_image_url(image_url: str = Form(...), prompt: str = Form(...)):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": image_url},
                    ],
                }
            ],
            max_tokens=300,
        )

        return JSONResponse(content=response.choices[0].get('message', {}))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to analyze multiple images from URLs
@app.post("/analyze-urls/")
async def analyze_image_urls(image_urls: List[str] = Form(...), prompt: str = Form(...)):
    try:
        # Build the messages with images and prompt
        messages = [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ]
        for url in image_urls:
            messages[0]["content"].append({"type": "image_url", "image_url": url})

        # Send the request to OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=300,
        )

        return JSONResponse(content=response.choices[0].get('message', {}))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to analyze uploaded image
@app.post("/analyze-upload/")
async def analyze_uploaded_image(prompt: str = Form(...), image: UploadFile = File(...)):
    try:
        # Read the uploaded image file
        image_data = await image.read()

        # Encode the image to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')

        # Create the payload for the OpenAI API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                    ]
                }
            ],
            "max_tokens": 300
        }

        # Send the request to OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Return the response from OpenAI API
        return JSONResponse(content=response.json())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to analyze multiple uploaded images
@app.post("/analyze-uploads/")
async def analyze_uploaded_images(prompt: str = Form(...), images: List[UploadFile] = File(...)):
    try:
        # Build the messages with images and prompt
        messages = [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ]
        for image in images:
            # Read and encode the image to base64
            image_data = await image.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            })

        # Create the payload for the OpenAI API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 300
        }

        # Send the request to OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Return the response from OpenAI API
        return JSONResponse(content=response.json())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Image Analysis API"}


# To run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# Multiple API Calls
# curl -X POST "http://127.0.0.1:8000/analyze-urls/" \
# -H "accept: application/json" \
# -H "Content-Type: application/x-www-form-urlencoded" \
# -d "image_urls[]=https://example.com/image1.jpg&image_urls[]=https://example.com/image2.jpg&prompt=What are in these images?"


# curl -X POST "http://127.0.0.1:8000/analyze-uploads/" \
# -H "accept: application/json" \
# -F "images=@path/to/your/image1.jpg" \
# -F "images=@path/to/your/image2.jpg" \
# -F "prompt=What are in these images?"
