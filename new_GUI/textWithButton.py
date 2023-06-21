import logging

from os import path
from typing import Tuple
from types import FunctionType
from UIadjusters.fontFabric import FontFabric
from tkabs.button import Button

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


class TextWithButton(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 text: str, button_function: FunctionType = None,
                 button_text: str = "Удалить",
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
        self.text = text
        self.button_function = button_function
        self.button_text = button_text
        self.base_font = FontFabric.get_base_font()
        self.initialize()

    @property
    def contained_text(self) -> str:
        return self.label.contained_text

    def change_button_function(self, function: FunctionType):
        self.button_function = function
        self.button.item.configure(command=function)

    def initialize(self) -> bool:
        if super().initialize():
            self.item.grid_columnconfigure(0, weight=1)
            self.item.grid_rowconfigure(0, weight=1)

            self.label = Label(parental_widget=self, master=self.item,
                               text=self.text, font=self.base_font)
            self.label.item.grid(row=0, column=0, pady=2, padx=1, sticky="nsew")
            self.add_widget(self.label)

            self.button = Button(parental_widget=self, master=self.item,
                                 text=self.button_text, font=self.base_font,
                                 width=100)
            if self.button_function is not None:
                self.change_button_function(self.button_function)
            self.button.item.grid(row=0, column=1, pady=2, sticky="e")
            self.add_widget(self.button)

            return True
        return False

    def destroy(self) -> bool:
        if super().destroy():
            self.label.item.destroy()
            self.button.item.destroy()
            self.item.destroy()
            return True
        return False
