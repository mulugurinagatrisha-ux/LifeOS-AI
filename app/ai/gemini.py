import time
from google import genai
from app.config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

MODELS = [
    "gemini-3.5-flash-lite"
]


def ask_ai(prompt):
    """
    General AI function
    Used by:
    - AI Chat
    - Voice Assistant
    - Goal Coach
    - Diet Planner
    - Expense Suggestions
    """

    last_error = None

    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response and response.text:
                    return response.text.strip()

            except Exception as e:
                last_error = e
                print(f"[{model}] Attempt {attempt+1}: {e}")
                time.sleep(2)

    return f"⚠️ AI service unavailable.\n{last_error}"