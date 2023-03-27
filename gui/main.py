import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.messagebox import showerror, showwarning, showinfo
from database.connection.connect import database
from database.connection.config import con
from func.validation_of_password import validate_password

bg_col = "#212121"
fg_col = "#00BFFF"

connect = database(host=con[0],
                               port=con[1],
                               user=con[2],
                               password=con[3],
                               database=con[4],
                               charset=con[5])
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
        for F in (Oauth, Registration, Account, Books):
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
            if res==None:
                showerror("Ошибка", message)
            elif str(log).lower()==res['login'].lower() and str(pas)==res['password']:
                print("Successful!")
                return controller.show_frame(Account)
            elif str(pas)!=res['password']:
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
        oauth_container = tk.LabelFrame(self, padx=15, pady=10, text="Авторизация", foreground=fg_col, font=default_font)
        oauth_container.configure(background=bg_col)
        oauth_container.pack(padx=100, pady=50)

        # items oauth_container
        log_label = tk.Label(oauth_container, text="ЛОГИН", font=entry_font, foreground=fg_col, background=bg_col).grid(row=0)
        pas_label = tk.Label(oauth_container, text="ПАРОЛЬ", font=entry_font, foreground=fg_col, background=bg_col).grid(row=2)
        log_entry = tk.Entry(oauth_container)
        log_entry.grid(row=1)
        pas_entry = tk.Entry(oauth_container)
        pas_entry.grid(row=3)

        self.btn_submit = tk.Button(self,
                                    text="Войти",
                                    font= default_font,
                                    command=oauth)
        self.btn_submit.pack(padx=10, pady=10, side=tk.TOP)

        # reg
        reg_label = tk.Label(self, text="Нет акканта?", font=reg_font, foreground=fg_col, background=bg_col).pack(side=tk.LEFT)
        reg_btn = tk.Button(self,
                           text="Регистрация",
                           font=reg_font,
                           command=lambda: controller.show_frame(Registration))
        reg_btn.pack(side=tk.LEFT)

class Registration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background=bg_col)
    def registration(self, arg1, arg2):
        log = arg1
        pas = arg2
        res = database.select_account(connect, log)
        if res == None:
            if validate_password(pas) == False:
                pass
            else:
                database.insert_account(connect, log, validate_password(pas))
        elif str(log).lower() == res['login'].lower():
            print("Такой аккаунт уже существует!")
        else:
            print("Error")
        # fonts style
        default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")
        entry_font = font.Font(family="TkTextFont:", size=14, weight="bold")
        reg_font = font.Font(family="TkDefaultFont:", size=10, weight="normal")

        reg_container = tk.LabelFrame(self, padx=15, pady=10)
        reg_container.configure(background=bg_col)
        reg_container.pack(padx=100, pady=50)

        log_label = tk.Label(reg_container, text="Введите логин", font=default_font, foreground=fg_col, background=bg_col)
        log_label.grid(row=0, sticky="nw")
        reg_label = tk.Label(reg_container, text="Введите пароль", font=default_font, foreground=fg_col, background=bg_col)
        reg_label.grid(row=2, sticky="nw")

        log_entry = tk.Entry(reg_container)
        log_entry.grid(row=1)
        pas_entry = tk.Entry(reg_container)
        pas_entry.grid(row=3)
        self.btn_submit = tk.Button(self,
                                    text="Регистрация",
                                    font=default_font,
                                    command=Registration.registration(log_entry.get(), pas_entry.get()))
        self.btn_submit.pack(padx=10, pady=10, side=tk.TOP)

class Account(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # authorization account_container
        account_container = tk.LabelFrame(self, padx=115, pady=60)
        account_container.configure(background=bg_col)
        account_container.pack(fill="both", side=tk.LEFT)

        name_label = tk.Label(account_container,
                              text="Ваше имя: ")
        name_label.grid(row=0, sticky="nw")
        name_label_view = tk.Label(account_container)
        name_label_view.grid(row=0, column=1, sticky="nw")

        surname_label = tk.Label(account_container,
                              text="Ваша фамилия: ")
        surname_label.grid(row=1, sticky="nw")
        surname_label_view = tk.Label(account_container)
        surname_label_view.grid(row=1, column=1, sticky="nw")

        email_label = tk.Label(account_container,
                                 text="Ваша почта: ")
        email_label.grid(row=2, sticky="nw")
        email_label_view = tk.Label(account_container)
        email_label_view.grid(row=2, column=1, sticky="nw")

        phone_label = tk.Label(account_container,
                               text="Ваш номер телефона: ")
        phone_label.grid(row=3, sticky="nw")
        phone_label_view = tk.Label(account_container)
        phone_label_view.grid(row=3, column=1, sticky="nw")

        passport_label = tk.Label(account_container,
                               text="Ваш паспорт: ")
        passport_label.grid(row=4, sticky="nw")
        passport_label_view = tk.Label(account_container)
        passport_label_view.grid(row=4, column=1, sticky="nw")
class Books(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,
                         text="Successful")
        label.grid(row=0)