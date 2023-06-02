"""Абстракция понятия toplevel в tkinter'е"""
import logging

from os import path
from typing import Tuple
from customtkinter import CTkToplevel

from new_GUI.button import Button
from uiabs.container import Container


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


class TopLevel(CTkToplevel, Container):
    def __init__(self, *args, parental_widget,
                 fg_color: str | Tuple[str, str] | None = None, **kwargs):
        CTkToplevel.__init__(self, *args, parental_widget, fg_color=fg_color, **kwargs)
        Container.__init__(self, parental_widget)

    def hide(self):
        if Container.hide(self):
            self.withdraw()
            return True
        return False

    def show(self) -> bool:
        if Container.show(self):
            self.deiconify()
            return True
        return False

    def destroy(self) -> bool:
        logger.debug("Закрываю топлевел")
        if Container.destroy(self):
            CTkToplevel.destroy(self)
            if self.parental_widget is not None:
                self.parental_widget.show()
            return True
        return False

    def initialize(self) -> bool:
        if Container.initialize(self):
            self.grid_rowconfigure(0, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)

            self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
            return True
        return False


class MainWindow(TopLevel):
    def __init__(self, *args, parental_widget,
                 fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, parental_widget=parental_widget,
                         fg_color=fg_color, **kwargs)
        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            self.title("Main window")
            self.geometry("1000x600+250+100")
            self.resizable(True, True)

            self.base_open_button = Button(parental_widget=self, master=self, text="Открыть Base",
                                           command=self.press, width=40, height=10)
            self.addWidget(self.base_open_button)

            self.show()
            return True
        return False

    def press(self):
        logger.debug("нажатие в mainWindow")
        self.parental_widget.show()
        self.hide()

    def destroy(self) -> bool:
        if super().destroy():
            self.parental_widget.main_window = None
            return True
        return False
