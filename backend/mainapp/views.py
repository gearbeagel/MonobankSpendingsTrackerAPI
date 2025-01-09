import os
import time
import hmac
import hashlib
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY = os.getenv('MONO_X_TOKEN')
print(PRIVATE_KEY)


def generate_signature(timestamp, url):
    data = (timestamp + url).encode('utf-8')
    sign = hmac.new(PRIVATE_KEY.encode('utf-8'), data, hashlib.sha256).digest()
    signB64 = base64.b64encode(sign).decode('utf-8')
    return signB64


def get_current_time():
    return str(int(time.time()))


class MainView(APIView):
    def get(self, request):
        return Response('Hello from Mono!')


class MonobankAuthAPIView(APIView):

    def get(self, request):
        return Response('Register with your Mono account!')

    def post(self, request):
        api_key_id = PRIVATE_KEY
        print(api_key_id)
        callback_url = "https://api.monobank.ua/personal/auth/request"
        current_time = get_current_time()
        sign = generate_signature(current_time, callback_url)

        headers = {
            "X-Key-Id": api_key_id,
            "X-Time": current_time,
            "X-Sign": sign,
            "X-Callback": callback_url,
        }

        response = requests.post(callback_url, headers=headers)

        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response(response.json(), status=response.status_code)
