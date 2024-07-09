# 顔認証（複数・画像）

#ライブラリのインポート
import numpy as np
import os
import cv2
from insightface.app import FaceAnalysis
from glob import glob
from tqdm import tqdm
from collections import defaultdict
from PIL import Image
from datetime import datetime
import urllib.request
import requests
import requests
from bs4 import BeautifulSoup

#平均を算出するための関数
def get_averages(names, scores):
    d = defaultdict(list) #空のリストを作成
    for n, s in zip(names, scores): #名前とスコアを同時に取得
        d[n].append(s) #リストに名前とスコアを追加

    averages = {}
    for n, s in d.items(): #namesとscoresに対してループ処理
        averages[n] = np.mean(s) #平均を算出
    return averages

#認証を行うための関数
def judge_sim(known_embeddings, known_names, unknown_embeddings, threshold):
    pred_names = [] #リストを生成
    for emb in unknown_embeddings:
        scores = np.dot(emb, known_embeddings.T)
        scores = np.clip(scores, 0., None)

        averages = get_averages(known_names, scores)
        pred = sorted(averages, key=lambda x: averages[x], reverse=True)[0]
        print(averages)
        score = averages[pred]

        if score > threshold:
            pred_names.append(pred)
        else:
            pred_names.append(None)
    
    return pred_names

#バウンディングボックスと名前を描画するための関数
def draw_on(img, faces, name):
    dimg = img.copy()
    for i in range(len(faces)):
        face = faces[i]
        box = face.bbox.astype(int)
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
        if face.kps is not None:
            kps = face.kps.astype(int)
            #print(landmark.shape)
            for l in range(kps.shape[0]):
                color = (0, 0, 255)
                if l == 0 or l == 3:
                    color = (0, 255, 0)
                cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color, 2)
        cv2.putText(dimg, name[i], (box[0]-1, box[1]-4),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)
    return dimg

#取得した画像を自分のディレクトリに保存するための関数
def download_file(url, dst_path):
    with urllib.request.urlopen(url) as web_file:
        with open(dst_path, 'wb') as local_file:
            local_file.write(web_file.read())

#名前と特徴量を格納するためのリストの初期化
known_names = []
known_embeddings = []
unknown_embeddings = []

# スクレイピング対象の URL にリクエストを送り HTML を取得する
res = requests.get('https://yu-windows.tail62876.ts.net/B/.face_images/')

# 取得したHTMLをパース
soup = BeautifulSoup(res.text, 'html.parser')

#ページに含まれるリンクを全て取得
link = [url.get('href') for url in soup.find_all('a')]

#.jpgのリンクのみを抽出し、dataディレクトリに保存
for i in link:
    if ".jpg" in i:
        url = 'https://yu-windows.tail62876.ts.net/B/.face_images/' + i
        dst_path = 'data/' + i
        download_file(url, dst_path)

#フォルダの名前（選手名）を取得
dir_path = "data"
players = os.listdir(dir_path)

#カメラの設定
# capture = cv2.VideoCapture(0)

# #顔認証用の写真を撮影
# while True:
#     ret, flame = capture.read()

#     if(ret == False):
#         continue
#     else:
#         break

#認証させる画像の登録
img_path = 'authe_image/arasm.jpg'
img = cv2.imread(img_path)

#登録写真の顔検出を行うための準備
app_pre = FaceAnalysis()
app_pre.prepare(ctx_id=0, det_size=(640, 640))

#認証写真の顔検出を行うための準備
app = FaceAnalysis()
app.prepare(ctx_id=0, det_size=(640, 640))

#顔の特徴量を抽出し、リストに追加
for player in tqdm(players):
    player_embeddings, player_names = [], []
    
    # 画像の読み込み
    im = cv2.imread(f'face_data/{player}')
    if im is None: continue #画像がない場合

    #顔を検出しリストに追加
    faces = app_pre.get(np.array(im)) 
    if len(faces) == 0 : continue #顔が検出されない場合
    player_embeddings.append(faces[0].embedding)
    player_names.append(player)
    
    #対応した名前をリストに追加
    player_embeddings = np.stack(player_embeddings, axis=0)
    known_embeddings.append(player_embeddings)
    known_names += player_names
known_embeddings = np.concatenate(known_embeddings, axis=0)#情報を１つの配列に格納

#顔認証の実施
faces = app.get(np.array(img))

for i in range(len(faces)):
    unknown_embeddings.append(faces[i].embedding) #認証画像をリストに追加

    #認証画像、登録画像、名前を用いて顔認証を実施
    pred_names = judge_sim(known_embeddings, known_names, unknown_embeddings, 90)
detect = draw_on(img, faces, pred_names) #認証できた顔と名前を元の画像に描画

attend_data = [] #認証成功した画像名を格納するためのリスト

#.jpgを切り離し画像名のみ格納
for i in pred_names:
    if(i != None):
        print(i)
        sla_split = str(i).split(".")
        attend_data.append(sla_split[0])
print("\nlistdata:" + attend_data)#結果を出力

#現在時刻を取得し、顔認証結果をresultディレクトリに保存
datetime_str = datetime.now().strftime("%Y %m-%d %H-%M %S")
cv2.imwrite( "result/" + str(datetime_str) + '.jpg', detect)