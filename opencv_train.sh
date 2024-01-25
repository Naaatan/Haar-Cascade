ESC=$(printf '\033') # \e や \x1b または $'\e' は使用しない

printf "${ESC}[34m%s${ESC}[m\n" '.vec ファイルの作成工程をスキップして次へ進みますか？[y/n]:'
read is_skip

if [ $is_skip = "y" ]; then
    printf "${ESC}[34m%s${ESC}[m\n" 'スキップします...'
else
    # 正解画像の作成枚数指定
    printf "${ESC}[34m%s${ESC}[m\n" '作成正解画像の枚数を入力してください >>'
    read createimg

    # opencv_createsamplesで正解画像リストをvecファイルに変換
    printf "${ESC}[34m%s${ESC}[m\n" '正解画像リストからVectorファイルに変換...'
    opencv_createsamples -info pos/poslist.txt -vec vec/posvec.vec -num $createimg
    echo
fi

# 不正解画像リストを作る
printf "${ESC}[34m%s${ESC}[m\n" '不正解画像リストを作成...'
ls neg | xargs -I {} echo neg/{} > ./neg/neglist.txt
printf "${ESC}[33m%s${ESC}[m\n" '画像数をカウント...'
wc -l neg/neglist.txt
echo

# cascadeoutフォルダのファイルを削除
printf "${ESC}[34m%s${ESC}[m\n" 'cascadeoutフォルダのデータを削除...'
rm -rf ./cascadeout/*
echo

# opencv_traincascadeでカスケード分類器を作成（numPos　は学習データ量の8〜9割程度の数を指定）
printf "${ESC}[34m%s${ESC}[m\n" '正解画像の学習データ量を入力してください >>'
read numpos
printf "${ESC}[34m%s${ESC}[m\n" '不正解画像の学習データ量を入力してください >>'
read numneg
opencv_traincascade -data ./cascadeout/ -vec ./vec/posvec.vec -bg ./neg/neglist.txt -numPos $numpos -numNeg $numneg