from dataclasses import dataclass

from ioconnection.App import Singleton


@dataclass
class ColorSetting:
    undone: str
    done: str
    vidan: str
    bg: str
    fg: str | None
    buttons: str | None
    lines: str | None
    font: str | None

    lines_width: int


class ColorFabric(metaclass=Singleton):

    def __init__(self, undone="#B22222", done="#FFA500", vidan="#7FFF00",
                 bg="transparent", fg=None, buttons=None,
                 lines=None, font=None, lines_width=1):
        self.color_setting = ColorSetting(undone=undone, done=done, vidan=vidan,
                                          bg=bg, fg=fg, buttons=buttons,
                                          lines=lines, font=font, lines_width=lines_width)

    # Сделать геттеры и сеттеры для всех полей

    # Добавить полей для цветов шрифта
