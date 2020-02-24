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
        self.ptt_pack = []
        # self.ptt_date_list = []
        # self.ptt_title_list = []
        # self.ptt_url_list = []
        self.thread_page_num = 50
        self.page_Q = Queue()

    def Get_Ptt(self, url):
        res = requests.get(url)
        data = pq(res.content.decode())
        self.data = data
        # print(data)
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
            temp = {}
            title = pq(titles[i])
            try:
                url = 'https://www.ptt.cc'+ pq(title)('a').attr('href')
            except: # 本文章已刪除
                url = '本文章已刪除'
            temp["url"] = url
            temp["date"] = (pq(dates[i]).text())
            temp["title"] = (title.text())
            self.ptt_pack.append(temp)
        # self.ptt_pack["date"] = self.ptt_date_list
        # self.ptt_pack["title"] = self.ptt_title_list
        # self.ptt_pack["url"] = self.ptt_url_list
        print(self.ptt_pack)
        return self.ptt_pack


if __name__ == '__main__':
    obj = PTT()
    url = 'https://www.ptt.cc/bbs/Grad-ProbAsk/index1255.html'
    # obj.Get_Ptt(url)
    # obj.Ptt_Btn()
    # obj.Allpage()
    obj.Ptt_Parse(url)
