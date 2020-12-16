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

from botdes.config import BOT_ACOUNT_ID, MASTODON_CLIENT_ID, MASTODON_ACCESS_TOKEN, MASTODON_CLIENT_SECRET, MASTODON_URL, iraira, toot_count

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

# イライラ管理
def iraira_calc():
    iraira_rating = float( toot_count / iraira ) * 100
    iraira_rate = "{:.2f}".format(iraira_rating) + "%" #strやで
    return iraira_rate

def r_toot():
    if float( toot_count / iraira ) >= 1:
        Mecab_file(r_toot)
        toot_count = random.randint(1,23)
        iraira = random.randint(random.randint(1,2011),random.randint(1033,5005))
        print("***はつげんをしたよ***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_calc())
    else:
        muramura = (59 - random.randint(1,97))
        toot_count += muramura
        iraira_calc()
        if muramura > 0:
            print("***イライラするよお***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_calc())
        else:
            print("***ムラムラムラムラ***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_calc())

# とぅーと
def Mecab_file(n):
    f = open("toot.txt","r")
    data = f.read()
    f.close()
 
    mt = MeCab.Tagger("-Owakati")
 
    wordlist = mt.parse(data)
    wordlist = wordlist.rstrip(" \n").split(" ")
 
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
    mstdn.toot(words)

# 発言拾う
def th_job_a_search():
    timeline = mstdn.timeline_local(max_id=None, since_id=None, limit=40)
    for line in timeline:
        if line['account']['username'] != bot_acount_id:
            f = open("toot.txt" , "a")
            lists = (line['content'].replace("\n", ""))
            f.write(lists)
            f.flush()
            f.close()
    print("***はつげんひろった***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_calc())

# 様子見
def th_job_d_nnn():
    print("***ようすをみている***")

# 画像サーチ
def img_ggrks(content):
    # リプライの本体から余分な情報を削る
    req = content.rsplit(">")[-2].split("<")[0].strip() 
    if "のエロ" in req:
        _toot = "いやえっちなのはよくない"
        mstdn.toot(_toot)
    elif "の画像" in req:
        ggrks = re.search(r'[\s|、|,]*.*?の画像', req)
        que = re.sub(r'の画像', '', ggrks.group(0))
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
def _request(url):
    # requestを処理しHTMLとcontent-typeを返す
    req = Request(url)
    try:
        with urlopen(req, timeout=5) as p:
            b_content = p.read()
            mime = p.getheader('Content-Type')
    except:
        return None, None
    return b_content, mime
def _yahoo_img_dl(word):
    # 画像保存ディレクトリがなかったらつくる
    # あっても消してつくる
    if os.path.exists('imgs'):
        shutil.rmtree('imgs')
        os.mkdir('imgs')
    else:
        os.mkdir('imgs')
    
    url = "https://search.yahoo.co.jp/image/search?p={}&ei=UTF-8&b=&vd=w".format(quote(word))
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
    request = req.Request(url=url, headers=headers)
    page = req.urlopen(request)
    response = requests.get(page)
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
        img = urllib.request.urlopen(imageURL)
        localfile = open('./imgs/' + str(imgnum)+pal, 'wb')
        localfile.write(img.read())
        img.close()
        localfile.close()
        imgnum += 1
    #保存した画像からランダムで1枚選ぶ
    random_file = random.choice(os.listdir("./imgs"))
    imgpath = "./imgs/" + random_file
    file = [mstdn.media_post(imgpath, mimetypes.guess_type(imgpath)[0]) for random_file in random_file]
    message = word + "ですよ"
    mstdn.status_post(status = message, media_ids = file, visibility='unlisted')
    # いちおう未収載でトゥート

def run():
    # 起動時に1回寝起きトゥート発動
    neoki()
    threads = []
    # タイムライン受信系
    mstdn.stream_user(Stream(), run_async=True,timeout=180, reconnect_async=True, reconnect_async_wait_sec=5)
    #スケジュール起動系(間隔)
    threads.append(scheduler.Scheduler(th_job_d_nnn, intvl=1))
    threads.append(scheduler.Scheduler(th_job_a_search, intvl=10))
    # てきとう発言系
    threads.append(scheduler.Scheduler(r_toot, intvl=5))

    for th in threads:
        th.start()
