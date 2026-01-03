import os
import requests


class AIClient:
    """
    Gemini AI Client (REST, stable, v1)
    """

    def __init__(self):
        self.api_key = os.getenv("REDSENTINEL_AI_KEY")
        if not self.api_key:
            raise EnvironmentError("REDSENTINEL_AI_KEY not set")

        self.api_url = (
            "https://generativelanguage.googleapis.com/v1/models/"
            "gemini-1.5-flash:generateContent"
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{system_prompt}\n\n{user_prompt}"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 800
            }
        }

        response = requests.post(
            f"{self.api_url}?key={self.api_key}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

