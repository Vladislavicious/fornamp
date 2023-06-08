"""Абстракция понятия frame в tkinter'е"""
import logging

from os import path
from typing import Tuple
from customtkinter import CTkFrame

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


class Frame(Container):
    def __init__(self, parental_widget: Container, master: any,
                 width: int = 200, height: int = 200,
                 corner_radius: int | str | None = None,
                 border_width: int | str | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
                 overwrite_preferred_drawing_method: str | None = None, **kwargs):

        super().__init__(parental_widget)
        self.name = "Frame в " + parental_widget.name

        self.frame = CTkFrame(master, width, height, corner_radius,
                              border_width, bg_color, fg_color, border_color,
                              background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        logger.debug(f"{self.name} инициализирован")

    def destroy(self) -> bool:
        if super().destroy():
            logger.debug(f"{self.name} уничтожен")
            return True
        return False

    def hide(self) -> bool:
        if super().hide():
            self.frame.grid_remove()
            return True
        return False

    def show(self) -> bool:
        if super().show():
            self.frame.grid()
            return True
        return False
