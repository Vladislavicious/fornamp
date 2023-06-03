import logging

from os import path
from typing import Tuple
from customtkinter import CTkLabel
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


class Label(Container):
    def __init__(self, parental_widget: Container, master: any, width: int = 0,
                 height: int = 28, corner_radius: int | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 text_color: str | Tuple[str, str] | None = None,
                 text: str = "CTkLabel", font: tuple | CTkFont | None = None,
                 image: CTkImage | None = None, compound: str = "center",
                 anchor: str = "center", wraplength: int = 0, **kwargs):

        super().__init__(parental_widget)
        if self.initialize():
            self.label = CTkLabel(master, width, height, corner_radius,
                                  bg_color, fg_color, text_color, text,
                                  font, image, compound, anchor, wraplength, **kwargs)
            self.name = "Метка " + text
            logger.debug(f"{self.name} инициализирована")

    def destroy(self) -> bool:
        if super().destroy():
            logger.debug(f"{self.name} уничтожена")
            self.label.destroy()
            return True
        return False

    def hide(self) -> bool:
        if super().hide():
            self.label.grid_remove()
            return True
        return False

    def show(self) -> bool:
        if super().show():
            self.label.grid()
            return True
        return False
