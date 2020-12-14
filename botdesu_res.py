from botdesu import iraira_calc, iraira_rate
from requests_oauthlib import OAuth1Session
import mimetypes
import requests
import json
import sys
import MeCab
import random
import re
import shutil
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

# ボットデスれすば対応 by さこつ

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
            content = str(notif['status']['content'])
            main(content)

def main(content):
    # リプライの本体から余分な情報を削る
    req = content.rsplit(">")[-2].split("<")[0].strip() 
    if "のエロ" in req:
        yokunai = "いやえっちなのはよくない"
        mstdn.toot(yokunai)
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
        iraira_calc()
        mstdn.toot(ggrks + "現在のイライラ度は" + iraira_rate)

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

#ストリームの起動
mstdn.stream_user(Stream())
