from Module import sptool
import requests
from pyquery import PyQuery as pq
from pprint import pprint
import re
from queue import Queue
from threading import Thread
import time


class PTT:
    def __init__(self):
        self.sp = sptool.sp()
        self.data = []
        self.chpage = []
        self.titlist = []
        self.thread_page_num = 50
        self.page_Q = Queue()

    def Get_Ptt(self, url):
        res = requests.get(url)
        data = pq(res.content.decode())
        self.data = data
        return self.data

    def Ptt_Btn(self):
        data = self.data
        btn = data('a.btn.wide')
        pages = ['old', 'last', 'next', 'new']
        # pages=[]
        for i in range(len(pages)):
            if pq(btn[i]).attr('href'):
                pages[i] = 'https://www.ptt.cc'+ pq(btn[i]).attr('href')
            else:
                pages[i] = None
            self.chpage.append(pages[i])
        # print(self.chpage)
        return self.chpage

    def Allpage(self):
        # url = self.chpage[1]
        chpage = self.Ptt_Btn()
        max_page = re.findall(r"\d+", chpage[1])[0]
        links = []
        # print(max_page)
        for i in range(int(max_page)+1):  #int(max_page)+1
            links.append('https://www.ptt.cc/bbs/Grad-ProbAsk/index{}.html'.format(str(i)))
        # pprint(links)
        return links

    def Ptt_Parse(self, link):
        data = self.Get_Ptt(link)
        rent = data('div.r-ent')
        titles = rent('div.title')
        dates = rent('div.date')
        for i in range(len(titles)):
            title = pq(titles[i])
            temp = []
            temp.append(pq(dates[i]).text())  # date
            temp.append(title.text())
            try:
                url = 'https://www.ptt.cc'+ pq(title)('a').attr('href')
            except: # 本文章已刪除
                url = '本文章已刪除'
            temp.append(url)
            self.titlist.append(temp)
        return self.titlist

    def Thread_Get_Page(self):
        while self.page_Q.qsize() != 0:
            link = self.page_Q.get()
            self.Ptt_Parse(link)
            time.sleep(1)

    def Ptt_Parse_Start_Thread(self):
        links = self.Allpage()
        for link in links:
            self.page_Q.put(link)
        # print(self.page_Q.qsize())
        for i in range(self.thread_page_num):
            t = Thread(target=self.Thread_Get_Page)
            t.start()
        print('start to fetch data')
        total_mission = self.page_Q.qsize()
        while self.page_Q.qsize() != 0:
            print('loading: {}/{}'.format(self.page_Q.qsize(), total_mission))
            time.sleep(1)
        print('\nclear')

        return self.titlist


if __name__ == '__main__':
    obj = PTT()
    url = 'https://www.ptt.cc/bbs/Grad-ProbAsk/index1255.html'
    obj.Get_Ptt(url)
    # obj.Ptt_Btn()
    # obj.Ptt_Parse_Start_Thread()
    # obj.Allpage()
    obj.Ptt_Parse(url)

    # obj.Ptt_Btn()