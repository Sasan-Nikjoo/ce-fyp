from google import genai
from google.genai import types

api_key = "MY_API_KEY_HERE"

client = genai.Client(api_key=api_key)

image_name = "test.jpg"

try:
    with open(image_name, "rb") as f:
        img = f.read()

    prompt = "Describe this image in detail and name some items you can see."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            types.Part.from_bytes(data=img, mime_type="image/jpeg"),
        ],
    )

    print(response.text)

except Exception as e:
    print(f"Error: {e}")