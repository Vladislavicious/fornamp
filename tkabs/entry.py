import tkinter
from customtkinter import CTkEntry
from customtkinter.windows.widgets.font import CTkFont
from UIadjusters.colorFabric import ColorFabric
from UIadjusters.fontFabric import FontFabric
from uiabs.Container_tk import Container_tk

from uiabs.widget_tk import Widget_tk


class Entry(Widget_tk):
    def __init__(self, parental_widget: Container_tk, master: any,
                 width: int = 140, height: int = 28,
                 corner_radius: int | None = None,
                 border_width: int | None = None,
                 bg_color: str | None = None,
                 fg_color: str | None = None,
                 border_color: str | None = None,
                 text_color: str | None = None,
                 placeholder_text_color: str | None = None,
                 textvariable: tkinter.Variable | None = None,
                 placeholder_text: str | None = None,
                 font: CTkFont = None,
                 state: str = tkinter.NORMAL, **kwargs):

        self.cf = ColorFabric()
        if border_width is None:
            border_width = self.cf.lines_width
        if fg_color is None:
            fg_color = self.cf.foreground
        if bg_color is None:
            bg_color = self.cf.background
        if text_color is None:
            text_color = self.cf.base_font
        if border_color is None:
            border_color = self.cf.border_color
        if placeholder_text_color is None:
            placeholder_text_color = self.cf.error_font

        super().__init__(parental_widget)
        if self.initialize():
            self.ff = FontFabric.get_instance()
            self.font = font
            if font is None:
                self.font = self.ff.get_base_font()
            self.item = CTkEntry(master, width, height, corner_radius,
                                 border_width, bg_color, fg_color, border_color,
                                 text_color, placeholder_text_color, textvariable,
                                 placeholder_text, self.font, state, **kwargs)
            self.name = "Entry " + placeholder_text

    @property
    def contained_text(self) -> str:
        return self.item.get()

    def place_text(self, string: str):
        text = self.contained_text
        length = len(text)
        if string != text:
            self.item.delete(0, length)
            self.item.insert(0, string)
