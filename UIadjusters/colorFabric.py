from dataclasses import dataclass


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


class ColorFabric():
    """Фабрика customTkinter шрифтов"""
    initialized = False

    @classmethod
    def initialize_base_settings(cls, undone="#B22222", done="#FFA500", vidan="#7FFF00",
                                 bg="transparent", fg=None, buttons=None,
                                 lines=None, font=None, lines_width=1):

        cls.color_setting = ColorSetting(undone=undone, done=done, vidan=vidan,
                                         bg=bg, fg=fg, buttons=buttons,
                                         lines=lines, font=font)
