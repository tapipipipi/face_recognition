# 顔認証（個人のみ）

#必要なライブラリのインポート
import cv2
import numpy as np
import time
import os
from insightface.app import FaceAnalysis

#顔認証用の写真を登録
dir_path = "face_data"

#フォルダ内にある写真のパスを取得
files = os.listdir(dir_path)

#類似度の算出のための関数（コサイン類似度）
def cos_sim(feat1, feat2):
    return np.dot(feat1, feat2) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))

#検出ボックスと名前を描画するための関数
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
        cv2.putText(dimg, name, (box[0]-1, box[1]-4),cv2.FONT_HERSHEY_COMPLEX,1.5,(0,255,0),2)
    return dimg

#顔検出をするカメラの指定
capture = cv2.VideoCapture(0)

#顔検出のオブジェクトのインスタンス化
app = FaceAnalysis()
app.prepare(ctx_id=1, det_size=(640, 640))

#カメラ画像から顔の検出と特徴量の抽出
while True:
    ret, flame = capture.read()

    #顔の検出ができているかの判定
    try:
        faces = app.get(flame)
        embeddings = faces[0].embedding
        #顔の検出に失敗した場合
    except IndexError: 
        print("face_false")
        time.sleep(0.5)
        continue

    #顔が認識されている場合
    if faces is not None:
        print("face_true")
        break

for f in files:
    #画像のパス指定と閾値の設定
    pre_img_path = "face_data/" + f
    print(pre_img_path)
    threshold = 0.75

    #画像の読み込みと特徴量の抽出
    pre_img = cv2.imread(pre_img_path)
    pre_face = app.get(pre_img)
    pre_embedding = [pre_face[0].embedding]

    #顔認証ができているかの判定
    known_face_name = ["Unknown", "success"]

    #類似度算出
    sim = cos_sim(pre_embedding, embeddings)

    #閾値を超えた際に、登録された人物であると判定
    if sim >= threshold:
        best_name_index = pre_embedding.index(pre_embedding[0]) + 1

        #結果を表示し処理を停止
        print(known_face_name[best_name_index])

        break
    else:
        best_name_index = 0

    #結果の表示
    print(known_face_name[best_name_index])