from time import time, sleep
from datetime import datetime
from pytz import timezone
import threading
import random

# スケジューラー

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
