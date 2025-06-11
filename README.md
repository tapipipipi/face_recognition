# 顔認証システム（単数・複数）
https://github.com/toma1128/Smart_Attendance  
の顔認証部分となるリポジトリで、RasberryPiに組み込んだコードです。

## ディレクトリ・ファイル一覧

* ディレクトリ ※個人の写真データが含まれているため.gitignoreで隠しています
  * result : 複数人の顔認証結果の画像を保存
  * authe_image :　複数人の顔認証をする際のサンプル画像　※テスト用
  * face_data : 登録画像と名前　※テスト用
  * data : サーバーから引っ張ってきた画像を保存
* ファイル
  * face_recogniyion_s.py : 顔認証コード（個人判別）
  * face_recogniyion_m.py : 顔認証コード（複数人判定）
  * ~_bk : バックアップファイル。初めて正常に動作した時のコード
  * ~_test: テスト用コード
  * environment.txt : 正常に動作した時点での自分の環境。今回使わないライブラリ多数有
  * result_reset.py : result,dataの画像を全て削除
  * その他ファイル：チーム開発時に必要だったファイル
