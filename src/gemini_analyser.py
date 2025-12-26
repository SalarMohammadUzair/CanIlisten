# this is the most important part, we will use an api from gemini ai studio t o analyse the lyrics.
#whoo-hoo
import os
import json
from pathlib import Path
from dotenv import load_dotenv
#import google.generativeai as genai # this library got deprecated :(
from google import genai # this is the new one

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
client = genai.Client(api_key=GEMINI_API_KEY)
# genai.configure(api_key=GEMINI_API_KEY)
model = ("gemini-flash-latest")
#genai.GenerativeModel
def load_prompt():
    prompt_path = Path(__file__).resolve().parent / "prompt.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"file not found: {prompt_path}")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def analysis(artist, lyrics):
    prompt_template = load_prompt()
    full_prompt = prompt_template + "\n" + artist + "\n" + lyrics
    try: 
        response = client.models.generate_content(
            model=model,
            contents=full_prompt,
            config={
                "temperature": 0.1,
                "response_mime_type": "application/json"

            }
        )
        result = json.loads(response.text)
        return result
    except json.JSONDecodeError as e:
        print(f"Failed to parse Gemini respone: {e}")
        print(f"raw response: {response.text}")
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None
# test this file standalone  
if __name__ == "__main__":
    test_lyrics = "I love you, you love me, we are happy"
    result = analysis("Test Artist", test_lyrics)
    print("Result:", result)