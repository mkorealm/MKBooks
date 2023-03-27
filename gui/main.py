import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.messagebox import showerror, showwarning, showinfo as mb
from database.connection.connect import database
from database.connection.config import con

BG_COL = "#212121"
FG_COL = "#00BFFF"

class Windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("MKBooks")
        self.resizable(False, False)
        try:
            self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id()))
            # fix for some devices
        except:
            self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

        container = tk.Frame(self, height=400, width=600)
        container.pack(side="top", fill="both", expand=True)
        container.grid(row=0, column=0)

        self.frames = {}
        for F in (Oauth, Registration, Books):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Oauth)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Oauth(tk.Frame):
    def __init__(self, parent, controller):
        def oauth():
            log = logEntry.get()
            pas = pasEntry.get()

            conect = database(host=con[0],
                           port=con[1],
                           user=con[2],
                           password=con[3],
                           database=con[4],
                           charset=con[5])
            res = database.select(conect, log)
            message = "Неверный логин или пароль!"
            if res==None:
                showerror("Ошибка", message)
            elif str(log)==res['login'] and str(pas)==res['password']:
                print("Successful!")
                return controller.show_frame(Books)
            elif str(pas)!=res['password']:
                showerror("Ошибка", message)

        tk.Frame.__init__(self, parent)
        self.configure(background=BG_COL)
        # styles
        style = ttk.Style()
        style.configure("TButton", relief="flat", background=BG_COL)
        style.configure("BW.TLabel", foreground=FG_COL)
        style.configure("TButton", foreground=FG_COL, background=BG_COL)

        # fonts style
        defaultFont = font.Font(family="TkDefaultFont:", size=12, weight="normal")
        entryFont = font.Font(family="TkTextFont:", size=14, weight="bold")
        regFont = font.Font(family="TkDefaultFont:", size=10, weight="normal")

        # authorization container
        oauthContainer = tk.LabelFrame(self, padx=15, pady=10, text="Авторизация", foreground=FG_COL, font=defaultFont)
        oauthContainer.configure(background=BG_COL)
        oauthContainer.pack(padx=10, pady=5)

        # items oauthContainer
        logLabel = tk.Label(oauthContainer, text="ЛОГИН", font=entryFont, foreground=FG_COL, background=BG_COL).grid(row=0)
        pasLabel = tk.Label(oauthContainer, text="ПАРОЛЬ", font=entryFont, foreground=FG_COL, background=BG_COL).grid(row=2)
        logEntry = tk.Entry(oauthContainer)
        logEntry.grid(row=1)
        pasEntry = tk.Entry(oauthContainer)
        pasEntry.grid(row=3)

        self.btn_submit = tk.Button(self,
                                    text="Войти",
                                    font= defaultFont,
                                    command=oauth)
        self.btn_submit.pack(padx=10, pady=10, side=tk.RIGHT)

        # reg
        regLabel = tk.Label(self, text="Нет акканта?", font=regFont, foreground=FG_COL, background=BG_COL).pack()
        regBtn = tk.Button(self,
                           text="Регистрация",
                           font=regFont,
                           command=lambda: controller.show_frame(Registration))
        regBtn.pack()

class Registration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # fonts style
        default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")
        entry_font = font.Font(family="TkTextFont:", size=14, weight="bold")
        reg_font = font.Font(family="TkDefaultFont:", size=10, weight="normal")

        label = tk.Label(self,
                         text="Введите логин",
                         font=default_font)
        label.grid(row=4)

class Books(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,
                         text="Successful")
        label.grid(row=4)