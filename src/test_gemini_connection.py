
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(dotenv_path=".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing.")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=15000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)

try:
    print("Testing Gemini 3.6 Flash...", flush=True)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=(
            "Reply with exactly: "
            "YojanaRAG Gemini connection successful"
        ),
        config=types.GenerateContentConfig(
            temperature=0,
            max_output_tokens=100
        )
    )

    print("Gemini response:", response.text)

except Exception as error:
    print("Gemini generation failed:")
    print(type(error).__name__)
    print(str(error)[:1200])

finally:
    client.close()



