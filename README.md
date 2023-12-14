# HAAR-CASCADE
Haar-Like分類器を作成するためのプログラム群です。  

## annotation_img.py
このプログラムは、画像に対してアノテーションを行い、その結果を保存します。アノテーションはマウス操作により行います。  

**使い方**  

1. `.images` フォルダにアノテーションをするファイルを保存
2. `python annotation_img.py`

- sキー：データ保存 → 次のフレーム
- dキー：矩形データを削除
- rキー：データ保存なし → 次のフレーム
- escキー：途中でプログラム終了

📌 プログラム内部の変数 `offset_frame` を指定することで保存画像の連番を調整できます。  

# annotation_mov.py
このプログラムは、動画に対してアノテーションを行い、その結果を保存します。アノテーションはマウス操作により行います。  

**使い方**  

1. `.video` フォルダにアノテーションをするファイルを保存
2. プログラム内部の `video_path` に動画ファイルパスを指定
3. `python annotation_mov.py`

- sキー：データ保存 → 次のフレーム
- dキー：矩形データを削除
- rキー：データ保存なし → 次のフレーム
- escキー：途中でプログラム終了

📌 プログラム内部の変数 `offset_frame` を指定することで保存画像の連番と読込フレーム位置を調整できます。  

# opencv_train.sh
このスクリプトは、アノテーションされたデータを用いて、OpenCVのカスケード分類器を訓練します。  
途中、正解画像の学習データ量を問われるので正解画像量のおよそ **8~9割** を指定してください。  
./cascadeout に `cascade.xml` が生成されていたら学習終了となります。  

**前準備**  

- pos フォルダに正解画像と `poslist.txt` が作成されている
- neg フォルダに不正解画像が保存されている


# Pipfile
このファイルは、プロジェクトのPython環境を定義します。Pythonのバージョンは3.11.2を使用し、必要なパッケージとしてopencv-pythonがインストールされます。  

