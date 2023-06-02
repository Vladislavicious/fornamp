"""Абстракция на ctk"""
import logging
from os import path

from customtkinter import CTk, CTkButton

from uiabs.container import Container
from new_GUI.toplevel import MainWindow

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


class FornampWindow(CTk, Container):
    def __init__(self):
        CTk.__init__(self)
        Container.__init__(self, None)

        self.initialize()

    def initialize(self) -> bool:
        if Container.initialize(self):
            self.geometry("500x220+500+340")
            self.resizable(True, True)
            self.title("Fornamp")

            self.main_window = None

            self.grid_rowconfigure(0, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)

            self.button = CTkButton(master=self, text="Открыть Main",
                                    command=self.press, width=40, height=10)
            self.button.grid()
            self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
            self.show()
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
        logger.debug("press в baseWidow")
        if self.main_window is None:
            self.main_window = MainWindow(parental_widget=self)
        self.main_window.show()
        self.hide()

    def __new__(cls):
        """Не позволяет сделать более одного экземпляра класса"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(FornampWindow, cls).__new__(cls)
        return cls.instance
