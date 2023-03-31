import pymysql
from gui.main import *

lst = []


class database:
    def __init__(self, host, port, user, password, database, charset):
        self.con = pymysql.connect(host=host,
                                   port=port,
                                   user=user,
                                   password=password,
                                   database=database,
                                   charset=charset,
                                   cursorclass=pymysql.cursors.DictCursor)

    def select_account(self, arg):
        with self.con.cursor() as cur:
            cur.execute(f"SELECT * FROM customers WHERE login='{arg}'")
            res = cur.fetchone()
        return res

    def insert_account(self, arg1, arg2, arg3):
        with self.con.cursor() as cur:
            insert = f"INSERT INTO customers(name, login, password) VALUES ('{arg1}', '{arg2}', '{arg3}')"
            cur.execute(insert)
        self.con.commit()

    def update(self, login, *args):
        log = login
        res = self.select_account(log)
        with self.con.cursor() as cur:
            update = f"UPDATE customers SET name=%s, surname=%s, email=%s, phone=%s, passport=%s WHERE " \
                     f"name='{res['name']}' AND surname='{res['surname']}' AND email='{res['email']}' AND " \
                     f"phone='{res['phone']}' AND passport='{res['passport']}'"
            cur.execute(update, args)
        self.con.commit()

    def select_column(self):
        with self.con.cursor() as cur:
            sql = f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'customers'"
            cur.execute(sql)
            res = cur.fetchall()
            for i in res:
                lst.append(i['COLUMN_NAME'])
            filt = ['email', 'id', 'login', 'name', 'passport', 'password', 'phone', 'surname']
            lst2 = list(filter(lambda x: x != lst, filt))
            return lst2
