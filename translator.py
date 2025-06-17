import httpx


class BergamotTranslator:
    client = httpx.Client()

    @classmethod
    def translate(cls, text):
        response = cls.client.post(
            url="http://localhost:8080/translate",
            json={
                "text": text,
            },
        )

        return response.json().get("result")
