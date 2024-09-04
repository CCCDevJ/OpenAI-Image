import google.generativeai as genai
import os
from dotenv import load_dotenv
import pathlib

media = pathlib.Path(__file__).parents[1] / "img"

# Load environment variables
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# model = genai.GenerativeModel('gemini-1.5-flash')
# response = model.generate_content("The opposite of hot is")
# print(response.text)

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
image_prompt += "includes Product Dimension like height, width, overall"
image_prompt += "only in json format"

# image_prompt = "Give me all information about image like what is dimensions of objects in image, height, width, capacity, color of object, type of furniture used, material used in image etc."
image_prompt =("Analyze the provided image and identify all the furniture Sofa items present. For each furniture item, return the following details in JSON format:"
               "Name: The common name or type of the furniture.)"
               "Category: The category it belongs to (e.g., chair, table, sofa)."
               "Material: The primary material the furniture is made from (e.g., wood, metal, fabric)."
               "Color: The color or primary colors of the furniture."
               "Dimensions: The approximate dimensions (height, width, depth) in inch."
               "Condition: Describe whether the furniture appears new, used, or vintage."
               "Additional Features: Any other notable features such as adjustability, upholstery details, etc.")
print(image_prompt)

myfile = genai.upload_file(media / "Tulen+Reclining+Sofa.webp")
print(f"{myfile=}")

model = genai.GenerativeModel("gemini-1.5-flash")
result = model.generate_content(
    [myfile, "\n\n", image_prompt]
)
print(f"{result.text=}")