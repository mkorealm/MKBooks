def open_value():
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font

    from main import Account, connect, script_dir

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
        root.destroy()

    root = tk.Tk()
    root.configure(background=bg_col)

    def close_win():
        root.quit()

    def min_win():
        global w
        root.withdraw()
        root.overrideredirect(False)
        root.iconify()
        w = 1

    def win(event):
        global w
        root.overrideredirect(True)
        if w == 1:
            w = 0

    def get_pos(event):
        global xwin
        global ywin

        xwin = event.x
        ywin = event.y

    def move_app(event):
        root.geometry(f"+{event.x_root - xwin}+{event.y_root - ywin}")

    # titlebar configure
    global w
    root.resizable(False, False)
    root.overrideredirect(True)
    root.bind("<Map>", win)
    w = 0

    # titlebar
    title_bar = tk.Frame(root, bg=bg_col, relief="raised", bd=1)
    title_bar.pack(expand=1, fill="x")
    title_bar.bind("<Button-1>", get_pos)
    title_bar.bind("<B1-Motion>", move_app)

    title_label = tk.Label(title_bar, text="MKBooks", bg=bg_col, fg="White")
    title_label.pack(side="left", pady=2)

    # root.close_icon = tk.PhotoImage(file=script_dir + "\\resources\\close.png")
    # root.close_icon = root.close_icon.subsample(25, 25)
    # close_btn = tk.Button(title_bar, bg=bg_col, image=root.close_icon, relief="flat", command=close_win)
    # close_btn.pack(side="right")
    #
    # root.collapse_btn = tk.PhotoImage(file=script_dir + "\\resources\\minus.png")
    # root.collapse_btn = root.collapse_btn.subsample(25, 25)
    # collapse_btn = tk.Button(title_bar, bg=bg_col, image=root.collapse_btn, relief="flat", command=min_win)
    # collapse_btn.pack(side="right")

    # center win
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 2.25 - windowWidth / 2)
    # positionDown = int(root.winfo_screenheight() / 3 - windowHeight / 2)

    root.geometry("+{}+{}".format(positionRight, windowHeight))

    # fonts style
    default_font = font.Font(family="TkDefaultFont:", size=12, weight="normal")

    # account account_container
    account_container = tk.LabelFrame(root, padx=115, pady=60)
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

    root.mainloop()
