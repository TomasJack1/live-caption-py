import time

import httpx

if __name__ == "__main__":
    with httpx.Client() as client:
        start_time = time.time()
        response = client.post(
            url="http://localhost:8989/translate",
            json={
                "from": "ja",
                "to": "zh",
                "text": "慎吾がYouTubeを始めたよ！",
            },
            headers={
                "Authorization": "",
            },
        )

        response = response.json()

        print(time.time() - start_time)
        print(response)
        print(response["result"])
