from mastodon import Mastodon, StreamListener
from requests_oauthlib import OAuth1Session
import mimetypes
from mimetypes import guess_extension
import requests
import pathlib
import json
import sys
import MeCab
import random
import threading

import os
import re
import shutil
from pytz import timezone

import datetime
import time

import bs4
from bs4 import BeautifulSoup
import urllib
import urllib.request, urllib.error
from urllib.request import urlopen, Request
from urllib import request as req
from urllib import error
from urllib import parse
from urllib.parse import quote

# ボットデスサブモジュール＆コンフィグ
from botdes import scheduler, config
import botdes.config

from botdes.config import BOT_ACOUNT_ID, MASTODON_CLIENT_ID, MASTODON_ACCESS_TOKEN, MASTODON_CLIENT_SECRET, MASTODON_URL

bot_acount_id = BOT_ACOUNT_ID

mstdn = Mastodon(
	client_id = MASTODON_CLIENT_ID,
    access_token = MASTODON_ACCESS_TOKEN,
	client_secret = MASTODON_CLIENT_SECRET,
    api_base_url = MASTODON_URL)

# リプライで送られてきた内容を元にAPIを叩いてその結果を返すクラス
class Stream(StreamListener):
    def __init__(self):
        super(Stream, self).__init__()

    def on_notification(self,notifn): #通知が来た時に呼び出して
        if notifn['type'] == 'mention': #通知の内容がメンションかチェック
            content = str(notifn['status']['content']) #なかみ
            img_ggrks(content) #画像ぐぐれかす用

def neoki():
    # 初回起動時とかtoot.txtがないときは作成
    if not os.path.exists("toot.txt"):
        touch_file = pathlib.Path("./toot.txt")
        touch_file.touch()

    # なんでかtoot.txtが空っぽの場合1回収集
    if os.stat("toot.txt").st_size == 0:
        timeline = mstdn.timeline_local(max_id=None, since_id=None, limit=40)
        for line in timeline:
            if line['account']['username'] != bot_acount_id:
                f = open("toot.txt" , "a")
                lists = (line['content'].replace("\n", ""))
                f.write(lists)
                f.flush()
                f.close()
    
    Mecab_file(neoki)
    print("***寝起きトゥート！***")

# イライラ定義
def iradef():
    global toot_count, iraira, searchcount
    toot_count = random.randint(1,13)
    iraira = random.randint(199,3571)
    searchcount = 12
    return toot_count, iraira, searchcount

# イライラ管理
def iraira_calc():
    global toot_count, iraira
    iraira_rating = float( toot_count / iraira ) * 100
    iraira_rate = "{:.2f}".format(iraira_rating) + "%" #strやで
    return iraira_rate

# とぅーと
def Mecab_file(n):
    global threads, toot_count, iraira
    f = open("toot.txt","r")
    data = f.read()
    f.close()
 
    mt = MeCab.Tagger("-Owakati")
 
    wordlist = mt.parse(data)
    try:
        wordlist = wordlist.rstrip(" \n").split(" ")
    except:
        # 発言集がなんかおかしいので消す（力業）
        os.remove("toot.txt")
        f = open('toot.txt','w')
        # 1回収集
        th_job_a_search()
    else:
 
        markov = {}
        w = ""
 
        for x in wordlist:
            if w:
                if w in markov:
                    new_list = markov[w]
                else:
                    new_list =[]
 
                new_list.append(x)
                markov[w] = new_list
            w = x
 
        choice_words = wordlist[0]
        sentence = ""
        count = 0

        if n == neoki:
            numm = random.randint(13,77)
        else:
            numm = random.randint(31,56)
    
        while count < numm:
            sentence += choice_words
            choice_words = random.choice(markov[choice_words])
            count += 1
 
            sentence = sentence.split(" ", 1)[0]
            p = re.compile("[!-/:-@[-`{-~]")
            sus = p.sub("", sentence)
    
        words = re.sub(re.compile("[!-~]"),"",sus)
        try:
            mstdn.toot(words)
        except:
            threads.append(scheduler.Scheduler(th_job_a_search, intvl=8))
            toot_count = random.randint(1,23)
            ira_x = random.randint(1,2011)
            ira_y = random.randint(1033,5005)
            if ira_x > ira_y:
                ira_x = ira_x - ira_y
            iraira = random.randint(ira_x,ira_y)
            print("***エラーで再起動！***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_calc())

# 発言拾う
def th_job_a_search():
    global toot_count, iraira
    timeline = mstdn.timeline_local(max_id=None, since_id=None, limit=40)
    for line in timeline:
        if line['account']['username'] != bot_acount_id:
            f = open("toot.txt" , "a")
            lists = (line['content'].replace("\n", ""))
            f.write(lists)
            f.flush()
            f.close()
    print("***はつげんひろった***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_calc())
    # 発言拾った後イライラ度が100%以上ならしゃべる
    if toot_count > iraira:
        Mecab_file(iraira)
        toot_count = random.randint(1,23)
        ira_x = random.randint(1,2011)
        ira_y = random.randint(1033,5005)
        if ira_x > ira_y:
            ira_x = ira_x - ira_y
        iraira = random.randint(ira_x,ira_y)
        print("***はつげんをしたよ***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_calc())
    else:
        muramura = (59 - random.randint(1,97))
        toot_count += muramura
        iraira_calc()
        if muramura > 0:
            print("***イライラするよお***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_calc())
        else:
            print("***ムラムラムラムラ***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_calc())

# 様子見
def th_job_d_nnn():
    global toot_count
    toot_count += random.randint(21,71)
    print("***ようすをみている***")

# あんまり検索しすぎないようにカウントする
def th_job_e_searchcount():
    global searchcount
    searchcount += 1

# 画像サーチ
def img_ggrks(content):
    global toot_count, iraira, searchcount
    # 検索しまくってたらそもそも検索しない
    if searchcount < 8:
        mstdn.toot("検索しすぎると怒られるからもうちょっと待って")
    else:
        # リプライの本体から余分な情報を削る
        req = content.rsplit(">")[-2].split("<")[0].strip() 
        if "エロ" in req:
            _toot = "いやえっちなのはよくない"
            mstdn.toot(_toot)
        elif "えっち" in req:
            _toot = "いやえっちなのはよくない"
            mstdn.toot(_toot)
        elif "の画像" in req:
            ggrks = re.search(r'[\s|、|,]*.*?の画像', req)
            que = re.sub(r'の画像', '', ggrks.group(0))
            _yahoo_img_dl(que)
        elif "画像" in req:
            ggrks = re.search(r'[\s|、|,]*.*?画像', req)
            que = re.sub(r'画像', '', ggrks.group(0))
            _yahoo_img_dl(que)
        elif "の絵" in req:
            ggrks = re.search(r'[\s|、|,]*.*?の絵', req)
            que = re.sub(r'の絵', '', ggrks.group(0))
            _yahoo_img_dl(que)
        else:
            # 何でもないときはイライラ度を返す
            ggrks = "なん？　"
            _toot = ggrks + "現在のイライラ度は" + iraira_calc()
            mstdn.toot(_toot)

#画像検索本体
def _yahoo_img_dl(word):
    global searchcount
    # 画像保存ディレクトリがなかったらつくる
    # あっても消してつくる
    if os.path.exists('imgs'):
        shutil.rmtree('imgs')
        os.mkdir('imgs')
    else:
        os.mkdir('imgs')
    
    url = "https://search.yahoo.co.jp/image/search?p={}&ei=UTF-8&b=&vd=w".format(quote(word))
    #headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
    #request = req.Request(url=url, headers=headers)
    #page = req.urlopen(request)
    response = requests.get(url)
    img_src_list = []
    pattern = 'original":{"url":"' + '(.*?)' + '"'
    tmp_extracted_text_array = re.findall(pattern, response.text)
    img_src_list.extend(tmp_extracted_text_array)
    # 画像ダウンロード
    imgnum = 0
    for imageURL in img_src_list:
        pal = '.jpg'
        if '.jpg' in imageURL:
            pal = '.jpg'
        elif '.JPG' in imageURL:
            pal = '.jpg'
        elif '.png' in imageURL:
            pal = '.png'
        elif '.gif' in imageURL:
            pal = '.gif'
        elif '.jpeg' in imageURL:
            pal = '.jpeg'
        else:
            pal = '.png'
        
        try:
            img = urllib.request.urlopen(imageURL)
            localfile = open('./imgs/' + str(imgnum)+pal, 'wb')
            localfile.write(img.read())
            img.close()
            localfile.close()
            imgnum += 1
        except UnicodeEncodeError:
            continue
        except error.HTTPError:
            mstdn.toot("ごめん検索しすぎで怒られた")
        except error.URLError:
            mstdn.toot("なんかダメだって")
            break
        
    #保存した画像からランダムで1枚選ぶ 0枚の時は画像が見当たらないってことで。
    try:
        random_file = random.choice(os.listdir("./imgs"))
        imgpath = "./imgs/" + random_file
        file = mstdn.media_post(imgpath, mimetypes.guess_type(imgpath)[0])
        message = word + "ですよ"
        # いちおう未収載でトゥート
        mstdn.status_post(status = message, media_ids = file, visibility='unlisted')
        # 検索カウンターリセット
        searchcount = 0
    except:
        mstdn.toot("画像探せんかったわ")

def run():
    global threads
    # 起動時に1回寝起きトゥート発動
    neoki()
    # イライラ定義、サーチカウント定義
    iradef()
    threads = []
    # タイムライン受信系
    mstdn.stream_user(Stream(), run_async=True,timeout=180, reconnect_async=True, reconnect_async_wait_sec=5)
    #スケジュール起動系(間隔)
    threads.append(scheduler.Scheduler(th_job_d_nnn, intvl=1))
    threads.append(scheduler.Scheduler(th_job_a_search, intvl=8))
    threads.append(scheduler.Scheduler(th_job_e_searchcount, intvl=5))

    for th in threads:
        th.start()
