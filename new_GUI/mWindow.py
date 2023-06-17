import logging

from os import path
from typing import Tuple
from ioconnection.App import App
from new_GUI.additionFrame import additionFrame
from new_GUI.mainFrame import mainFrame
from new_GUI.menu import Menu
from tkabs.toplevel import TopLevel

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


class MainWindow(TopLevel):
    def __init__(self, *args, parental_widget,
                 fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, parental_widget=parental_widget,
                         fg_color=fg_color, **kwargs)
        self.name = "MainWindow"
        self.app = App()
        self.current_order = None
        self.menu_opened = False
        self.current_window = None
        self.current_menu_holder = None

        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            logger.debug(f"Инициализирую {self.name}")
            self.title("Fornamp")
            self.geometry("1000x600+250+100")
            self.resizable(True, True)
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            self.mainFrame = mainFrame(parental_widget=self, master=self,
                                       border_width=0)
            self.mainFrame.frame.grid(row=0, column=0, sticky="nsew")

            self.additionFrame = additionFrame(parental_widget=self, master=self, border_width=0,
                                               go_to_main_function=lambda window=self.mainFrame:
                                               self.open_window(window))
            self.additionFrame.frame.grid(row=0, column=0, sticky="nsew")
            self.additionFrame.frame.grid_remove()

            self.menu = Menu(parental_widget=self.mainFrame, master=self.mainFrame.frame,
                             open_menu_function=self.mainFrame.open_menu,
                             close_menu_function=self.mainFrame.close_menu,
                             menu_options={"Добавить заказ":
                                           lambda window=self.additionFrame: self.open_window(window)})
            self.current_window = self.mainFrame

            self.change_menu_holder(self.mainFrame)

            self.add_widget(self.mainFrame)
            self.show()
            return True
        return False

    def change_menu_holder(self, holder):
        if holder != self.current_menu_holder:
            if self.current_menu_holder is not None:
                self.current_menu_holder.remove_widget(self.menu)

            holder.insert_menu(self.menu)
            holder.add_widget(self.menu)
            self.current_menu_holder = holder

    def open_window(self, window):
        if self.current_window != window:
            # self.current_window.remove_widget(self.menu)
            # # В дальнейшем будет необходима проверка
            self.current_menu_holder.close_menu()
            self.current_window.hide()
            window.show()
            self.current_window = window
