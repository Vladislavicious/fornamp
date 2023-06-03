import logging

from os import path
from typing import Tuple

from new_GUI.frame import Frame
from new_GUI.scroller import Scroller
from new_GUI.toplevel import TopLevel
from new_GUI.button import Button

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


class MainWindow(TopLevel):
    def __init__(self, *args, parental_widget,
                 fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, parental_widget=parental_widget,
                         fg_color=fg_color, **kwargs)
        self.name = "MainWindow"
        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            logger.debug(f"Инициализирую {self.name}")
            self.title("Main Window")
            self.geometry("1000x600+250+100")
            self.resizable(True, True)

            self.grid_rowconfigure(0, weight=1)  # configure grid system
            for i in range(2):
                self.grid_columnconfigure(i, weight=1)

            self.first_frame = Frame(parental_widget=self, master=self,
                                     border_width=1, bg_color="#FF0000")

            self.first_frame.frame.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

            self.scroller = Scroller(parental_widget=self, master=self,
                                     border_width=1, bg_color="#2E8B57")

            self.scroller.scroller.grid(row=0, column=1, padx=4, pady=4, sticky="nsew")

            self.base_open_button = Button(parental_widget=self.first_frame, master=self.first_frame.frame,
                                           text="Открыть Base", command=self.press, width=40, height=10)

            self.base_open_button.button.grid(row=0, column=0, padx=24, pady=24)

            self.first_frame.addWidget(self.base_open_button)

            self.addWidget(self.first_frame)
            self.addWidget(self.scroller)

            self.show()
            return True
        return False

    def press(self):
        logger.debug(f"нажатие в {self.name}")
        self.parental_widget.show()
        self.hide()

    def destroy(self) -> bool:
        if super().destroy():
            logger.debug(f"Закрываю {self.name}")
            self.parental_widget.main_window = None
            return True
        return False
