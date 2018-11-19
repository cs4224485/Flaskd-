# Author: harry.cai
# DATE: 2018/9/2
import pymysql
import settings


class Mymeta(type):
    def __init__(self,name, bases, dic):
        self.__instance = None
        super(Mymeta, self).__init__(name, bases, dic)

    def __call__(self, *args, **kwargs):
        if not self.__instance:
            self.__instance = object.__new__(self)  # 产生对象
            self.__init__(self.__instance, *args, **kwargs)  # 初始化对象
        return self.__instance


class HandleMysql(metaclass=Mymeta):

    def db_connect(self):
        self.conn = settings.DefaultConfig.POOL.connection()
        self.cursor = self.conn.cursor()

    def db_close(self):
        self.cursor.close()
        self.conn.close()

    def insert(self, sql, *args):
        self.db_connect()
        self.cursor.execute(sql, args)
        row = self.conn.commit()
        self.db_close()
        return row

    def fetch_one(self, sql, *args):
        self.db_connect()
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        self.db_close()
        return result

    def fetch_all(self, sql, *args):
        self.db_connect()
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        self.db_close()
        return result


database = HandleMysql()


