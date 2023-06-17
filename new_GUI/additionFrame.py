import logging

from os import path
from typing import List, Tuple
from BaH.order import OrderPreview
from new_GUI.menu import Menu
from new_GUI.prodField import ProductField
from UIadjusters.fontFabric import FontFabric
from ioconnection.App import App
from new_GUI.ordPreviewField import OrderPreviewField
from new_GUI.orderField import OrderField
from tkabs.scroller import Scroller
from tkabs.button import Button

from tkabs.frame import Frame
from tkabs.label import Label
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


class additionFrame(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 go_to_main_function,
                 width: int = 200, height: int = 200,
                 corner_radius: int | str | None = None,
                 border_width: int | str | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
                 overwrite_preferred_drawing_method: str | None = None, **kwargs):

        super().__init__(parental_widget, master, width,
                         height, corner_radius, border_width,
                         bg_color, fg_color, border_color,
                         background_corner_colors,
                         overwrite_preferred_drawing_method, **kwargs)
        self.back_function = go_to_main_function
        self.base_font = FontFabric.get_base_font()
        self.app = App()
        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_rowconfigure(0, weight=0)
            self.frame.grid_rowconfigure(1, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_columnconfigure(1, weight=3)
            self.frame.grid_columnconfigure(2, weight=3)

            self.label = Label(self, self.frame, text="Абоба",
                               font=self.base_font)
            self.label.label.grid(row=0, column=0, sticky="ew")
            self.add_widget(self.label)
            self.label.label.bind('<Button-1>', command=lambda event: self.back_function())

            self.order_frame = Frame(parental_widget=self, master=self.frame,
                                     border_width=2)
            self.order_frame.frame.grid(row=1, column=0, sticky="nsew")
            self.add_widget(self.order_frame)

            self.product_frame = Frame(parental_widget=self, master=self.frame,
                                       border_width=2)
            self.product_frame.frame.grid(row=1, column=1, sticky="nsew")
            self.add_widget(self.product_frame)

            self.step_frame = Frame(parental_widget=self, master=self.frame,
                                    border_width=2)
            self.step_frame.frame.grid(row=1, column=2, sticky="nsew")
            self.add_widget(self.step_frame)

            return True
        return False

    """
    2 ряда, 2 колонны разделены 1 к 3, слева сверху будет меню, справа сверху свободное место под что-нибудь.
    """
