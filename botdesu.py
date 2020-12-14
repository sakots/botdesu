from requests_oauthlib import OAuth1Session
import mimetypes
import requests
import json
import sys
import MeCab
import random
import re
from mastodon import Mastodon, StreamListener
import os
from dotenv import load_dotenv

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

from mimetypes import guess_extension

# ボットデス by さこつ

# .envファイルの内容を読み込み
load_dotenv()

bot_acount_id = os.getenv('BOT_ACOUNT_ID')

mstdn = Mastodon(
	client_id = os.getenv('MASTODON_CLIENT_ID'),
    access_token = os.getenv('MASTODON_ACCESS_TOKEN'),
	client_secret = os.getenv('MASTODON_CLIENT_SECRET'),
    api_base_url = os.getenv('MASTODON_URL'))

# リプライで送られてきた内容を元にAPIを叩いてその結果を返すクラス
class Stream(StreamListener):
    def __init__(self):
        super(Stream, self).__init__()

    def on_notification(self,notif): #通知が来た時に呼び出して
        if notif['type'] == 'mention': #通知の内容がメンションかチェック
            content = notif['status']['content'] #なかみ
            content = str(notif["content"])
            main(content)

try:
    toot_count
except NameError:
    toot_count = random.randint(1,13)
try:
    iraira
except NameError:
    iraira = random.randint(199,3571)

def main(content):
    req = content.rsplit(">")[-2].split("<")[0].strip() #リプライの本体から余分な情報を削る
    if "の画像" in req:
        ggrks = re.search(r'[\s|、(.*?)]の画像', req)
    elif "の絵" in req:
        ggrks = re.search(r'[\s|、(.*?)]の絵', req)
    elif "ちょうだい" in req:
        ggrks = re.search(r'[\s|、(.*?)]ちょうだい', req)
    elif "ください" in req:
        ggrks = re.search(r'[\s|、(.*?)]ください', req)
    elif "くれ" in req:
        ggrks = re.search(r'[\s|、(.*?)]くれ', req)
    else:
        # 何でもないときはイライラ度を返す
        ggrks = "なん？　"
        iraira_calc()
        mstdn.toot(ggrks + "現在のイライラ度は" + iraira_rate)
    # ググる
    _google_img_search(ggrks)
    #保存した画像からランダムで1枚選ぶ
    random_file = random.choice(os.listdir("imgs"))
    imgpath = "./imgs/" + random_file
    file = [mstdn.media_post(random_file, mimetypes.guess_type(random_file)[0]) for random_file in imgpath]
    message = ggrks + "ですよ"
    mstdn.status_post(status = message, media_ids = file, visibility='unlisted')
    # いちおう未収載

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
            localfile = open('./img/'+str(imgcounter)+pal, 'wb')
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

def job_a_search():
    timeline = mstdn.timeline_local(max_id=None, since_id=None, limit=40)
    for line in timeline:
        if line['account']['username'] != bot_acount_id:
            f = open("toot.txt" , "a")
            lists = (line['content'].replace("\n", ""))
            f.write(lists)
            f.flush()
            f.close()

def job_b_toot():
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

def iraira_calc():
    global iraira_rate
    iraira_rate = float( toot_count / iraira ) * 100
    iraira_rate = "{:.2f}".format(iraira_rate ) + "%" #strやで

iraira_calc()
print("***ようすをみている***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)

#ストリームの起動
mstdn.stream_user(Stream())

while True:
    see = 0
    while see < 10: 
        print("***ようすをみている***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "]")
        time.sleep(60)
        see += 1

    job_a_search()
    toot_count += random.randint(97,311)
    iraira_calc()
    print("***トゥートひろった***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)
    if toot_count > iraira:
        job_b_toot()
        toot_count = random.randint(1,23)
        iraira = random.randint(random.randint(1,2011),random.randint(1033,5005))
        iraira_calc()
        print("***はつげんしたよ！***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)
    else:
        muramura = (59 - random.randint(1,97))
        toot_count += muramura
        iraira_calc()
        if muramura > 0:
            print("***イライラするよ…***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)
        else:
            print("***ムラムラ…ふぅ…***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)
