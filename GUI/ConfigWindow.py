import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

from ioconnection.App import App


class ConfigWindow(ctk.CTkToplevel):
    def __init__(self, root, app: App, main_window):
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

        self.label = ctk.CTkLabel(self, text="Вы уверены, что хотите сменить папку хранения заказов?")
        self.label.pack(anchor=tk.CENTER, pady=2)

        self.button_confirm = ctk.CTkButton(self, text="Да", command=self.yes)
        self.button_confirm.place(relx=0.1, rely=0.75)

        self.button_undo = ctk.CTkButton(self, text="Отменить", command=self.no)
        self.button_undo.place(relx=0.575, rely=0.75)

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
            self.app.PreChangeOrderDir()
            self.file_manager.changeConfig(orders_dir_path=filepath)
            self.app.PostChangeOrderDir()
            self.main_window.add_list_order()  # Обновляем какие заказы показываются

            self.button_confirm.destroy()

            self.label_warning.configure(text="")
            self.label.configure(text="Для лучшей работы приложения лучше произвести перезапуск")
            self.button_undo.configure(text="Ок")
            self.button_undo.place(relx=0.3, rely=0.75)

        else:
            self.label_warning.configure(text="Выбрана та же папка, что и раньше")

    def no(self):
        self.close_window()
