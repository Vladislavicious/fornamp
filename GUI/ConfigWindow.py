import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

from BaH.App import App


class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, root, app : App, main_window):
        self.root = root
        super().__init__(root)
        self.main_window = main_window
        self.app = app
        self.file_manager = app.file_manager
        self.init_dialog_window()

    def init_dialog_window(self):

        self.title("Подтверждение действия")
        self.geometry("450x200+525+340")
        self.resizable(False, False)
        self.transient(self.main_window)

        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        label_recipient = ctk.CTkLabel(self, text="Вы уверены, что хотите сменить папку хранения заказов?")
        label_recipient.pack(anchor=tk.CENTER, pady=2)

        self.button_send = ctk.CTkButton(self, text="Да", command=self.yes)
        self.button_send.place(relx=0.1, rely=0.75)

        self.button_send_me = ctk.CTkButton(self, text="Отменить", command=self.no)
        self.button_send_me.place(relx=0.575, rely=0.75)

        self.label_warning = ctk.CTkLabel(self, text="", font=self.fontmini, width=450, height=5,
                                          text_color="#d11515", justify=tk.CENTER)
        self.label_warning.place(relx=0, rely=0.9)

    def close_window(self):
        self.destroy()

    def yes(self):
        orders_drectory = self.file_manager.orders_dir_path
        filepath = filedialog.askdirectory(initialdir=orders_drectory,
                                           title="Выберите папку")
        if filepath != "" and filepath != orders_drectory:
            self.file_manager.changeConfig(orders_dir_path=filepath)
            self.close_window()

    def no(self):
        self.close_window()


# TO DO: После изменения конфига, необходимо почистить всё в нынешнем App - удалить из оперативы Ордеры,
# Превью и прочее
