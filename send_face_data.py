import requests
import json

num = [
    123, 456, 789
]

#POSTで渡すデータをJSON形式に変換して送信
req = requests.post("https://yu-windows.tail62876.ts.net/B/face_attend.php", data={'testdata': json.dumps(num)})

print(req.text)