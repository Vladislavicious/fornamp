import logging

import tkinter
from os import path
from typing import Any, Callable, Tuple
from customtkinter import CTkButton
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage

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


class Button(Container):
    def __init__(self, parental_widget: Container, master: any, width: int = 140,
                 height: int = 28, corner_radius: int | None = None,
                 border_width: int | None = None, border_spacing: int = 2,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 hover_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 text_color: str | Tuple[str, str] | None = None,
                 text_color_disabled: str | Tuple[str, str] | None = None,
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
                 round_width_to_even_numbers: bool = True,
                 round_height_to_even_numbers: bool = True,
                 text: str = "CTkButton", font: tuple | CTkFont | None = None,
                 textvariable: tkinter.Variable | None = None,
                 image: CTkImage | Any | None = None, state: str = "normal",
                 hover: bool = True, command: Callable[[], None] | None = None,
                 compound: str = "left", anchor: str = "center", **kwargs):

        super().__init__(parental_widget)
        if self.initialize():
            self.item = CTkButton(master, width, height, corner_radius, border_width,
                                  border_spacing, bg_color, fg_color, hover_color,
                                  border_color, text_color, text_color_disabled,
                                  background_corner_colors, round_width_to_even_numbers,
                                  round_height_to_even_numbers, text, font, textvariable,
                                  image, state, hover, command, compound, anchor, **kwargs)
            self.name = "Кнопка " + text

            logger.debug(f"{self.name} инициализирована")

    def destroy(self) -> bool:
        if super().destroy():
            self.item.destroy()
            logger.debug(f"{self.name} уничтожена")
            return True
        return False

    def hide(self) -> bool:
        if super().hide():
            self.item.grid_remove()
            return True
        return False

    def show(self) -> bool:
        if super().show():
            self.item.grid()
            return True
        return False
