from tkinter import Variable
from typing import Callable, Tuple
from customtkinter import CTkSlider

from uiabs.container import Container
from uiabs.editable import Editable
from uiabs.widget import Widget


class Slider(Widget, Editable):
    def __init__(self, parental_widget: Container, master: any, width: int | None = 200,
                 height: int | None = 30, corner_radius: int | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] = "transparent",
                 progress_color: str | Tuple[str, str] | None = None,
                 button_color: str | Tuple[str, str] | None = None,
                 button_hover_color: str | Tuple[str, str] | None = None,
                 from_: int = 0, to: int = 1, state: str = "normal",
                 number_of_steps: int | None = None, hover: bool = True,
                 command: Callable[[float], None] | None = None,
                 variable: Variable | None = None, orientation: str = "horizontal", **kwargs):

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
