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
        self.sp = sptool.spider()
        self.data = []
        self.chpage = []
        self.titlist = {}
        self.thread_page_num = 20
        self.page_Q = Queue()

    def Get_Ptt(self, url):
        res = requests.get(url)
        data = pq(res.content.decode())
        self.data = data
        return self.data

    def Ptt_Btn(self):
        data = self.data
        btn = data('a.btn.wide')
        page_name = ['old', 'last', 'next', 'new']
        pages=[]
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
        for i in range(int(max_page)+1):
            links.append('https://www.ptt.cc/bbs/Grad-ProbAsk/index{}.html'.format(str(i)))
        # pprint(links)
        return links

    def Ptt_Parse(self, link):
        data = self.Get_Ptt(link)
        rent = data('div.r-ent')
        titlist = self.titlist
        titles = rent('div.title')
        dates = rent('div.date')
        for i in range(len(titles)):
            title = pq(titles[i])
            date = pq(dates[i])
            titlist[title.text()] = []
            try:
                # cont_url = self.sp.tiny('https://www.ptt.cc'+ pq(title)('a').attr('href'))
                cont_url = 'https://www.ptt.cc'+ pq(title)('a').attr('href')
                titlist[title.text()].append(cont_url)
            except: # 本文章已刪除
                titlist[title.text()].append(None)
            titlist[title.text()].append(date.text())
        # pprint(titlist)
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
        print(self.titlist)


if __name__ == '__main__':
    obj = PTT()
    url = 'https://www.ptt.cc/bbs/Grad-ProbAsk/index.html'
    obj.Get_Ptt(url)
    obj.Ptt_Btn()
    # obj.Ptt_Parse_Start_Thread()
    # obj.Allpage()
    # obj.Ptt_Parse(url)

    # obj.Ptt_Btn()