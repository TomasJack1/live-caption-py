import deepl
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


class DeeplTranslator:
    auth_key = "d30c7c54-dd98-461e-9cef-53e228e90572:dp"
    server_url = "https://api.deepl-pro.com"
    translator = deepl.Translator(auth_key, server_url=server_url)

    @classmethod
    def translate(cls, text) -> str:
        """调用后端翻译服务

        Args:
            text (_type_): 翻译后的文本

        Returns:
            str: _description_
        """
        result = cls.translator.translate_text(
            text,
            source_lang="JA",
            target_lang="ZH",
        )
        return result.text
