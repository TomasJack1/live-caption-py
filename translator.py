import httpx

from settings import get_settings


class BergamotTranslator:
    client = httpx.Client()
    settings = get_settings()

    @classmethod
    def translate(cls, text) -> str:
        """调用后端翻译服务

        Args:
            text (_type_): 翻译后的文本

        Returns:
            str: _description_
        """
        server_ip = cls.settings.value("server_ip")
        server_port = cls.settings.value("server_port")
        response = cls.client.post(
            url=f"http://{server_ip}:{server_port}/translate",
            json={
                "text": text,
            },
        )

        return response.json().get("result")
