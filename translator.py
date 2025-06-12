import httpx


class MTranslator:
    client = httpx.Client()

    @classmethod
    def translate(cls, text, src="ja", tgt="zh"):
        response = cls.client.post(
            url="http://localhost:8989/translate",
            json={
                "from": src,
                "to": tgt,
                "text": text,
            },
            headers={
                "Authorization": "",
            },
        )

        return response.json().get("result")
