import os
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter.messagebox import showerror

from database.connection.config import con
from database.connection.connect import database
from func.validation_of_password import validate_password
from gui.update_account import open_value

script_dir = os.path.dirname(__file__)

bg_col = "#212121"
fg_col = "#00BFFF"

connect = database(host=con[0], port=con[1], user=con[2], password=con[3], database=con[4], charset=con[5])


class Windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global w

        def close_win():
            self.quit()

        def min_win():
            global w
            self.withdraw()
            self.overrideredirect(False)
            self.iconify()
            w = 1

        def win(event):
            global w
            self.overrideredirect(True)
            if w == 1:
                w = 0

        def get_pos(event):
            global xwin
            global ywin

            xwin = event.x
            ywin = event.y

        def move_app(event):
            self.geometry(f"+{event.x_root - xwin}+{event.y_root - ywin}")

        # titlebar configure
        self.resizable(False, False)
        self.overrideredirect(True)
        self.bind("<Map>", win)
        w = 0

        # titlebar
        title_bar = tk.Frame(self, bg=bg_col, relief="raised", bd=1)
        title_bar.pack(expand=1, fill="x")
        title_bar.bind("<Button-1>", get_pos)
        title_bar.bind("<B1-Motion>", move_app)

        title_label = tk.Label(title_bar, text="MKBooks", bg=bg_col, fg="White")
        title_label.pack(side="left", pady=2)

        self.close_icon = tk.PhotoImage(file=script_dir + "\\resources\\close.png")
        self.close_icon = self.close_icon.subsample(25, 25)
        close_btn = tk.Button(title_bar, bg=bg_col, image=self.close_icon, relief="flat", command=close_win)
        close_btn.pack(side="right")

        self.collapse_btn = tk.PhotoImage(file=script_dir + "\\resources\\minus.png")
        self.collapse_btn = self.collapse_btn.subsample(25, 25)
        collapse_btn = tk.Button(title_bar, bg=bg_col, image=self.collapse_btn, relief="flat", command=min_win)
        collapse_btn.pack(side="right")

        # center win
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        positionRight = int(self.winfo_screenwidth() / 2.25 - windowWidth / 2)
        # positionDown = int(self.winfo_screenheight() / 3 - windowHeight / 2)

        self.geometry("+{}+{}".format(positionRight, windowHeight))

        # try:
        #     self.eval('tk::PlaceWindow %s center' % self.winfo_pathname(self.winfo_id()))
        # # fix for some devices
        # except:
        #     self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

        container = tk.Frame(self, height=400, width=600, background=bg_col)
        container.pack(side="top", fill="both", expand=True)
        # container.grid(row=0, column=0)

        self.frames = {}
        for F in (Oauth, Registration, Main, Account, Main):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Oauth)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Oauth(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=bg_col)

        def oauth():
            log = log_entry.get()
            pas = pas_entry.get()

            res = database.select_account(connect, log)
            message = "Неверный логин или пароль!"
            if res == None:
                showerror("Ошибка", message)
            elif str(log).lower() == res['login'].lower() and str(pas) == res['password']:
                Main.login = log
                return controller.show_frame(Main)
            elif str(pas) != res['password']:
                showerror("Ошибка", message)

        # styles
        style = ttk.Style()
        style.configure("TButton", relief="flat", background=bg_col)
        style.configure("BW.TLabel", foreground=fg_col)
        style.configure("TButton", foreground=fg_col, background=bg_col)

        # fonts style
        default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")
        entry_font = font.Font(family="TkTextFont:", size=14, weight="bold")
        reg_font = font.Font(family="TkDefaultFont:", size=10, weight="normal")

        # authorization oauth_container
        oauth_container = tk.LabelFrame(self, padx=15, pady=10, text="Авторизация", foreground=fg_col,
                                        font=default_font)
        oauth_container.configure(background=bg_col)
        oauth_container.pack(padx=100, pady=50)

        # items oauth_container
        log_label = tk.Label(oauth_container, text="ЛОГИН", font=entry_font, foreground=fg_col, background=bg_col)
        log_label.grid(row=0)
        pas_label = tk.Label(oauth_container, text="ПАРОЛЬ", font=entry_font, foreground=fg_col, background=bg_col)
        pas_label.grid(row=2)

        log_entry = tk.Entry(oauth_container)
        # log_entry.bind("<>")
        log_entry.grid(row=1)
        pas_entry = tk.Entry(oauth_container, show="*")
        pas_entry.grid(row=3)

        btn_submit = tk.Button(self, text="Войти", font=default_font, command=oauth)
        btn_submit.pack(padx=10, pady=10)

        # reg
        reg_label = tk.Label(self, text="Нет акканта?", font=reg_font, foreground=fg_col, background=bg_col)
        reg_label.pack(side=tk.LEFT)
        reg_btn = tk.Button(self, text="Регистрация", font=reg_font,
                            command=lambda: controller.show_frame(Registration))
        reg_btn.pack(side=tk.LEFT)


class Registration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=bg_col)

        def registration():
            name = name_entry.get()
            log = log_entry.get()
            pas = pas_entry.get()
            res = database.select_account(connect, log)
            if res == None:
                if validate_password(pas) == False:
                    pass
                else:
                    Main.login = log
                    database.insert_account(connect, name, log, validate_password(pas))
                    return controller.show_frame(Main)
            elif str(log).lower() == res['login'].lower():
                showerror("Ошибка", "Такой аккаунт уже существует!")
            else:
                showerror("Ошибка", f"{Exception}")

        # fonts style
        default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")

        # registration reg_container
        reg_container = tk.LabelFrame(self, padx=15, pady=10)
        reg_container.configure(background=bg_col)
        reg_container.pack(padx=100, pady=50)

        # items reg_container
        name_label = tk.Label(reg_container, text="Введите имя:", font=default_font, foreground=fg_col,
                              background=bg_col)
        name_label.grid(row=0, sticky="nw")
        log_label = tk.Label(reg_container, text="Введите логин", font=default_font, foreground=fg_col,
                             background=bg_col)
        log_label.grid(row=2, sticky="nw")
        reg_label = tk.Label(reg_container, text="Введите пароль", font=default_font, foreground=fg_col,
                             background=bg_col)
        reg_label.grid(row=4, sticky="nw")

        name_entry = tk.Entry(reg_container)
        name_entry.grid(row=1)
        log_entry = tk.Entry(reg_container)
        log_entry.grid(row=3)
        pas_entry = tk.Entry(reg_container, show="*")
        pas_entry.grid(row=5)

        self.btn_submit = tk.Button(self, text="Регистрация", font=default_font, command=registration)
        self.btn_submit.pack(padx=10, pady=10, side=tk.TOP)


class Account(tk.Frame):
    login = None

    name = None
    surname = None
    email = None
    phone = None
    passport = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=bg_col)

        def open_main(event):
            controller.show_frame(Main)
            Main.login = self.login

        def set(event):
            res = connect.select_account(self.login)
            name_label_view["text"] = res['name']
            surname_label_view["text"] = res['surname']
            email_label_view["text"] = res['email']
            phone_label_view["text"] = res['phone']
            passport_label_view["text"] = res['passport']

            Account.name = name_label_view["text"]
            Account.surname = surname_label_view["text"]
            Account.email = email_label_view["text"]
            Account.phone = phone_label_view["text"]
            Account.passport = passport_label_view["text"]
            return

        # fonts style
        default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")

        style = ttk.Style()
        style.configure("Acc.TLabel", font=default_font, foreground="#f2f2f2", background=bg_col, relief="raised")

        # account account_container
        account_container = tk.LabelFrame(self, text="Аккаунт", foreground=fg_col,
                                          font=default_font, padx=15, pady=10)
        account_container.configure(background=bg_col)
        account_container.pack(fill="both", side="bottom", padx=100, pady=50)

        account_menu = ttk.Label(self, style="Acc.TLabel", text="Главное меню", background=bg_col)
        account_menu.pack(anchor="nw")
        account_menu.bind("<Button>", open_main)

        # items account_container
        name_label = tk.Label(account_container, text="Ваше имя: ", font=default_font, foreground=fg_col,
                              background=bg_col)
        name_label.grid(row=1, sticky="nw", ipady=4)
        name_label_view = tk.Label(account_container, font=default_font, foreground=fg_col, background=bg_col)
        name_label_view.grid(row=1, column=1, sticky="nw", ipady=4)

        surname_label = tk.Label(account_container, text="Ваша фамилия: ", font=default_font, foreground=fg_col,
                                 background=bg_col)
        surname_label.grid(row=2, sticky="nw", ipady=4)
        surname_label_view = tk.Label(account_container, font=default_font, foreground=fg_col, background=bg_col)
        surname_label_view.grid(row=2, column=1, sticky="nw", ipady=4)

        email_label = tk.Label(account_container, text="Ваша почта: ", font=default_font, foreground=fg_col,
                               background=bg_col)
        email_label.grid(row=3, sticky="nw", ipady=4)
        email_label_view = tk.Label(account_container, font=default_font, foreground=fg_col, background=bg_col)
        email_label_view.grid(row=3, column=1, sticky="nw", ipady=4)

        phone_label = tk.Label(account_container, text="Ваш номер телефона: ", font=default_font, foreground=fg_col,
                               background=bg_col)
        phone_label.grid(row=4, sticky="nw", ipady=4)
        phone_label_view = tk.Label(account_container, font=default_font, foreground=fg_col, background=bg_col)
        phone_label_view.grid(row=4, column=1, sticky="nw", ipady=4)

        passport_label = tk.Label(account_container, text="Ваш паспорт: ", font=default_font, foreground=fg_col,
                                  background=bg_col)
        passport_label.grid(row=5, sticky="nw", ipady=4)
        passport_label_view = tk.Label(account_container, font=default_font, foreground=fg_col, background=bg_col)
        passport_label_view.grid(row=5, column=1, sticky="nw", ipady=4)

        btn_update = tk.Button(account_container, text="Редактировать профиль", font=default_font, command=open_value)
        btn_update.bind("<Button>", set)
        btn_update.grid(row=6, sticky="nsew")

        self.bind("<Motion>", set)


class Main(tk.Frame):
    login = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=bg_col)

        def open_account(event):
            controller.show_frame(Account)
            Account.login = self.login

        def set_login(event):
            connect.select_account(self.login)

        # fonts style
        default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")

        style = ttk.Style()
        style.configure("Acc.TLabel", font=default_font, foreground="#f2f2f2", background=bg_col, relief="raised")

        account_menu = ttk.Label(self, style="Acc.TLabel", text="Аккаунт", background=bg_col)
        account_menu.pack(anchor="nw")
        account_menu.bind("<Button-1>", open_account)
