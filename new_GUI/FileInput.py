import logging

from os import path
from typing import List, Tuple
from tkinter import filedialog as fd
from UIadjusters.fontFabric import FontFabric
from new_GUI.textWithButton import TextWithButton
from tkabs.button import Button

from tkabs.frame import Frame
from tkabs.label import Label
from tkabs.scroller import Scroller
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


class FileInput(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 purpose_name: str,
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
        self.purpose_name = purpose_name
        self.base_font = FontFabric.get_base_font()
        self.initialize()

    @property
    def contained_paths(self) -> List[str]:
        return list(pathway.contained_text for pathway in self.scroller.widgets)

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_columnconfigure(1, weight=1)
            self.frame.grid_rowconfigure(0, weight=0)
            self.frame.grid_rowconfigure(1, weight=0)
            self.frame.grid_rowconfigure(2, weight=1)

            self.label = Label(parental_widget=self, master=self.frame,
                               text=self.purpose_name, font=self.base_font)
            self.label.label.grid(row=0, column=0, columnspan=2, pady=2, padx=1, sticky="nsew")
            self.add_widget(self.label)

            self.add_button = Button(parental_widget=self, master=self.frame,
                                     text="Добавить", font=self.base_font,
                                     command=self.add_path)
            self.add_button.button.grid(row=1, column=1, pady=2, padx=1, sticky="e")
            self.add_widget(self.add_button)

            self.clear_button = Button(parental_widget=self, master=self.frame,
                                       text="Очистить", font=self.base_font,
                                       command=self.clear_paths)
            self.clear_button.button.grid(row=1, column=0, pady=2, padx=1, sticky="w")
            self.add_widget(self.clear_button)

            self.scroller = Scroller(parental_widget=self, master=self.frame)
            self.scroller.scroller.grid(row=2, column=0, columnspan=2, sticky="nsew")
            self.scroller.scroller.grid_columnconfigure(index=0, weight=1)
            self.add_widget(self.scroller)

            return True
        return False

    def __select_files(self) -> List[str]:
        filetypes = (
            ('PNG Image', '*.png'),
            ('JPEG Image', ['*.jpeg*', '*.jpg*']),
            ('BMP Image', '*.bmp'),
            ('TIFF Image', '*.tiff'),
            ('Any Images', ['*.png', '*.jpeg*', '*.jpg*', '*.bmp', '*.tiff'])
        )

        filenames = fd.askopenfilenames(
            title=self.purpose_name,
            initialdir='/Desktop',
            filetypes=filetypes)

        return filenames

    def add_path(self):
        filenames = self.__select_files()
        if len(filenames) != 0:
            for filename in filenames:
                pathway = TextWithButton(self.scroller, self.scroller.scroller,
                                         text=filename, button_text="Удалить")
                pathway.frame.grid(padx=2, pady=2, sticky="ew")
                self.scroller.add_widget(pathway)
                pathway.change_button_function(lambda: self.scroller.delete_widget(pathway))

    def clear_paths(self):
        for pathway in self.scroller.widgets:
            pathway.destroy()
        self.scroller.clear_widgets()
