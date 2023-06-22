import logging

from os import path
from typing import Literal, Tuple
from customtkinter import CTkScrollableFrame
from customtkinter.windows.widgets.font import CTkFont

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


class Scroller(Container):
    def __init__(self, parental_widget: Container, master: any, width: int = 200,
                 height: int = 200, corner_radius: int | str | None = None,
                 border_width: int | str | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 scrollbar_fg_color: str | Tuple[str, str] | None = None,
                 scrollbar_button_color: str | Tuple[str, str] | None = None,
                 scrollbar_button_hover_color: str | Tuple[str, str] | None = None,
                 label_fg_color: str | Tuple[str, str] | None = None,
                 label_text_color: str | Tuple[str, str] | None = None,
                 label_text: str = "", label_font: tuple | CTkFont | None = None,
                 label_anchor: str = "center",
                 orientation: Literal['vertical', 'horizontal'] = "vertical"):

        super().__init__(parental_widget)
        self.name = f"Scroller в {parental_widget.name}"
        self.item = CTkScrollableFrame(master, width, height, corner_radius,
                                       border_width, bg_color, fg_color,
                                       border_color, scrollbar_fg_color,
                                       scrollbar_button_color, scrollbar_button_hover_color,
                                       label_fg_color, label_text_color, label_text,
                                       label_font, label_anchor, orientation)
        logger.debug(f"{self.name} инициализирован")

    def destroy(self) -> bool:
        if super().destroy():
            logger.debug(f"{self.name} уничтожен")
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
