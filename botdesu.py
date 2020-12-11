from requests_oauthlib import OAuth1Session
import json
import sys
import MeCab
import random
import re
from mastodon import Mastodon
import os
from dotenv import load_dotenv

import datetime
import time

# ボットデス by さこつ

# .envファイルの内容を読み込み
load_dotenv()

bot_acount_id = os.getenv('BOT_ACOUNT_ID')

mstdn = Mastodon(
	client_id = os.getenv('MASTODON_CLIENT_ID'),
    access_token = os.getenv('MASTODON_ACCESS_TOKEN'),
	client_secret = os.getenv('MASTODON_CLIENT_SECRET'),
    api_base_url = os.getenv('MASTODON_URL'))

def job_a_search():
    Search()
    print("***はつげんをひろったよ***")

def job_b_toot():
    Mecab_file()
    print("***はつげんしたよ***")

def job_c_deltxt():
    Del_text()
    print("***ログをけしたよ***")

def Search():
    timeline = mstdn.timeline_local(max_id=None, since_id=None, limit=40)
    for line in timeline:
        if line['account']['username'] != bot_acount_id:
            f = open("toot.txt" , "a")
            lists = (line['content'].replace("\n", ""))
            f.write(lists)
            f.flush()
            f.close()

def Mecab_file():
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

# 今は使っていないのでテキストはどんどん溜まっていく仕様
def Del_text():
    os.remove("toot.txt")
    f = open('toot.txt','w')
    f.close()
    timeline = mstdn.timeline_local(max_id=None, since_id=None, limit=40)
    for line in timeline:
        if line['account']['username'] != bot_acount_id:
            f = open("toot.txt" , "a")
            lists = (line['content'].replace("\n", ""))
            f.write(lists)
            f.flush()
            f.close()

while True:
    toot_count = random.randint(0,13)
    print("***ようすをみている***")
    time.sleep(600)
    job_a_search()
    toot_count += random.randint(97,311)
    iraira = random.randint(199,3571)
    if toot_count > iraira:
        job_b_toot()
        toot_count = 0

