import logging

import tkinter
from os import path
from typing import Any, Callable
from customtkinter import CTkButton
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.image import CTkImage
from UIadjusters.colorFabric import ColorFabric
from UIadjusters.fontFabric import FontFabric

from uiabs.container import Container
from uiabs.widget import Widget

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


class Button(Widget):
    def __init__(self, parental_widget: Container, master: any, width: int = 140,
                 height: int = 28, corner_radius: int | None = None,
                 border_width: int | None = None, border_spacing: int = 2,
                 bg_color: str | None = None,
                 fg_color: str | None = None,
                 hover_color: str | None = None,
                 border_color: str | None = None,
                 text_color: str | None = None,
                 text: str = "CTkButton", font: CTkFont | None = None,
                 textvariable: tkinter.Variable | None = None,
                 image: CTkImage | Any | None = None, state: str = "normal",
                 hover: bool = True, command: Callable[[], None] | None = None,
                 compound: str = "left", anchor: str = "center", **kwargs):

        self.cf = ColorFabric()
        if fg_color is None:
            fg_color = self.cf.foreground
        if bg_color is None:
            bg_color = self.cf.background
        if border_width is None:
            border_width = self.cf.lines_width
        if border_color is None:
            border_color = self.cf.border_color
        if text_color is None:
            text_color = self.cf.base_font
        if hover_color is None:
            hover_color = self.cf.button_hover

        super().__init__(parental_widget)
        if self.initialize():
            self.ff = FontFabric()
            self.font = font
            if font is None:
                self.font = self.ff.get_base_font()

            self.item = CTkButton(master=master, width=width, height=height, corner_radius=corner_radius,
                                  border_width=border_width, border_spacing=border_spacing,
                                  bg_color=bg_color, fg_color=fg_color, hover_color=hover_color,
                                  border_color=border_color, text_color=text_color,
                                  text=text, font=self.font, textvariable=textvariable,
                                  image=image, state=state, hover=hover, command=command,
                                  compound=compound, anchor=anchor, **kwargs)
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
