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
from botdes import irairacalc, config
from irairacalc import iraira_rate, toot_count, iraira

from botdes.config import BOT_ACOUNT_ID, MASTODON_CLIENT_ID, MASTODON_ACCESS_TOKEN, MASTODON_CLIENT_SECRET,  MASTODON_URL

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

def r_toot():
    Mecab_file(r_toot)
    print("***はつげんをしたよ***")

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

def th_job_a_search():
    timeline = mstdn.timeline_local(max_id=None, since_id=None, limit=40)
    for line in timeline:
        if line['account']['username'] != bot_acount_id:
            f = open("toot.txt" , "a")
            lists = (line['content'].replace("\n", ""))
            f.write(lists)
            f.flush()
            f.close()
    print("***はつげんひろった***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)

def img_ggrks(content):
    # リプライの本体から余分な情報を削る
    req = content.rsplit(">")[-2].split("<")[0].strip() 
    if "のエロ" in req:
        _toot = "いやえっちなのはよくない"
        mstdn.toot(_toot)
    elif "の画像" in req:
        ggrks = re.search(r'[\s|、|,]*.*?の画像', req)
        que = re.sub(r'の画像', '', ggrks.group(0))
        _google_img_search(que)
    elif "の絵" in req:
        ggrks = re.search(r'[\s|、|,]*.*?の絵', req)
        que = re.sub(r'の絵', '', ggrks.group(0))
        _google_img_search(que)
    else:
        # 何でもないときはイライラ度を返す
        ggrks = "なん？　"
        _toot = ggrks + "現在のイライラ度は" + iraira_rate
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
def _google_img_search(word):
    # 画像保存ディレクトリがなかったらつくる
    # あっても消してつくる
    shutil.rmtree('imgs')
    if not os.path.exists('imgs'):
        os.mkdir('imgs')
    
    urlKeyword = parse.quote(word)
    url = "https://www.google.com/search?as_st=y&tbm=isch&hl=ja&as_q=" + urlKeyword + "&as_epq=&as_oq=&as_eq=&imgsz=&imgar=&imgc=&imgcolor=&imgtype=&cr=&as_sitesearch=&safe=active&as_filetype=&tbs=qdr:w"

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
    request = req.Request(url=url, headers=headers)
    page = req.urlopen(request)

    html = page.read().decode('utf-8')
    html = bs4.BeautifulSoup(html, "html.parser")
    elems = html.select('.rg_meta.notranslate')

    # 保存すっぞ
    imgcounter = 0
    for ele in elems:
        ele = ele.contents[0].replace('"','').split(',')
        eledict = dict()
        for e in ele:
            num = e.find(':')
            eledict[e[0:num]] = e[num+1:]
        imageURL = eledict['ou']

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
            img = req.urlopen(imageURL)
            localfile = open('./imgs/'+str(imgcounter)+pal, 'wb')
            localfile.write(img.read())
            img.close()
            localfile.close()
            imgcounter += 1
        except UnicodeEncodeError:
            continue
        except error.HTTPError:
            continue
        except error.URLError:
            continue
        break
    #保存した画像からランダムで1枚選ぶ
    random_file = random.choice(os.listdir("./imgs"))
    imgpath = "./imgs/" + random_file
    file = [mstdn.media_post(random_file, mimetypes.guess_type(random_file)[0]) for random_file in imgpath]
    message = word + "ですよ"
    mstdn.status_post(status = message, media_ids = file, visibility='unlisted')
    # いちおう未収載

def run():
    # 起動時に1回寝起きトゥート発動
    neoki()
    threads = []
    # タイムライン受信系
    mstdn.stream_user(Stream(), run_async=True,timeout=180, reconnect_async=True, reconnect_async_wait_sec=5)
    #スケジュール起動系(間隔)
    threads.append(irairacalc.Scheduler(th_job_a_search, intvl=6))
    # てきとう発言系
    threads.append(irairacalc.Ira(r_toot))

    for th in threads:
        th.start()
