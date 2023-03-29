import os
import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter.messagebox import showerror

from database.connection.config import con
from database.connection.connect import database
from func.validation_of_password import validate_password

script_dir = os.path.dirname(__file__)

bg_col = "#212121"
fg_col = "#00BFFF"

connect = database(host=con[0], port=con[1], user=con[2], password=con[3], database=con[4], charset=con[5])


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

        container = tk.Frame(self, height=400, width=600, background=bg_col)
        container.pack(side="top", fill="both", expand=True)
        container.grid(row=0, column=0)

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
        log_entry.grid(row=1)
        pas_entry = tk.Entry(oauth_container, show="*")
        pas_entry.grid(row=3)

        self.btn_submit = tk.Button(self, text="Войти", font=default_font, command=oauth)
        self.btn_submit.pack(padx=10, pady=10, side=tk.TOP)

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
                showerror("Ошибка", Exception)

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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=bg_col)

        def open_main(event):
            controller.show_frame(Main)
            Main.login = self.login

        def open_value():
            def update(event):
                connect.update(name_entry.get(), surname_entry.get(), email_entry.get(), phone_entry.get(),
                               passport_entry.get())

            win = tk.Tk()
            win.title("Input Value")
            win.resizable(False, False)
            win.configure(background=bg_col)
            try:
                win.eval('tk::PlaceWindow %s center' % win.winfo_pathname(win.winfo_id()))
            # fix for some devices
            except:
                win.eval('tk::PlaceWindow %s center' % win.winfo_toplevel())
            default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")

            style = ttk.Style()
            style.configure("Acc.TLabel", font=default_font, foreground="#f2f2f2", background="#313131",
                            relief="raised")
            style.configure("Tap.TLabel", font=default_font, foreground="#f2f2f2", background="#313131")

            # account account_container
            account_container = tk.LabelFrame(win, padx=115, pady=60)
            account_container.configure(background=bg_col)
            account_container.bind("<Button>", set_login)
            account_container.pack(fill="both", side="bottom")

            # items account_container
            name_label = tk.Label(account_container, text="Ваше имя: ", font=default_font, foreground=fg_col,
                                  background=bg_col)
            name_label.grid(row=1, sticky="nw", ipady=4)
            name_entry = tk.Entry(account_container, font=default_font, foreground=fg_col, background=bg_col)
            name_entry.grid(row=1, column=1, sticky="nw", ipady=4)

            surname_label = tk.Label(account_container, text="Ваша фамилия: ", font=default_font, foreground=fg_col,
                                     background=bg_col)
            surname_label.grid(row=2, sticky="nw", ipady=4)
            surname_entry = tk.Entry(account_container, font=default_font, foreground=fg_col, background=bg_col)
            surname_entry.grid(row=2, column=1, sticky="nw", ipady=4)

            email_label = tk.Label(account_container, text="Ваша почта: ", font=default_font, foreground=fg_col,
                                   background=bg_col)
            email_label.grid(row=3, sticky="nw", ipady=4)
            email_entry = tk.Entry(account_container, font=default_font, foreground=fg_col, background=bg_col)
            email_entry.grid(row=3, column=1, sticky="nw", ipady=4)

            phone_label = tk.Label(account_container, text="Ваш номер телефона: ", font=default_font, foreground=fg_col,
                                   background=bg_col)
            phone_label.grid(row=4, sticky="nw", ipady=4)
            phone_entry = tk.Entry(account_container, font=default_font, foreground=fg_col, background=bg_col)
            phone_entry.grid(row=4, column=1, sticky="nw", ipady=4)

            passport_label = tk.Label(account_container, text="Ваш паспорт: ", font=default_font, foreground=fg_col,
                                      background=bg_col)
            passport_label.grid(row=5, sticky="nw", ipady=4)
            passport_entry = tk.Entry(account_container, font=default_font, foreground=fg_col, background=bg_col)
            passport_entry.grid(row=5, column=1, sticky="nw", ipady=4)

            btn_update = tk.Button(account_container, text="Отправить настройки", font=default_font)
            btn_update.bind("<Button>", update)
            btn_update.grid(row=6, sticky="nsew")

            win.mainloop()

        def set_login(event):
            res = connect.select_account(self.login)
            name_label_view["text"] = res['name']
            surname_label_view["text"] = res['surname']
            email_label_view["text"] = res['email']
            phone_label_view["text"] = res['phone']
            passport_label_view["text"] = res['passport']

        default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")

        style = ttk.Style()
        style.configure("Acc.TLabel", font=default_font, foreground="#f2f2f2", background="#313131", relief="raised")
        style.configure("Tap.TLabel", font=default_font, foreground="#f2f2f2", background="#313131")

        # account account_container
        account_container = tk.LabelFrame(self, padx=15, pady=10)
        account_container.configure(background=bg_col)
        account_container.bind("<Button>", set_login)
        account_container.pack(fill="both", side="bottom", padx=100, pady=50)

        account_menu = ttk.Label(self, style="Acc.TLabel", text="Главное меню", background=bg_col)
        account_menu.pack(anchor="nw")
        account_menu.bind("<Button>", open_main)

        label = ttk.Label(self, style="Tap.TLabel", text="Кликните чтобы продолжить", background=bg_col)
        label.bind("<Button>", set_login)
        label.pack(anchor="n")

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
        btn_update.grid(row=6, sticky="nsew")

        self.bind("<Button>", set_login)


class Main(tk.Frame):
    login = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def open_account(event):
            controller.show_frame(Account)
            Account.login = self.login

        def set_login(event):
            connect.select_account(self.login)

        default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")

        style = ttk.Style()
        style.configure("Acc.TLabel", font=default_font, foreground="#f2f2f2", background="#313131", relief="raised")

        menu_container = tk.LabelFrame(self)
        menu_container.configure(background=bg_col)
        menu_container.pack(fill="x", side="top")

        main_container = tk.LabelFrame(self, text="MKBooks", foreground=fg_col, font=default_font, padx=15, pady=10)
        main_container.configure(background=bg_col)
        main_container.pack(padx=100, pady=50)
        main_container.bind("<Button>", set_login)

        account_menu = ttk.Label(menu_container, style="Acc.TLabel", text="Аккаунт")
        account_menu.pack(side="left")
        account_menu.bind("<Button>", open_account)

        label = tk.Label(main_container, text="Кликните чтобы продолжить", font=default_font, foreground=fg_col,
                         background=bg_col)
        label.grid()
        label.bind("<Button>", set_login)
