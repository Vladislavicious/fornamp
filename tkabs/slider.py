from tkinter import Variable
from typing import Callable
from customtkinter import CTkSlider
from UIadjusters.colorFabric import ColorFabric

from uiabs.container import Container
from uiabs.editable import Editable
from uiabs.widget_tk import Widget_tk
from uiabs.widget import Widget


class Slider(Widget_tk, Editable):
    def __init__(self, parental_widget: Container, master: any, width: int | None = 200,
                 height: int | None = 30, corner_radius: int | None = None,
                 bg_color: str | None = None,
                 fg_color: str | None = None,
                 border_color: str | None = None,
                 progress_color: str | None = None,
                 button_color: str | None = None,
                 button_hover_color: str | None = None,
                 from_: int = 0, to: int = 1, state: str = "normal",
                 number_of_steps: int | None = None, hover: bool = True,
                 command: Callable[[float], None] | None = None,
                 variable: Variable | None = None, orientation: str = "horizontal", **kwargs):

        self.cf = ColorFabric()
        if fg_color is None:
            fg_color = self.cf.foreground
        if bg_color is None:
            bg_color = self.cf.background
        if border_color is None:
            border_color = self.cf.border_color
            if border_color is None:   # специально для слайдера
                border_color = "transparent"
        if button_color is None:
            button_color = self.cf.buttons
        if button_hover_color is None:
            button_hover_color = self.cf.button_hover

        Widget.__init__(self, parental_widget=parental_widget)
        Editable.__init__(self)
        if self.initialize():
            self.item = CTkSlider(master=master, width=width, height=height,
                                  corner_radius=corner_radius,
                                  bg_color=bg_color, fg_color=fg_color,
                                  border_color=border_color, progress_color=progress_color,
                                  button_color=button_color,
                                  button_hover_color=button_hover_color,
                                  from_=from_, to=to, state=state,
                                  number_of_steps=number_of_steps,
                                  hover=hover, command=command,
                                  variable=variable, orientation=orientation, **kwargs)
            self.name = "Slider in" + self.parental_widget.name

            self.initial_value = from_

    @property
    def slider_value(self):
        return self.item.get()

    def set_value(self, value: int):
        self.item.set(value)
