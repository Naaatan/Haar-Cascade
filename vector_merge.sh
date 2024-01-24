ESC=$(printf '\033') # \e や \x1b または $'\e' は使用しない

printf "${ESC}[34m%s${ESC}[m\n" '分割されたvectorファイルをマージします [y/n]:'
read isStart

if [ $isStart = "y" ]; then
    python mergevec.py -v ./vec -o ./vec/posvec.vec
    printf "${ESC}[34m%s${ESC}[m\n" 'Completed...'
else
    printf "${ESC}[31m%s${ESC}[m\n" 'Stop...'
    exit 1
fi

