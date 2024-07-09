# 顔認証システム（単数・複数）

## ディレクトリ・ファイル一覧

* ディレクトリ
  * authe_image :　複数人の顔認証をする際のサンプル画像　※テスト用
  * face_data : 登録画像と名前　※テスト用
  * result : 複数人の顔認証結果の画像を保存
  * data : サーバーから引っ張ってきた画像を保存
* ファイル
  * face_recogniyion_s.py : 顔認証コード（個人判別）
  * face_recogniyion_m.py : 顔認証コード（複数人判定）
  * ~_bk : バックアップファイル。初めて正常に動作した時のコード
  * ~_test: cv2が正常に動いているか確認するコード
  * environment.txt : 正常に動作した時点での自分の環境。今回使わないライブラリ多数有
  * result_reset.py : result,dataの画像を全て削除

***

### ※insightfaceがインストール出来なかったとき

コマンドプロンプト等で以下のコマンドを実行しインストール（Windows）

 Microsoft Visual C++  
`winget install -e --id Microsoft.VCRedist.2015+.x64`

 Visual Studio 2022 Build Tools(C++を選択)  
`winget install -e --id Microsoft.VisualStudio.2022.BuildTools --override "--wait --add Microsoft.VisualStudio.Workload.NativeDesktop --includeRecommended"`

再度実行 ※既にcythonが入っていることを確認  
`pip install insightface`

これで無理なら分かりませんｽｲﾏｾﾝ...
