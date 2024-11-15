import base64
from openai import OpenAI

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_defect(image_path, defect_list, white_list):
  # Path to your image
  
  # Getting the base64 string
  base64_image = encode_image(image_path)

  prompt = "Is there a defect in this fabric? Say yes if there's a >= 65% chance of defect, otherwise no. \
              Please provide a reason for your response and explain approximately where you see the defect in the image."

  if (defect_list):
    prompt += "Also call out the defect type from the following list: " + defect_list

  if (white_list):
    prompt += "The following are not considered defects: " + white_list

  print("PROMPT: ", prompt)
              
  
  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
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
  print(response.choices[0].message.content, is_defective)
  return {
    "is_defective": is_defective,
    "reason": response.choices[0].message.content
  }


image_path = "../datasets/defective/hole/34.jpg"
#get_defect(image_path)