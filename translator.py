# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys
import time
from pathlib import Path
from typing import List

import httpx

# import torch
# import intel_extension_for_pytorch as ipex
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_util import models as util_models
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline


class AliyunTranslator:
    """阿里云翻译器"""

    @staticmethod
    def create_client() -> OpenApiClient:
        """使用凭据初始化账号Client

        @return: Client
        @throws Exception
        """
        # 工程代码建议使用更安全的无AK方式，凭据配置方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            access_key_id=os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        )

        # Endpoint 请参考 https://api.aliyun.com/product/alimt
        config.endpoint = f"mt.cn-hangzhou.aliyuncs.com"
        return OpenApiClient(config)

    @staticmethod
    def create_api_info() -> open_api_models.Params:
        """API 相关

        @param path: string Path parameters
        @return: OpenApi.Params
        """
        return open_api_models.Params(
            # 接口名称,
            action="TranslateGeneral",
            # action="Translate",
            # 接口版本,
            version="2018-10-12",
            # 接口协议,
            protocol="HTTPS",
            # 接口 HTTP 方法,
            method="POST",
            auth_type="AK",
            style="RPC",
            # 接口 PATH,
            pathname=f"/",
            # 接口请求体内容格式,
            req_body_type="formData",
            # 接口响应体内容格式,
            body_type="json",
        )

    @classmethod
    def translate(cls, text) -> dict:
        client = cls.create_client()
        params = cls.create_api_info()
        # body params
        body = {}
        body["FormatType"] = "text"
        body["SourceLanguage"] = "ja"
        body["TargetLanguage"] = "zh"
        body["SourceText"] = text
        body["Scene"] = "general"
        # body["Scene"] = "social"
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(body=body)
        # 返回值实际为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
        return client.call_api(params, request, runtime)["body"]["Data"]["Translated"]


class NLLPTranslator:
    """NLLP模型翻译器"""

    @classmethod
    def translate(cls, text):
        if not hasattr(cls, "_translator"):
            # 加载预训练的分词器和模型
            tokenizer = AutoTokenizer.from_pretrained("./models/nllb-200-distilled-600M", token=True)
            model = AutoModelForSeq2SeqLM.from_pretrained("./models/nllb-200-distilled-600M", token=True)
            # model = ipex.optimize(
            #     model,
            #     dtype=torch.bfloat16,  # 保持 BF16 精度
            #     graph_mode=True,  # 启用图优化
            #     weights_prepack=True,  # 预打包权重
            # )

            cls._translator = pipeline(
                "translation",
                model=model,
                tokenizer=tokenizer,
                src_lang="ja_Latn",
                tgt_lang="zho_Hans",
                max_length=50,
                device=0 if torch.xpu.is_available() else -1,
            )

        return cls._translator(text)


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


if __name__ == "__main__":
    import asyncio
    from pathlib import Path

    from dotenv import load_dotenv

    CURRENT_DIR = Path(__file__).parent.resolve()

    load_dotenv(CURRENT_DIR / ".env", verbose=True)
    asyncio.run(AliyunTranslator.translate_async("慎吾がYouTubeを始めたよ！"))
