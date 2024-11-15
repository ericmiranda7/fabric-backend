import base64
from openai import OpenAI

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_defect(image_path):
  # Path to your image
  
  # Getting the base64 string
  base64_image = encode_image(image_path)
  
  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Is there a chance that there might be a defect in this fabric? Include yes in your response.",
          },
          {
            "type": "image_url",
            "image_url": {
              "url":  f"data:image/jpeg;base64,{base64_image}"
            },
          },
        ],
      }
    ],
  )
  
  is_defective = response.choices[0].message.content.lower().find("yes") != -1
  print(is_defective)
  return is_defective


image_path = "../datasets/defective/hole/34.jpg"
#get_defect(image_path)