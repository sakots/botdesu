from time import time, sleep
from datetime import datetime
from pytz import timezone
import threading
import random

# てきとうスケジューラー（イライラ管理）

global iraira_rate, toot_count, iraira
# イライラ定義
try:
    toot_count
except NameError:
    toot_count = random.randint(1,13)
try:
    iraira
except NameError:
    iraira = random.randint(199,3571)
iraira_rate = float( toot_count / iraira ) * 100
iraira_rate = "{:.2f}".format(iraira_rate ) + "%" #strやで


class Scheduler():
    def __init__(self, func, intvl):
        if intvl:
            self.th = threading.Thread(target=self.scheduler, args=(func, intvl))
        else:
            self.th = threading.Thread(target=self.scheduler_rnd, args=(func,))
    
    def scheduler(self, func, intvl):
        #func:起動する処理
        while True:
            func()
            sleep(intvl * 60)
    def scheduler_rnd(self, func):
        #func:起動する処理
        while True:
            func()
            sleep(random.randint(1,173))

    def start(self):
        self.th.start()

class Ira():
    def __init__(self, func):
        self.th = threading.Thread(target=self.iraira_rnd, args=(func,))
    def iraira_calc(self):
        global iraira_rate
        iraira_rate = float( toot_count / iraira ) * 100
        iraira_rate = "{:.2f}".format(iraira_rate ) + "%" #strやで
    def iraira_rnd(self, func):
        while True:
            if toot_count > iraira:
                toot_count = random.randint(1,23)
                iraira = random.randint(random.randint(1,2011),random.randint(1033,5005))
                func()
                self.iraira_calc()
            else:
                muramura = (59 - random.randint(1,97))
                toot_count += muramura
                self.iraira_calc()
                if muramura > 0:
                    print("***イライラするよお***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)
                else:
                    print("***ムラムラムラムラ***" + " - c[" + str(toot_count) + "]:" + "i[" + str(iraira) + "] イライラ度 " + iraira_rate)

    def start(self):
        self.th.start()