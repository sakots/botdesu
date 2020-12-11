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
import schedule
import time

# ボットデス v0.9.13 lot.201212.0

# .envファイルの内容を読み込み
load_dotenv()

bot_acount_id = os.getenv('BOT_ACOUNT_ID')

mstdn = Mastodon(
	client_id = os.getenv('MASTODON_CLIENT_ID'),
    access_token = os.getenv('MASTODON_ACCESS_TOKEN'),
	client_secret = os.getenv('MASTODON_CLIENT_SECRET'),
    api_base_url = os.getenv('MASTODON_URL'))

def job_a():
    Search()
    print("***はつげんをひろったよ***")

def job_b():
    Mecab_file()
    print("***はつげんしたよ***")

def job_c():
    Del_text()
    print("***ログをけしたよ***")

# schedule.every(997).minutes.do(job_c)
schedule.every(17).minutes.do(job_a)
schedule.every(random.randint(3,173)).minutes.do(job_b)

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
  schedule.run_pending()
  print("***ようすをみている***")
  time.sleep(120)
