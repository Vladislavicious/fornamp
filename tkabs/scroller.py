import logging

from os import path
from customtkinter import CTkScrollableFrame
from UIadjusters.colorFabric import ColorFabric

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
                 border_width: int | None = None,
                 bg_color: str | None = None,
                 fg_color: str | None = None,
                 border_color: str | None = None,
                 scrollbar_fg_color: str | None = None,
                 scrollbar_button_color: str | None = None,
                 scrollbar_button_hover_color: str | None = None):

        self.cf = ColorFabric()
        if border_width is None:
            border_width = self.cf.lines_width
        if fg_color is None:
            fg_color = self.cf.foreground
        if bg_color is None:
            bg_color = self.cf.background
        if border_color is None:
            border_color = self.cf.border_color

        super().__init__(parental_widget)
        self.name = f"Scroller в {parental_widget.name}"
        self.item = CTkScrollableFrame(master, width, height, corner_radius,
                                       border_width, bg_color, fg_color,
                                       border_color, scrollbar_fg_color,
                                       scrollbar_button_color, scrollbar_button_hover_color)
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
