import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(user_question):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for motorsports pit stop data."},
                {"role": "user", "content": user_question}
            ],
            temperature=0.3,
        )
        print(f"GPT response: {response}")
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error querying GPT: {e}"
