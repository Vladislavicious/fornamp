import tkinter as tk
from turtle import width
import customtkinter as ctk

class EmailWindow(ctk.CTkToplevel):
    def __init__(self, root, app, main_window):
        self.root = root

        super().__init__(root)
        self.main_window = main_window
        self.app = app
        self.user = self.app.file_manager.user_handler.lastUser
        self.user_handler = self.app.file_manager.user_handler
        self.init_email_window()

    def init_email_window(self):

        self.title("Регистрация почты")
        self.geometry("500x200+500+340")
        self.resizable(False, False)
        self.transient(self.main_window)

        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.frame_user_data = ctk.CTkFrame(self, width=500, height=200) 
        self.frame_user_data.pack(side=tk.TOP)
        self.frame_user_data.pack_propagate(False)

        label_email = ctk.CTkLabel(self.frame_user_data,text = "Ведите почту", font=self.font_, width = 400)
        label_email.pack(anchor = tk.CENTER, pady=2)

        self.entry_email = ctk.CTkEntry(self.frame_user_data, width = 400)
        self.entry_email.pack(anchor = tk.CENTER, pady=2)

        label_email_password = ctk.CTkLabel(self.frame_user_data,text = "Ведите пароль от почты", font=self.font_, width = 400)
        label_email_password.pack(anchor = tk.CENTER, pady=2)

        self.entry_email_password = ctk.CTkEntry(self.frame_user_data, width = 400)
        self.entry_email_password.pack(anchor = tk.CENTER, pady=2)


        self.button_autorization = ctk.CTkButton(self.frame_user_data, text = "Зарегестрировать",command = self.registration)
        self.button_autorization.pack(anchor = tk.S, pady = 10)

        self.label_warning = ctk.CTkLabel(self.frame_user_data, text = "", font=self.fontmini, width = 500, height=5, text_color = "#d11515", justify = tk.CENTER)
        self.label_warning.place(relx=0, rely=0.9)


    def registration(self):
        errors = self.user_handler.addEmailInfo(self.user_handler.lastUser,
                                       self.entry_email.get(),self.entry_email_password.get())
        text = ""
        for error in errors:
            key = list(error)
            if(key[0] == 0):
                self.user_handler.SaveToFile()
                self.main_window.button_add_email.destroy()
                self.destroy()
                return
            if(key[0] == 1):
                self.entry_email.configure(fg_color="#faebeb", border_color= "#e64646")
                text = error[1]
            elif(key[0] == 2):
                text = error[2]
                self.entry_email_password.configure(fg_color="#faebeb", border_color= "#e64646")
            self.label_warning.configure(text = text)


class DialogWindow(ctk.CTkToplevel):
    def __init__(self, root, app, main_window):
        self.root = root

        super().__init__(root)
        self.main_window = main_window
        self.app = app
        self.user = self.app.file_manager.user_handler.lastUser
        self.user_handler = self.app.file_manager.user_handler
        self.init_dialog_window()

    def init_dialog_window(self):

        self.title("Подтверждение действия")
        self.geometry("300x100+550+365")
        self.resizable(False, False)
        self.transient(self.main_window)

        label_confirm = ctk.CTkLabel(self, text = "Подтвердить отправку отчета?")
        label_confirm.pack(anchor = tk.N)

        self.button_yes = ctk.CTkButton(self, text = "Да", command = self.send_report, width = 100)
        self.button_yes.pack(side = tk.LEFT, padx = 20, pady = 20)

        self.button_no = ctk.CTkButton(self, text = "Нет", command = self.close_window , width = 100)
        self.button_no.pack(side = tk.RIGHT, padx = 20, pady = 20)

    def close_window(self):
        self.destroy()

    def send_report(self):
        self.app.AuthentificateMail()