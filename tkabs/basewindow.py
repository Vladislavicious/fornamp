"""Абстракция на ctk"""
import logging
import tkinter as tk
from os import path
from typing import Tuple


from customtkinter import CTk
from ioconnection.App import Singleton
from tkabs.button import Button
from tkabs.dialog import Dialog
from uiabs.container import Container
from new_GUI.mWindow import MainWindow

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# настройка обработчика и форматировщика для logger
handler = logging.FileHandler(path.abspath(path.curdir)+f"\\logs\\{__name__}.log", mode='w', encoding="utf-8")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)

logger.info(f"Testing the custom logger for module {__name__}...")


def validate_string(string: str = "") -> Tuple[bool, str]:
    """Проверяет строку на соответствие параметрам"""
    if len(string) < 20:
        return False, "Строка слишком короткая"
    if not string.isidentifier():
        return False, "Содержит неподобающие символы"
    return True, ""


class FornampWindow(CTk, Container, metaclass=Singleton):
    def __init__(self):
        CTk.__init__(self)
        Container.__init__(self, None)
        self.name = "FornampWindow"
        self.initialize()

    def initialize(self) -> bool:
        if Container.initialize(self):
            logger.debug(f"Инициализирую {self.name}")
            self.geometry("500x220+500+340")
            self.resizable(True, True)
            self.title("Fornamp")

            self.dialog = Dialog(parental_widget=self, master=self)
            self.dialog.show()
            self.main_window = None
            for i in range(2):
                self.grid_rowconfigure(i, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)
            self.grid_propagate(True)

            self.main_open_button = Button(parental_widget=self, master=self, text="Открыть Main",
                                           command=self.press, width=40, height=10)
            self.main_open_button.item.grid(row=1, column=0, ipadx=6, ipady=6, padx=4, pady=4, sticky=tk.NSEW)
            self.add_widget(self.main_open_button)

            self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
            self.update()
            self.update_idletasks()
            self.show()

            self.dialog.hide()
            return True
        return False

    def show(self) -> bool:
        if Container.show(self):
            self.deiconify()
            return True
        return False

    def hide(self) -> bool:
        if Container.hide(self):
            self.withdraw()
            return True
        return False

    def destroy(self):
        if Container.destroy(self):
            CTk.destroy(self)
            logger.debug("Закрываю Fornamp")
            return True
        return False

    def press(self):
        logger.debug(f"press в {self.name}")
        if self.main_window is None:
            self.main_window = MainWindow(parental_widget=self, master=self)
        self.main_window.show()
        self.hide()

    def __new__(cls):
        """Не позволяет сделать более одного экземпляра класса"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(FornampWindow, cls).__new__(cls)
        return cls.instance
