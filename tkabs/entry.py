import tkinter
from typing import Tuple
from customtkinter import CTkEntry
from customtkinter.windows.widgets.font import CTkFont

from uiabs.container import Container


class Entry(Container):
    def __init__(self, parental_widget: Container, master: any,
                 width: int = 140, height: int = 28,
                 corner_radius: int | None = None,
                 border_width: int | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 text_color: str | Tuple[str, str] | None = None,
                 placeholder_text_color: str | Tuple[str, str] | None = None,
                 textvariable: tkinter.Variable | None = None,
                 placeholder_text: str | None = None,
                 font: tuple | CTkFont | None = None,
                 state: str = tkinter.NORMAL, **kwargs):

        super().__init__(parental_widget)
        if self.initialize():
            self.item = CTkEntry(master, width, height, corner_radius,
                                 border_width, bg_color, fg_color, border_color,
                                 text_color, placeholder_text_color, textvariable,
                                 placeholder_text, font, state, **kwargs)
            self.name = "Entry " + placeholder_text

    @property
    def contained_text(self) -> str:
        return self.item.get()

    def destroy(self) -> bool:
        if super().destroy():
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

    def place_text(self, string: str):
        text = self.contained_text
        length = len(text)
        if string != text:
            self.item.delete(0, length)
            self.item.insert(0, string)
