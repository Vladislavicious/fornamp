"""Абстракция понятия frame в tkinter'е"""
import logging

from os import path
from customtkinter import CTkFrame
from UIadjusters.colorFabric import ColorFabric
from uiabs.container_tk import Container_tk

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


class Frame(Container_tk):
    def __init__(self, parental_widget: Container_tk, master: any,
                 width: int = 200, height: int = 200,
                 corner_radius: int | None = None,
                 border_width: int | None = None,
                 bg_color: str | None = None,
                 fg_color: str | None = None,
                 border_color: str | None = None,
                 overwrite_preferred_drawing_method: str | None = None, **kwargs):

        self.cf = ColorFabric()
        if border_width is None:
            border_width = self.cf.lines_width
        if fg_color is None:
            fg_color = self.cf.foreground
        if bg_color is None:
            bg_color = self.cf.background
        if border_color is None:
            border_color = self.cf.border_color

        super().__init__(parental_widget)
        self.name = "Frame в " + parental_widget.name

        self.item = CTkFrame(master, width, height, corner_radius,
                             border_width, bg_color, fg_color, border_color,
                             overwrite_preferred_drawing_method, **kwargs)
        logger.debug(f"{self.name} инициализирован")

    @property
    def width(self) -> int:
        return self.item.winfo_width()

    @property
    def height(self) -> int:
        return self.item.winfo_height()
