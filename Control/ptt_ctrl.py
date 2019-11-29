from Module import ptt, DB
import json
from tqdm import tqdm


class CTRL:
    def __init__(self):
        self.ptt = ptt.PTT()
        self.db = DB.DB()

    def Grad_Data(self, url):
        self.ptt.Get_Ptt(url)
        datalst = self.ptt.Ptt_Parse_Start_Thread()
        return datalst

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
    data = obj.Grad_Data(url)

    obj.DB_Start('PTT', 'GRAD')
    obj.W2DB(data, 'GRAD')



    # obj.Export_txt(url, 'Ptt.txt')
    # obj.Export_json(url, 'Ptt.json')
    # obj.DB_Start(name='PTT', table='GRAD')
    # with open('Ptt.json', 'r+', encoding='utf8') as f:
    #     data = json.load(f)
    # obj.W2DB(data, 'PTT', 'GRAD')






