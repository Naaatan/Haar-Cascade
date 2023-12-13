import os
import re

import cv2
import numpy as np

img_path = "./pos/"  # 画像保存先のディレクトリ
poslist = "./pos/poslist.txt"  # 正解画像リスト
src_img_path = "./images/"  # ソースイメージ格納ディレクトリ

# 位置格納用
point = np.empty((0, 2), dtype=np.int64)  # 確定位置
point_drawing = np.empty(0, dtype=np.int64)  # 暫定位置


# 位置格納関数
def mouse_event(event, x, y, flags, param):
    # グローバル変数を利用
    global point, point_drawing
    # マウス左ボタン押下時
    if event == cv2.EVENT_LBUTTONDOWN:
        point = np.append(point, np.array([[x, y]]), axis=0)  # 位置格納
    # マウス左ボタン解放時
    elif event == cv2.EVENT_LBUTTONUP:
        point = np.append(point, np.array([[x, y]]), axis=0)  # 位置格納
        point_drawing = np.empty(0, dtype=np.int64)  # 暫定位置
    # 移動操作
    elif event == cv2.EVENT_MOUSEMOVE:
        pt_num = int(len(point))
        if pt_num % 2 == 1:
            point_drawing = [point[pt_num - 1], [x, y]]  # 暫定位置格納


# 保存関数
def save_img(img, frame):
    # グローバル変数を利用
    global point
    # 画像の保存
    img_name = str(frame) + ".jpg"  # 画像名
    cv2.imwrite(img_path + img_name, img)  # 画像の保存

    # poslistの保存
    point = point.reshape((-1, 4))
    pt_num = int(len(point))  # 矩形数

    pt_txt = " " + str(pt_num)  # 出力用

    for i in range(pt_num):
        pt_txt = (
            pt_txt
            + " "
            + str(point[i][0])
            + " "
            + str(point[i][1])
            + " "
            + str(point[i][2] - point[i][0])
            + " "
            + str(point[i][3] - point[i][1])
        )

    txt_data = img_name + pt_txt + "\n"  # 画像名と共に保存
    with open(poslist, "a") as txt:  # ポジリスト
        txt.write(txt_data)


# 画像(jpg/png)のみ取得
def listupImage(path):
    patternStr = ".+\.(jpg|png)"
    pattern = re.compile(patternStr)
    listup = []
    for item in os.listdir(path):
        result = pattern.match(item)
        # resultがNone以外=画像 なのでパスをリストに追加
        if result:
            listup.append(os.path.join(path, item))
    return listup


file_list = listupImage(src_img_path)  # 画像ファイル一覧取得
file_count = len(file_list)  # ファイル数取得


cv2.namedWindow("window", cv2.WINDOW_NORMAL)  # windowの生成
cv2.setMouseCallback("window", mouse_event)  # 描画関数を設定
offset_frame = 0  # フレーム開始位置
frame = 0  # フレーム番号
h = 0  # 画像の高さ

# プログラム全体終了フラグ
fin_flag = True

# ループ処理
while fin_flag:
    # フレーム取り出し
    if frame < file_count:
        img = cv2.imread(file_list[frame])
        h, _ = img.shape[:2]
    else:
        break

    # フレーム番号の描画
    frame += 1  # フレーム番号の加算

    # ループ処理
    while True:
        paint = img.copy()  # データのコピー

        cv2.putText(
            paint,
            str(frame + offset_frame),
            (5, h - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            thickness=2,
        )  # フレーム番号の描画

        # 矩形座標が決まっているもののみ描画
        for i in range(int(len(point) / 2)):
            cv2.rectangle(
                paint,
                tuple(point[2 * i]),
                tuple(point[2 * i + 1]),
                (0, 0, 255),
                thickness=2,
            )  # 描画

        # 暫定位置の描画
        if len(point_drawing) == 2:
            cv2.rectangle(
                paint,
                tuple(point_drawing[0]),
                tuple(point_drawing[1]),
                (0, 0, 255),
                thickness=2,
            )  # 描画

        # windowに描画する
        cv2.imshow("window", paint)

        # キー入力を待つ
        key = cv2.waitKey(10)
        # sキーが押されたら,データの保存,次のフレーム
        if key == ord("s"):
            save_img(img, frame + offset_frame)
            point = np.empty((0, 2), dtype=np.int64)
            break
        # dキーが押されたら,矩形データを削除
        elif key == ord("d"):
            point = np.empty((0, 2), dtype=np.int64)
        # rキーが押されたら次のフレーム
        elif key == ord("r"):
            point = np.empty((0, 2), dtype=np.int64)
            break
        # escキーが押されたらプログラム終了
        elif key == 27:
            fin_flag = False
            break


cv2.destroyAllWindows()  # windowを消す
