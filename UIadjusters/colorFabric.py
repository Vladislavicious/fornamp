from dataclasses import dataclass

from ioconnection.Singletone import Singleton


@dataclass
class ColorSetting:
    undone: str
    done: str
    vidan: str
    bg: str
    border_color: str | None
    fg: str | None
    buttons: str | None
    button_hover: str | None
    lines: str | None
    base_font: str | None
    error_font: str | None
    lines_width: int


class ColorFabric(metaclass=Singleton):
    @classmethod
    def from_color_setting(cls, cs: ColorSetting):
        return ColorFabric(undone=cs.undone, done=cs.done, vidan=cs.vidan,
                           border_color=cs.border_color, bg=cs.bg, fg=cs.fg,
                           buttons=cs.buttons, error_font=cs.error_font,
                           lines=cs.lines, font=cs.base_font,
                           lines_width=cs.lines_width, button_hover=cs.button_hover)

    def __init__(self, undone="#B22222", done="#FFA500", vidan="#7FFF00",
                 bg="transparent", border_color=None,
                 fg=None, buttons=None, button_hover=None, error_font=None,
                 lines=None, font=None, lines_width=1):
        self.__color_setting = ColorSetting(undone=undone, done=done, vidan=vidan, border_color=border_color,
                                            bg=bg, fg=fg, buttons=buttons, button_hover=button_hover,
                                            error_font=error_font,
                                            lines=lines, base_font=font, lines_width=lines_width)

    @property
    def undone(self) -> str:
        return self.__color_setting.undone

    @undone.setter
    def undone(self, stroka: str):
        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.undone = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123'")

    @property
    def done(self) -> str:
        return self.__color_setting.done

    @done.setter
    def done(self, stroka: str):
        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.done = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123'")

    @property
    def vidan(self) -> str:
        return self.__color_setting.vidan

    @vidan.setter
    def vidan(self, stroka: str):
        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.vidan = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123'")

    @property
    def background(self) -> str:
        return self.__color_setting.bg

    @background.setter
    def background(self, stroka: str):
        value = stroka.lower()
        if value.lower() == "transparent":
            self.__color_setting.bg = value
            return
        if self.__validate_color(value):
            self.__color_setting.bg = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123' или transparent")

    @property
    def border_color(self) -> str:
        return self.__color_setting.border_color

    @border_color.setter
    def border_color(self, stroka: str):
        if stroka is None:
            self.__color_setting = None
            return

        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.border_color = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123' или None")

    @property
    def foreground(self) -> str:
        return self.__color_setting.fg

    @foreground.setter
    def foreground(self, stroka: str | None):
        if stroka is None:
            self.__color_setting.fg = None
            return

        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.fg = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123' или None")

    @property
    def buttons(self) -> str:
        return self.__color_setting.buttons

    @buttons.setter
    def buttons(self, stroka: str | None):
        if stroka is None:
            self.__color_setting.buttons = None
            return

        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.buttons = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123' или None")

    @property
    def button_hover(self) -> str:
        return self.__color_setting.button_hover

    @button_hover.setter
    def button_hover(self, stroka: str | None):
        if stroka is None:
            self.__color_setting.button_hover = None
            return

        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.button_hover = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123' или None")

    @property
    def lines(self) -> str:
        return self.__color_setting.lines

    @lines.setter
    def lines(self, stroka: str | None):
        if stroka is None:
            self.__color_setting.lines = None
            return

        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.lines = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123' или None")

    @property
    def base_font(self) -> str:
        return self.__color_setting.base_font

    @base_font.setter
    def base_font(self, stroka: str | None):
        if stroka is None:
            self.__color_setting.base_font = None
            return

        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.base_font = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123' или None")

    @property
    def error_font(self) -> str:
        return self.__color_setting.error_font

    @error_font.setter
    def error_font(self, stroka: str | None):
        if stroka is None:
            self.__color_setting.error_font = None
            return

        value = stroka.lower()
        if self.__validate_color(value):
            self.__color_setting.error_font = value
            return
        raise ValueError("Цвет должен быть в формате '#AF0123' или None")

    @property
    def lines_width(self) -> int:
        return self.__color_setting.lines_width

    @lines_width.setter
    def lines_width(self, width: int):
        if width < 0:
            raise ValueError("Ширина не может быть отрицательной")
        self.__color_setting.lines_width = width

    def __validate_color(self, color: str) -> bool:
        stroka = color
        if stroka[0] != '#':
            return False

        valid_symb = set("1234567890abcdef")
        valid = True
        for symb in stroka[1:]:
            if symb not in valid_symb:
                valid = False
                break
        return valid

    # Добавить полей для цветов шрифта
