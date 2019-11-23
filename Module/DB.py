import sqlite3 as lite
import os

class DB:
    def __init__(self):
        self.conn = []
        self.cursor = []

    def DB_dir(self):
        db_dir = os.path.join(os.path.abspath(os.path.pardir)+ '\Database')
        print(os.path.abspath(os.path.pardir) + db_dir)
        if not os.path.exists(db_dir):
            os.mkdir(db_dir)
        return db_dir

    def DBon(self, name):
        db_dir = self.DB_dir()
        # print(db_dir+ '\{}.sqlite3'.format(name))
        self.conn = lite.connect(db_dir+ '\{}.sqlite3'.format(name))
        self.cursor = self.conn.cursor()

    def DBbld(self, name, table, col):
        sqlstr = "CREATE TABLE IF NOT  EXISTS {} ({})".format(table, col)
        self.cursor.execute(sqlstr)

    def DBoff(self):
        self.conn.commit()
        self.conn.close()

    def In_DB(self, table, value):
        # print('insert into {} value {}'.format(table, value))
        sqlstr = "insert into {} values {}".format(table, value)
        # sqlstr = "insert into {} values (1, '2', '3', 'test')"
        self.cursor.execute(sqlstr)

    def Del_DB(self, table, col):
        sqlstr = "delete from {} where {}".format(table, col)
        self.conn.execute(sqlstr)

    def Del_table(self, table):
        sqlstr = "DROP TABLE {}".format(table)
        self.conn.execute(sqlstr)

    def Up_DB(self, table, update, where):
        sqlstr = "update {} set {} where {}".format(table, update, where)
        self.conn.execute(sqlstr)

    def Sch_DB(self, table):
        self.cursor = self.conn.execute('select * from {}'.format(table))
        rows = self.cursor.fetchall()
        print(rows)
        return rows


if __name__ == '__main__':
    # test
    obj = DB()
    obj.DB_dir()
    obj.DBon('test')

    col = '"date" Text, "title" Text, "url" Text'
    obj.DBbld('test', 'table01', col)

    # obj.In_DB('table01', ('2', '5', 'test'))
    # obj.Del_DB('table01', 'title')
    # obj.Del_table('table01')
    # obj.Up_DB('table01', 'title="我"', 'date=2')
    # obj.Sch_DB('table01')
    #
    obj.DBoff()