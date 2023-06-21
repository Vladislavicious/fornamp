import logging

from os import path
from typing import Tuple
from textwrap import wrap
from customtkinter import CTkLabel, CTkFont

from customtkinter.windows.widgets.image import CTkImage
from UIadjusters.fontFabric import FontFabric
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
                 text: str = "Метка", font: tuple | CTkFont | None = None,
                 image: CTkImage | None = None, compound: str = "center",
                 anchor: str = "center", wraplength: int = 0, **kwargs):

        logger.debug(f"initial width: {width}")
        super().__init__(parental_widget)
        if self.initialize():
            self.font = font
            self.item = CTkLabel(master, width, height, corner_radius,
                                 bg_color, fg_color, text_color, text,
                                 font, image, compound, anchor, wraplength, **kwargs)
            self.name = "Метка " + text
            logger.debug(f"{self.name} инициализирована")

    def change_text(self, text: str):
        self.item.configure(text=text)

    @property
    def contained_text(self) -> str:
        text = self.item.cget("text")
        return text.replace("\n", "")

    def destroy(self) -> bool:
        if super().destroy():
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
            text = self.item.cget("text")
            text_length = len(text)
            if text_length > 25:
                self.item.update()

            self.__check_text_length()

            self.item.grid()

            logger.debug(f"second width: {self.item.winfo_width()}")
            return True
        return False

    def __check_text_length(self):
        """Если длина строки больше, чем ей выделено места,
           делает переносы строки"""
        text = self.item.cget("text")
        text_length = len(text)
        if text_length <= 25:
            return False

        label_width = self.item.winfo_width()
        if label_width > 1:
            mean_width = FontFabric.calculate_mean_width(self.font)
            if label_width > text_length * mean_width:
                return False

            new_string_length = label_width // mean_width - 5

            wrapped_text = '\n'.join(wrap(text, new_string_length,
                                          replace_whitespace=False, drop_whitespace=False))
            self.item.configure(text=wrapped_text)
            return True
        return False
