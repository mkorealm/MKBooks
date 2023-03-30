def open_value():
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font

    from main import Account, connect

    bg_col = "#212121"
    fg_col = "#00BFFF"

    def update():
        if name_entry.get() == "":
            name_entry.insert(0, Account.name)
        if surname_entry.get() == "":
            surname_entry.insert(0, Account.surname)
        if email_entry.get() == "":
            email_entry.insert(0, Account.email)
        if phone_entry.get() == "":
            phone_entry.insert(0, Account.phone)
        if passport_entry.get() == "":
            passport_entry.insert(0, Account.passport)
        else:
            pass
        connect.update(Account.login, name_entry.get(), surname_entry.get(), email_entry.get(), phone_entry.get(),
                       passport_entry.get())
        win.destroy()

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

    btn_update = tk.Button(account_container, text="Отправить данные", font=default_font, command=lambda: update())
    btn_update.grid(row=6, column=1, sticky="nsew")

    win.mainloop()
