import logging

from os import path
from typing import Dict, Tuple
from types import FunctionType
from UIadjusters.fontFabric import FontFabric
from ioconnection.App import App

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


class MenuItem(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 item_name: str, item_function, font,
                 width: int = 50, height: int = 25,
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

        self.__item_name = item_name
        self.function = item_function
        self.base_font = font
        self.initialize()

    @property
    def item_name(self) -> str:
        return self.__item_name

    @item_name.setter
    def item_name(self, value: str):
        self.__item_name = value
        self.name_label.change_text(value)

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_columnconfigure(0, weight=1)

            self.name_label = Label(parental_widget=self, master=self.frame,
                                    text=self.item_name, font=self.base_font)
            self.name_label.label.grid(row=0, column=0, sticky="ew")
            self.add_widget(self.name_label)

            self.frame.configure(cursor="hand2")
            self.frame.bind('<Button-1>', command=self.function)
            self.name_label.label.configure(cursor="hand2")
            self.name_label.label.bind('<Button-1>', command=lambda event: self.function())


class Menu(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 open_menu_function, menu_options: Dict[str, FunctionType] = dict(),
                 width: int = 50, height: int = 25,
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

        self.__menu_opened = False
        self.base_font = FontFabric.get_changed_font(size=20, weight='bold')
        self.app = App()
        self.option_dict = menu_options
        self.menu_items = list()
        self.open_menu_function = open_menu_function
        self.initialize()

    @property
    def menu_opened(self) -> bool:
        return self.__menu_opened

    @menu_opened.setter
    def menu_opened(self, value: bool):
        self.__menu_opened = value

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_columnconfigure(0, weight=1)

            self.open_menu = MenuItem(parental_widget=self, master=self.frame,
                                      item_name="Menu", item_function=self.press,
                                      font=self.base_font)
            self.open_menu.frame.grid(row=0, column=0, pady=2, sticky="ew")
            self.add_widget(self.open_menu)

            for option_name in self.option_dict.keys():
                function = self.option_dict[option_name]

                menu_item = MenuItem(parental_widget=self, master=self.frame,
                                     item_name=option_name, item_function=function,
                                     font=self.base_font)
                menu_item.frame.grid(pady=2, sticky="ew")
                self.add_widget(menu_item)
                self.menu_items.append(menu_item)

    def press(self):
        logger.debug(f"нажатие в {self.name}")

        self.open_menu_function()
        if self.menu_opened is False:
            self.open_menu.item_name = "Return"
            self.unfold()
            self.menu_opened = True
        else:
            self.menu_opened = False
            self.fold()
            self.open_menu.item_name = "Menu"

    def show(self) -> bool:
        if super().show():
            if self.menu_opened:
                self.unfold()
            else:
                self.fold()
            return True
        return False

    def unfold(self):
        for item in self.menu_items:
            item.show()

    def fold(self):
        for item in self.menu_items:
            item.hide()
