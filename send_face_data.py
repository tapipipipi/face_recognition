import requests
import json
import os
from dotenv import load_dotenv

num = [
    123, 456, 333
]

#POSTで渡すデータをJSON形式に変換して送信
req = requests.post("SERVER_URL", data={'testdata': json.dumps(num)})

print(req.text)