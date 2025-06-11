from pathlib import Path

import httpx


class MTranslator:
    client = httpx.Client()

    @classmethod
    def translate(cls, text):
        response = cls.client.post(
            url="http://localhost:8989/translate",
            json={
                "from": "ja",
                "to": "zh",
                "text": text,
            },
            headers={
                "Authorization": "",
            },
        )

        return response.json().get("result")
