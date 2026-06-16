import time
import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def extract_receipt(image):

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

    start = time.perf_counter()
    response = model.generate_content(
        [
            prompt,
            image
        ]
    )

    runtime = time.perf_counter() - start
    return response.text, runtime