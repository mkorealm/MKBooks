from database.connection.connect import database
from gui.main import *
from database.connection.config import con

if __name__=="__main__":
    # con = database(host=con[0],
    #                port=con[1],
    #                user=con[2],
    #                password=con[3],
    #                database=con[4],
    #                charset=con[5])
    # str  = "korolev"
    # res = database.select(con, str)
    # if str == res['login']:
    #     print("Successful!")
    window = Windows()
    # main.pack(side="top", fill="both", expand=True)
    # window.wm_geometry("400x400")
    # window.wm_title("MKBook")
    window.mainloop()