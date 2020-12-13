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

try:
    toot_count
except NameError:
    toot_count = random.randint(1,13)
try:
    iraira
except NameError:
    iraira = random.randint(199,3571)

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

while True:
    iraira_calc()
    see = 0
    print("***ようすをみている***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)
    while see < 9: 
        print("***ようすをみている***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "]")
        time.sleep(60)
        see += 1

    job_a_search()
    toot_count += random.randint(97,311)
    iraira_calc()
    print("***はつげんをひろったよ***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)
    if toot_count > iraira:
        job_b_toot()
        toot_count = random.randint(1,23)
        iraira = random.randint(random.randint(1,2011),random.randint(1033,5005))
        iraira_calc()
        print("***はつげんしたよ***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)
    else:
        toot_count += random.randint(1,47)
        iraira_calc()
        print("***はつげんしたかったよ…***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)
