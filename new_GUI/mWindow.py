import logging

from os import path
from typing import Tuple
from BaH.App import App
from new_GUI.ordField import OrderField

from tkabs.frame import Frame
from tkabs.label import Label
from tkabs.scroller import Scroller
from tkabs.toplevel import TopLevel
from tkabs.button import Button

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
        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            logger.debug(f"Инициализирую {self.name}")
            self.title("Main Window")
            self.geometry("1000x600+250+100")
            self.resizable(True, True)
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=3)

            self.first_frame = Frame(parental_widget=self, master=self,
                                     border_width=1, bg_color="#FF0000")

            self.first_frame.frame.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

            self.base_open_button = Button(parental_widget=self.first_frame, master=self.first_frame.frame,
                                           text="Открыть Base", command=self.press, width=40, height=10)

            self.base_open_button.button.grid(row=0, column=0, padx=24, pady=24)

            self.first_frame.add_widget(self.base_open_button)

            # Настройка правого фрейма
            self.second_frame = Frame(parental_widget=self, master=self,
                                      border_width=1, bg_color="#2E8B57")

            self.second_frame.frame.grid(row=0, column=1, padx=4, sticky="nsew")
            self.second_frame.frame.grid_columnconfigure(0, weight=1)
            self.second_frame.frame.grid_rowconfigure(0, weight=1)
            self.second_frame.frame.grid_rowconfigure(1, weight=9)

            self.title = Frame(parental_widget=self.second_frame, master=self.second_frame.frame,
                               border_width=1, bg_color="#1E8B57")
            self.title.frame.grid(row=0, column=0, pady=4, sticky="nsew")

            self.title_label = Label(parental_widget=self.title, master=self.title.frame,
                                     text="Заказы")
            self.title_label.label.grid(row=0, column=0, pady=4, sticky="e")
            self.title.add_widget(self.title_label)

            self.second_frame.add_widget(self.title)

            self.scroller = Scroller(parental_widget=self.second_frame, master=self.second_frame.frame,
                                     border_width=1, bg_color="#2E8B57")
            self.scroller.scroller.grid_columnconfigure(0, weight=1)

            self.scroller.scroller.grid(row=1, column=0, pady=4, sticky="nsew")

            self.second_frame.add_widget(self.scroller)

            self.__parse_order_previews()
            ###
            self.add_widget(self.first_frame)
            self.add_widget(self.second_frame)

            self.show()
            return True
        return False

    def press(self):
        logger.debug(f"нажатие в {self.name}")
        self.parental_widget.show()
        self.hide()

    def destroy(self) -> bool:
        if super().destroy():
            logger.debug(f"Закрываю {self.name}")
            self.parental_widget.main_window = None
            return True
        return False

    def __parse_order_previews(self):
        logger.debug("Выводим заказы")
        if self.scroller.items_count == 0:
            for order_preview in self.app.order_previews:
                order_field = OrderField(self.scroller, self.scroller.scroller,
                                         order_preview=order_preview)
                self.scroller.add_widget(order_field)

                order_field.frame.grid(sticky="nsew", pady=2)
                order_field.frame.bind('<Button-1>', lambda event, ID=order_preview.id: self.open_info(ID))

    def open_info(self, id: int):
        logger.debug(f"Нажатие по заказу {id}")
