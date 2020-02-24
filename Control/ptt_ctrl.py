from Module import ptt, DB
from queue import Queue
from threading import Thread
import time
import json

class CTRL:
    def __init__(self, wui=None):
        self.ptt = ptt.PTT()
        self.thread_page_num = 50
        self.page_Q = Queue()
        self.date_list = []
        self.title_list = []
        self.url_list = []
        self.wui = wui
        self.db = DB.DB()

    def Thread_Get_Page(self):
        while self.page_Q.qsize() != 0:
            link = self.page_Q.get()
            self.ptt.Ptt_Parse(link)

            time.sleep(1)

    def Ptt_Parse_Start_Thread(self):
        links = self.ptt.Allpage()
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
        print(self.ptt.ptt_pack)
        return self.ptt.ptt_pack


    def Ptt_List_fn(self, client, detail):
        url = 'https://www.ptt.cc/bbs/Grad-ProbAsk/index.html'
        self.ptt.Ptt_Parse(url)
        end = self.ptt.ptt_pack
        self.wui.Send_Order(client, "Ptt_List", end)
        # print(end)

    def DB_Start(self, name, table):
        col = '"DATE" Text, "TITLE" Text, "url" Text'
        self.db.DBbld(name, table, col)

    def W2DB(self, data, table):
        for i in tqdm(data, desc='loading'):
            print(i)
            try:
                self.db.Add_DB(table, (i[0], i[1], i[2]))
            except:
                self.db.Add_DB(table, (i[0], i[1].replace("'", '"'), i[2]))

        self.db.DBoff()
        print('complete')

    def Export_json(self, url, filename):
        data = self.Grad_Data(url)
        with open(filename, 'w+', encoding='utf8') as f:
            f.write(json.dumps(data))

    def Export_txt(self, url, filename):
        data = self.Grad_Data(url)
        with open(filename, 'w+', encoding='utf8') as f:
            for i in data:
                f.write(i[0]+'@@'+i[1]+'@@'+i[2]+'@@@')

if __name__ == '__main__':
    obj = CTRL()
    url = 'https://www.ptt.cc/bbs/Grad-ProbAsk/index.html'

    # obj.ptt.Ptt_Parse(url)
    # obj.ptt.Get_Ptt(url)
    # obj.Ptt_Parse_Start_Thread()
    obj.Ptt_List_fn()

    # obj.DB_Start('PTT', 'GRAD')
    # obj.W2DB(data, 'GRAD')







