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
model = "gpt-4o"
# model = "gpt-4o-mini"

# Open AI Client
client = OpenAI(api_key=openai_api_key)

attributes = {
    "Product Type": ["Convertible Sofa", "Sleeper", "Loveseat"],
    "Sofa Design": ["Sofa Bed / Sleeper", "Reclining"],
    "Back Type": ["Cushioned", "Pillow Back"],
    "Seat Style": ["Multiple Cushion Seat"],
    "Arm Type": ["Flared Arms", "Pillow Top Arms"],
    "Leg Color / Finish": ["Black", "Sleeper"],
    "Upholstered": ["Yes", ],
    "Frame Materia": ["Metal", "Metal; Solid + Manufactured Wood", "Manufactured Wood"],
    "Fill Material": ["Foam", "Foam; Cotton"],
    "Back Fill Material": ["Foam", "Foam; Cotton"],
    "SeatingCapacity": ["3", "2"]
}

# Convert attributes to a string format
attribute_description = (
    f"Product Type: {', '.join(attributes['Product Type'])}. "
    f"Sofa Design: {', '.join(attributes['Sofa Design'])}. "
    f"Back Type: {', '.join(attributes['Back Type'])}."
    f"Seat Style: {', '.join(attributes['Seat Style'])}."
    f"Arm Type: {', '.join(attributes['Arm Type'])}."
    f"Leg Color / Finish: {', '.join(attributes['Leg Color / Finish'])}."
    f"Upholstered: {', '.join(attributes['Upholstered'])}."
    f"Frame Materia: {', '.join(attributes['Frame Materia'])}."
    f"Fill Material: {', '.join(attributes['Fill Material'])}."
    f"Back Fill Material: {', '.join(attributes['Back Fill Material'])}."

    f"SeatingCapacity: {', '.join(attributes['SeatingCapacity'])}."
)

# image_prompt = "You are a cool image analyst.  Your goal is to describe sofa in this image."

image_prompt = f"You are an image analysis expert. The attributes of the image are: {attribute_description}."
image_prompt += "Add an additional attributes your self. No extra description needed. Select any one value from options for each attribute."
image_prompt += "only in json formate"

image_prompt =("Analyze the provided image and identify all the furniture Sofa items present. For each furniture item, return the following details in JSON format:"
               "Name: The common name or type of the furniture.)"
               "Category: The category it belongs to (e.g., chair, table, sofa)."
               "Material: The primary material the furniture is made from (e.g., wood, metal, fabric)."
               "Color: The color or primary colors of the furniture."
               "Dimensions: The approximate dimensions (height, width, depth) in inch."
               "Condition: Describe whether the furniture appears new, used, or vintage."
               "Additional Features: Any other notable features such as adjustability, upholstery details, etc.")
print(image_prompt)

system_role = {
    "role": "system",
    "content": [
        {
            "type": "text",
            "text": image_prompt
        }
    ],
}
max_token = 1000


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
                system_role,
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": max_token
        }

        # Send the request to OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        json_response = response.json()
        # Return the response from OpenAI API
        return {"status": 200, "response": json_response["choices"][0]["message"]["content"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to analyze multiple uploaded images
@app.post("/analyze-uploads/")
async def analyze_uploaded_images(prompt: str = Form(...), images: List[UploadFile] = File(...)):
    try:
        # Build the messages with images and prompt
        messages = [
            system_role,
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ]
        for image in images:
            # Read and encode the image to base64
            image_data = await image.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            messages[1]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })

        # Create the payload for the OpenAI API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_token
        }

        # Send the request to OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        json_response = response.json()
        # Return the response from OpenAI API
        # return JSONResponse(content=json_response["choices"][0]["message"]["content"])
        return {"status": 200, "response": json_response["choices"][0]["message"]["content"]}

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

# Prompt
# Give me all information about image like what is dimensions of objects in image, height, width, capacity, color of object, type of furniture used, material used in image etc.
# is this images are same give me answer only in true or false.
# is this images are same give me answer only in true or false, give similarity percentage, if false then give proper reason
# is this images are same give me answer only in true or false,give similarity percentage if false then give proper reason, all answers in json formate with proper keys, result: boolean, similarity_percentage: float, reason: string
