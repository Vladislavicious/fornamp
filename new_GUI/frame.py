"""Абстракция понятия frame в tkinter'е"""
from typing import List, Tuple
from customtkinter import CTkFrame

from uiabs.container import Container


class Frame(CTkFrame, Container):
    def __init__(self, parental_widget: any, width: int = 200, height: int = 200,
                 corner_radius: int | str | None = None, border_width: int | str | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
                 overwrite_preferred_drawing_method: str | None = None,
                 widgets: List[Container] = list(), **kwargs):

        CTkFrame.__init__(self, parental_widget, width, height, corner_radius,
                          border_width, bg_color, fg_color, border_color,
                          background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        Container.__init__(self, parental_widget, widgets)
