#!/bin/bash

echo "ボットデス v0.10.1 lot.201212.8 by さこつ"
# とりあえず起動したらトゥート
python3 botdesu_neoki.py
# 乱数取得
toot_count=$((($RANDOM % 13)+1)) # 1~13
iraira=$((($RANDOM % 3372)+199)) # 199~3571
while true
do
    # 発言を拾ってくる
    python3 botdesu_catch.py
    # 600秒間待機
    echo "***ようすをみている***"
    sleep 600
    # カウントをテキトーに増やす
    $((toot_count+=$((($RANDOM % 214)+97)))) #97~311くらいふえる
    $((iraira+=$((($RANDOM % 2396)+35)))) #35~2431くらいふえる
    # イライラ値がこえた！
    if [ "$(toot_count)" -gt "$(iraira)" ] ; then
        # とぅーとする
        python3 botdesu_toot.py
        # カウントリセット
        toot_count=$((($RANDOM % 23)+1)) # 1~23
        iraira=$((($RANDOM % 3372)+199)) # 199~3571
    fi
done
