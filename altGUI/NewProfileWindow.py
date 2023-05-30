import tkinter as tk
import customtkinter as ctk
from altGUI.NewMainWindow import NewMainWindow
import BaH.App as application

class NewProfileWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.app = application.App()
        self.user_handler = self.app.file_manager.user_handler
        self.init_profile_window()

    def init_profile_window(self) -> None:
        if(self.user_handler.lastUser != None):
            self.user_handler.Authorize(self.user_handler.lastUser.login, self.user_handler.lastUser.password)
            self.open_main_window()
        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.label_rigisration = ctk.CTkLabel(self.root,text = "Зарегестрироваться", font=self.fontmini, text_color = "#3473e0", cursor = "hand2")
        self.label_rigisration.pack(anchor = tk.E, pady=1, padx=5)
        self.label_rigisration.bind("<Enter>", self.color_enter)
        self.label_rigisration.bind("<Leave>", self.color_leave)
        self.label_rigisration.bind("<Button-1>", self.theme_registration)



        self.frame_user_data = ctk.CTkFrame(self.root, width=500, height=220)
        self.frame_user_data.pack(side=tk.TOP)
        self.frame_user_data.pack_propagate(False)

        label_login = ctk.CTkLabel(self.frame_user_data,text = "Ведите логин", font=self.font_, width = 400)
        label_login.pack(anchor = tk.CENTER, pady=2)

        self.entry_login = ctk.CTkEntry(self.frame_user_data, width = 400)
        self.entry_login.pack(anchor = tk.CENTER, pady=2)

        label_password = ctk.CTkLabel(self.frame_user_data,text = "Ведите пароль", font=self.font_, width = 400)
        label_password.pack(anchor = tk.CENTER, pady=2)

        self.entry_password = ctk.CTkEntry(self.frame_user_data, width = 400, show = '*')
        self.entry_password.pack(anchor = tk.CENTER, pady=2)


        self.combobox_post = ctk.CTkComboBox(self.frame_user_data, width = 160, state = "readonly", values=["Рабочий", "Начальник"])
        self.combobox_post.set("Рабочий")

        self.button_autorization = ctk.CTkButton(self.frame_user_data, text = "Войти",command = self.autorization)
        self.button_autorization.pack(anchor = tk.S, pady = 10)

        self.label_warning = ctk.CTkLabel(self.frame_user_data, text = "", font=self.fontmini, width = 500, height=5, text_color = "#d11515", justify = tk.CENTER)
        self.label_warning.place(relx=0, rely=0.9)




    def color_enter(self, event):
        self.label_rigisration.configure(text_color = "#2113bf")

    def color_leave(self, event):
        self.label_rigisration.configure(text_color = "#3473e0")

    def theme_registration(self, event):
        self.cancel_error()

        self.button_autorization.configure(text = "Зарегестрироваться", command = self.registration)
        self.button_autorization.place(relx = 0.55, rely=0.75)
        self.combobox_post.place(relx = 0.15, rely=0.75)

        self.label_rigisration.configure(text = "Авторизироваться")
        self.label_rigisration.unbind(event)
        self.label_rigisration.bind("<Button-1>", self.theme_autorization)

    def theme_autorization(self, event):

        self.button_autorization.configure(text = "Войти", command = self.autorization)
        self.button_autorization.place(relx = 0.36, rely=0.75)
        self.combobox_post.place(relx = 1.3, rely=0.8)

        self.label_rigisration.configure(text = "Зарегестрироваться")
        self.label_rigisration.unbind(event)
        self.label_rigisration.bind("<Button-1>", self.theme_registration)


    def check_fielde(self):
        check = True



        return check

    def cancel_error(self):
        self.entry_login.configure(fg_color="#f9f9fa", border_color= "#979da2")
        self.entry_password.configure(fg_color="#f9f9fa", border_color= "#979da2")
        self.label_warning.configure(text = "")


    def registration(self):
        self.cancel_error()

        list_errors = list()
        if(self.combobox_post.get() == "Рабочий"):
            list_errors = self.user_handler.NewUser(self.entry_login.get(), self.entry_password.get())
        else:
            list_errors = self.user_handler.NewUser(self.entry_login.get(), self.entry_password.get(), isAdministrator = True)

        for error in list_errors:
            key = list(error)
            if(key[0] == 1):
                self.entry_login.configure(fg_color="#faebeb", border_color= "#e64646")
                self.label_warning.configure(text = error[1])
            elif(key[0] == 2):
                self.label_warning.configure(text = error[2])
                self.entry_password.configure(fg_color="#faebeb", border_color= "#e64646")
            elif(key[0] == 0):
                self.autorization()



    def autorization(self):
        if(self.user_handler.Authorize(self.entry_login.get(), self.entry_password.get()) == True):
            self.user_handler.markAsLastUser(self.entry_login.get())
            self.entry_login.delete(0, len(self.entry_login.get()))
            self.entry_password.delete(0, len(self.entry_password.get()))
            self.cancel_error()
            self.open_main_window()
        else:
            self.entry_login.configure(fg_color="#faebeb", border_color= "#e64646")
            self.entry_password.configure(fg_color="#faebeb", border_color= "#e64646")
            self.label_warning.configure( text = "Неправильный логин или пароль")




    def open_main_window(self):
        NewMainWindow(self.root, self.app)
