from tkinter import Variable
from typing import Callable, Tuple
from customtkinter import CTkSlider

from uiabs.container import Container


class Slider(Container):
    def __init__(self, parental_widget: Container, master: any, width: int | None = None,
                 height: int | None = None, corner_radius: int | None = None,
                 button_corner_radius: int | None = None,
                 border_width: int | None = None,
                 button_length: int | None = None,
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

        super().__init__()
        if self.initialize():
            self.slider = CTkSlider(master, width, height, corner_radius,
                                    button_corner_radius, border_width,
                                    button_length, bg_color, fg_color,
                                    border_color, progress_color, button_color,
                                    button_hover_color, from_, to, state,
                                    number_of_steps, hover, command,
                                    variable, orientation, **kwargs)
            self.name = "Slider in" + self.parental_widget.name

    @property
    def slider_value(self):
        return self.slider.get()

    def destroy(self) -> bool:
        if super().destroy():
            self.slider.destroy()
            return True
        return False

    def hide(self) -> bool:
        if super().hide():
            self.slider.grid_remove()
            return True
        return False

    def show(self) -> bool:
        if super().show():
            self.slider.grid()
            return True
        return False
