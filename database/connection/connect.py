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

    def insert_account(self, arg1, arg2, arg3):
        with self.con.cursor() as cur:
            insert = f"INSERT INTO customers(name, login, password) VALUES ('{arg1}', '{arg2}', '{arg3}')"
            print(insert)
            cur.execute(insert)
        self.con.commit()

    # def select_books(self):
    #     with self.con.cursor() as cur:
    #         cur.execute(f"SELECT title, year, price, surname, author.name, midname, country, genres.name, "
    #                     f"description FROM books, author, genres")
    #         res = cur.fetchall()
    #         print(res)
    #         cur.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=N'books'")
    #         b = cur.fetchall()
    #         b_lst = []
    #         cur.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=N'author'")
    #         a = cur.fetchall()
    #         a_lst = []
    #         cur.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=N'genres'")
    #         g = cur.fetchall()
    #         g_lst = []
    #         for i in b:
    #             b_lst.append(i['COLUMN_NAME'])
    #         for i in a:
    #             a_lst.append(i['COLUMN_NAME'])
    #         for i in g:
    #             g_lst.append(i['COLUMN_NAME'])
