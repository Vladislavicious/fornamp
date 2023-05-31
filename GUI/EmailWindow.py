import tkinter as tk
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

        label_email = ctk.CTkLabel(self.frame_user_data,text = "Введите почту", font=self.font_, width = 400)
        label_email.pack(anchor = tk.CENTER, pady=2)

        self.entry_email = ctk.CTkEntry(self.frame_user_data, width = 400)
        self.entry_email.pack(anchor = tk.CENTER, pady=2)

        label_email_password = ctk.CTkLabel(self.frame_user_data,text = "Введите пароль от почты", font=self.font_, width = 400)
        label_email_password.pack(anchor = tk.CENTER, pady=2)

        self.entry_email_password = ctk.CTkEntry(self.frame_user_data, width = 400)
        self.entry_email_password.pack(anchor = tk.CENTER, pady=2)


        self.button_autorization = ctk.CTkButton(self.frame_user_data, text = "Зарегистрировать", command = self.registration)
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
                self.main_window.button_add_email.configure(text = "Редактировать\n данные почты")
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
        self.geometry("450x200+525+340")
        self.resizable(False, False)
        self.transient(self.main_window)

        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        label_recipient = ctk.CTkLabel(self, text = "Введите почту получателя")
        label_recipient.pack(anchor = tk.CENTER, pady = 2)

        self.entry_recipient = ctk.CTkEntry(self, width = 375)
        self.entry_recipient.pack(anchor = tk.CENTER, pady=2)

        label_message = ctk.CTkLabel(self, text = "Введите сообщение")
        label_message.pack(anchor = tk.CENTER, pady = 2)

        self.entry_message = ctk.CTkEntry(self, width = 375)
        self.entry_message.pack(anchor = tk.CENTER, pady=2)

        self.button_send = ctk.CTkButton(self, text = "Отправить", command = lambda: self.send_report(self.entry_recipient.get()))
        self.button_send.place(relx=0.1, rely=0.75)

        self.button_send_me = ctk.CTkButton(self, text = "Отправить себе", command = lambda: self.send_report(self.user.email))
        self.button_send_me.place(relx=0.575, rely=0.75)

        self.label_warning = ctk.CTkLabel(self, text = "", font=self.fontmini, width = 450, height=5, text_color = "#d11515", justify = tk.CENTER)
        self.label_warning.place(relx=0, rely=0.9)

    def close_window(self):
        self.destroy()

    def send_report(self, user):
        error = self.app.AuthentificateMail()
        if(error[0] != 0):
            self.label_warning.configure(text = error[1])
        elif(user == ""):
            self.label_warning.configure(text = "Введите почту получателя")
        else:
            text = self.entry_message.get()
            self.close_window()
            self.app.sendOtchetMail(user, text)
