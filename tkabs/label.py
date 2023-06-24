import logging

from os import path
from textwrap import wrap
from customtkinter import CTkLabel, CTkFont

from customtkinter.windows.widgets.image import CTkImage
from UIadjusters.colorFabric import ColorFabric
from UIadjusters.fontFabric import FontFabric
from uiabs.Container_tk import Container_tk
from uiabs.widget_tk import Widget_tk

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


class Label(Widget_tk):
    def __init__(self, parental_widget: Container_tk, master: any, width: int = 0,
                 height: int = 28, corner_radius: int | None = None,
                 bg_color: str | None = None,
                 fg_color: str | None = None,
                 text_color: str | None = None,
                 text: str = "Метка", font: CTkFont = None,
                 image: CTkImage | None = None, compound: str = "center",
                 anchor: str = "center", wraplength: int = 0, **kwargs):

        self.cf = ColorFabric()
        if fg_color is None:
            fg_color = self.cf.foreground
        if bg_color is None:
            bg_color = self.cf.background
        if text_color is None:
            text_color = self.cf.base_font

        logger.debug(f"initial width: {width}")
        super().__init__(parental_widget)
        if self.initialize():
            self.ff = FontFabric.get_instance()
            self.font = font
            if font is None:
                self.font = self.ff.get_base_font()
            self.item = CTkLabel(master, width, height, corner_radius,
                                 bg_color, fg_color, text_color, text,
                                 self.font, image, compound, anchor, wraplength, **kwargs)
            self.name = "Метка " + text
            logger.debug(f"{self.name} инициализирована")

    def change_text(self, text: str):
        self.item.configure(text=text)

    @property
    def contained_text(self) -> str:
        text = self.item.cget("text")
        return text.replace("\n", "")

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
            mean_width = self.ff.calculate_mean_width(self.font)
            if label_width > text_length * mean_width:
                return False

            new_string_length = label_width // mean_width - 5

            wrapped_text = '\n'.join(wrap(text, new_string_length,
                                          replace_whitespace=False, drop_whitespace=False))
            self.item.configure(text=wrapped_text)
            return True
        return False
