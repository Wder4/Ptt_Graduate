import sqlite3 as lite
import os

class DB:
    def __init__(self):
        self.conn = []
        self.cursor = []

    def DB_dir(self):
        db_dir = os.path.join(os.path.abspath(os.path.pardir)+ '\Database')
        # print(os.path.abspath(os.path.pardir) + db_dir)
        if not os.path.exists(db_dir):
            os.mkdir(db_dir)
        return db_dir

    def DBon(self, name):
        db_dir = self.DB_dir()
        # print(db_dir+ '\{}.sqlite3'.format(name))
        self.conn = lite.connect(db_dir+ '\{}.sqlite3'.format(name))
        self.cursor = self.conn.cursor()

    def DBoff(self):
        self.conn.close()

    def DBbld(self, name, table, col):
        self.DBon(name)
        sqlstr = "CREATE TABLE IF NOT  EXISTS {} ({})".format(table, col)
        self.cursor.execute(sqlstr)
        self.conn.commit()

    def Add_DB(self, table, value):
        # print('insert into {} value {}'.format(table, value))
        # sqlstr = "insert into {} values {}".format(table, value)
        sqlstr = ("insert into {} values {}".format(table, value))
        # sqlstr = "insert into {} values (1, '2', '3', 'test')"

        self.cursor.execute(sqlstr)
        self.conn.commit()

    def Del_DB(self, table, col):
        sqlstr = "delete from {} where {}".format(table, col)
        self.conn.execute(sqlstr)
        self.conn.commit()

    def Del_table(self, table):
        sqlstr = "DROP TABLE {}".format(table)
        self.conn.execute(sqlstr)
        self.conn.commit()

    def Up_DB(self, table, update, where):
        sqlstr = "update {} set {} where {}".format(table, update, where)
        self.conn.execute(sqlstr)
        self.conn.commit()

    def Sch_DB(self, table):
        self.cursor = self.conn.execute('select * from {}'.format(table))
        rows = self.cursor.fetchall()
        print(rows)
        return rows


if __name__ == '__main__':
    # test
    obj = DB()
    # obj.DB_dir()


    col = '"date" Text, "title" Text, "url" Text'
    val = ['5/03', '[理工] Ay"+By\'+Cy = v (A,B,C是二乘二方陣 y,v是二乘一向量)', 'https://www.ptt.cc/bbs/Grad-ProbAsk/M.1399087810.A.C59.html']
    # obj.Add_DB('test', 'table01', (val[0], val[1], val[2]))
    obj.DBbld('test', 'table01', col)
    obj.Add_DB('table01', (val[0], val[1].replace("'", '"'), val[2]))
    obj.DBoff()


