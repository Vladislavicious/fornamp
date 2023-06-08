from tkinter import Variable
from typing import Callable, Tuple
from customtkinter import CTkSlider

from uiabs.container import Container


class Slider(Container):
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

        super().__init__(parental_widget=parental_widget)
        if self.initialize():
            self.slider = CTkSlider(master=master, width=width, height=height,
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

            self.__is_being_edited = False
            self.is_edited = False
            self.initial_value = from_

    @property
    def is_confirmed(self) -> bool:
        return not self.__is_being_edited

    @property
    def slider_value(self):
        return self.slider.get()

    def set_value(self, value: int):
        self.slider.set(value)

    def edit(self):
        self.__is_being_edited = True

    def confirm(self):
        self.is_edited = True
        self.__is_being_edited = False

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
