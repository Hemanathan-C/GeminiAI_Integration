from openai import OpenAI
from env import OPEN_API_KEY

open_ai_client = OpenAI(
    apikey = OPEN_API_KEY
)

user_input = input("Enter an public image URL to generate an caption (50 words): ")

response = open_ai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate an caption for this image in 50 words."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": str(user_input)
                    }
                }
            ]
        }
    ]
)

print("Response : ",response.choices[0].message.content)