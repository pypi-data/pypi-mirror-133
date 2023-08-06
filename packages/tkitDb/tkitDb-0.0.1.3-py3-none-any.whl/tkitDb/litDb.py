# -*- coding: utf-8 -*-
"""
作者：　terrychan
Blog: https://terrychan.org
# 说明：
https://docs.python.org/3/library/sqlite3.html
"""
import os
import sqlite3
import pandas


class Lit3Db:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.db_path = os.path.join(os.path.dirname(__file__), 'lit.db')

    def conn(self):
        """
        conn db


        :return:
        """
        self.db = sqlite3.connect(self.db_path)
        self.cursor = self.db.cursor()

    def save(self):
        self.db.commit()

    def close(self):
        """
        closs db
        :return:
        """
        self.db.close()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')

    def add(self):
        self.cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    def get_item(self):
        for row in self.cursor.execute('SELECT * FROM stocks ORDER BY price'):
            yield row

    def csv_to_sql(self, csv_file, table_name="csv_import"):
        df = pandas.read_csv(csv_file)
        df.to_sql(table_name, self.db, if_exists='replace', index=False)

    def get_csv(self, table_name="csv_import"):
        for row in self.cursor.execute('SELECT * FROM csv_import'):
            yield row

    def panda_to_sql(self, df: pandas.DataFrame, table_name="panda_import"):
        """
        import pandas dataframe to sqlite

        :param df:
        :param table_name:
        :return:
        """
        df.to_sql(table_name, self.db, if_exists='replace', index=False)

    def table_info(self, sql):
        for row in self.cursor.execute(sql):
            yield row

    def select(self, sql):
        for row in self.cursor.execute(sql):
            yield row

    def update(self, sql):
        self.cursor.execute(sql)

    def delete(self, sql):
        self.cursor.execute(sql)

    def create_index(self, sql):
        self.cursor.execute(sql)

    def drop_index(self, sql):
        self.cursor.execute(sql)

    def create_trigger(self, sql):
        self.cursor.execute(sql)

    def drop_trigger(self, sql):
        self.cursor.execute(sql)

    def create_view(self, sql):
        self.cursor.execute(sql)

    def drop_view(self, sql):
        self.cursor.execute(sql)

    def kv_set(self, key, value):
        self.cursor.execute("INSERT INTO kv VALUES ('{}','{}')".format(key, value))

    def kv_get(self, key):
        for row in self.cursor.execute("SELECT * FROM kv WHERE key='{}'".format(key)):
            yield row


if __name__ == '__main__':
    db = Lit3Db()
    db.conn()
    # db.create_table()
    db.add()
    db.save()
    #
    # db.csv_to_sql("/mnt/data/dev/github/tkitDb/data/ratings.csv")
    #
    # for it in db.get_csv():
    #     print(it)
    db.close()
    pass
