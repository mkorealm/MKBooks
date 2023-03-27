import pymysql

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
    def insert_account(self, arg1, arg2):
        with self.con.cursor() as cur:
            cur.execute(f"INSERT INTO customers(login, password) VALUES ('{arg1}', '{arg2}')")
        self.con.commit()