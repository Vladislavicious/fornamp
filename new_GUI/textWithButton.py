import logging

from os import path
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
                 border_width: int | None = None,
                 bg_color: str | None = None,
                 fg_color: str | None = None,
                 border_color: str | None = None, **kwargs):

        super().__init__(parental_widget, master, width,
                         height, border_width, bg_color,
                         fg_color, border_color, **kwargs)
        self.text = text
        self.button_function = button_function
        self.button_text = button_text
        self.ff = FontFabric.get_instance()
        self.font = self.ff.get_base_font()
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
                               text=self.text, font=self.font)
            self.label.item.grid(row=0, column=0, pady=2, padx=1, sticky="nsew")
            self.add_widget(self.label)

            self.button = Button(parental_widget=self, master=self.item,
                                 text=self.button_text, font=self.font,
                                 width=60)
            if self.button_function is not None:
                self.change_button_function(self.button_function)
            self.button.item.grid(row=0, column=1, pady=2, sticky="e")
            self.add_widget(self.button)

            return True
        return False
