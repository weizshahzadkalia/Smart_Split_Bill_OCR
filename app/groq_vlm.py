#VLM yang kedua adalah Groq

import os
import json
import base64
import time

from groq import Groq
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def encode_image(image):

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    return base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

def extract_receipt_groq(image):

    prompt = """
    Extract receipt information.

    Return ONLY valid JSON.

    {
      "store_name":"",
      "date":"",
      "items":[
        {
          "item_name":"",
          "quantity":0,
          "unit_price":0,
          "amount":0
        }
      ],
      "subtotal":0,
      "tax":0,
      "total":0
    }
    """

    base64_image = encode_image(image)

    start = time.perf_counter()

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",

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
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    runtime = time.perf_counter() - start

    return (
        response.choices[0].message.content,
        runtime
    )