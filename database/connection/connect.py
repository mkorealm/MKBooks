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

    def select(self, arg):
        with self.con.cursor() as cur:
            cur.execute(f"SELECT * FROM customers WHERE login='{arg}'")
            res = cur.fetchone()
        return res