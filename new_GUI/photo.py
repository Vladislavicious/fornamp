import logging

from os import path
from typing import Tuple
from UIadjusters.fontFabric import FontFabric

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


class Photo(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 photopath: str,
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
        self.photopath = photopath
        self.base_font = FontFabric.get_base_font()
        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():

            self.frame.grid_rowconfigure(1, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)

            _, _, name = self.photopath.rpartition("\\")

            self.label = Label(parental_widget=self, master=self.frame,
                               text=name, font=self.base_font)
            self.label.label.grid(row=0, column=0, pady=2, sticky="nsew")
            self.add_widget(self.label)

            return True
        return False


"""
Класс фотографии. По умолчанию является рамкой с Лэйблом и канвасом, на канвасе фото.
при нажатии на фото открывается увеличенная версия фото с крестиком в правом верхнем углу
"""
