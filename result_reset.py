import os
import shutil

#顔認証結果画像の削除

target_dir = 'result'
shutil.rmtree(target_dir)
os.mkdir(target_dir)

target_dir = 'data'
shutil.rmtree(target_dir)
os.mkdir(target_dir)