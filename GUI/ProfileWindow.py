import tkinter as tk
import customtkinter as ctk
import GUI.MainWindow as gui
import BaH.App as application

class ProfileWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.app = application.App()
        self.init_profile_window()

    def init_profile_window(self) -> None:
        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.label_rigisration = ctk.CTkLabel(self.root,text = "Зарегестрироваться", font=self.fontmini, text_color = "#3473e0", cursor = "hand2")
        self.label_rigisration.pack(anchor = tk.E, pady=1, padx=1)
        self.label_rigisration.bind("<Enter>", self.color_enter)
        self.label_rigisration.bind("<Leave>", self.color_leave)
        self.label_rigisration.bind("<Button-1>", self.registration)



        self.frame_user_data = ctk.CTkFrame(self.root, width=500, height=220) 
        self.frame_user_data.pack(side=tk.TOP)
        self.frame_user_data.pack_propagate(False)

        label_login = ctk.CTkLabel(self.frame_user_data,text = "Ведите логин", font=self.font_, width = 400)
        label_login.pack(anchor = tk.CENTER, pady=2)

        entry_login = ctk.CTkEntry(self.frame_user_data, width = 400)
        entry_login.pack(anchor = tk.CENTER, pady=2)

        label_password = ctk.CTkLabel(self.frame_user_data,text = "Ведите пароль", font=self.font_, width = 400)
        label_password.pack(anchor = tk.CENTER, pady=2)

        entry_password = ctk.CTkEntry(self.frame_user_data, width = 400)
        entry_password.pack(anchor = tk.CENTER, pady=2)

        self.button_autorization = ctk.CTkButton(self.frame_user_data, text = "Войти",command = self.open_main_window)
        self.button_autorization.pack(anchor = tk.S, pady = 10)


    def color_enter(self, event):
        self.label_rigisration.configure(text_color = "#2113bf")

    def color_leave(self, event):
        self.label_rigisration.configure(text_color = "#3473e0")

    def registration(self, event):
        self.label_rigisration.configure(text = "Авторизироваться")
        self.button_autorization.configure(text = "Зарегестрироваться")
        self.label_rigisration.unbind(event)
        self.label_rigisration.bind("<Button-1>", self.autorization)

    def autorization(self, event):
        self.label_rigisration.configure(text = "Зарегестрироваться")
        self.button_autorization.configure(text = "Войти")
        self.label_rigisration.unbind(event)
        self.label_rigisration.bind("<Button-1>", self.registration)

    def open_main_window(self):
        gui.MainWindow(self.root, self.app)

    