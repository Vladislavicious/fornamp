"""Абстракция на ползунок со значениями 'от' и 'до'"""

from typing import Tuple
from new_GUI.textField import TextField
from tkabs.slider import Slider
from tkabs.fontFabric import FontFabric
from tkabs.frame import Frame
from uiabs.container import Container


def validate_number(string: str = "", name: str = "Количество") -> Tuple[bool, str]:
    if string.isdecimal():
        if int(string) <= 0:
            return False, f"{name} меньше 1"
        return True, ""
    elif len(string) == 0:
        return False, f"Введите {name}"
    return False, "Введите число"


class Runner(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 from_value: int = 0, to_value: int = 1, steps_count: int = 1,
                 width: int = 100, height: int = 100,
                 border_width: int | str | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None):

        super().__init__(parental_widget=parental_widget, master=master,
                         width=width, height=height,
                         border_width=border_width, bg_color=bg_color,
                         fg_color=fg_color, border_color=border_color)

        if from_value < 0:
            from_value = 0
        if to_value < 1:
            to_value = 1
        if to_value == from_value:
            to_value += 1
        if to_value < from_value:
            (to_value, from_value) = (to_value, from_value)
            print("Очень плохие данные в слайдере")

        self.base_font = FontFabric.get_base_font()
        self.is_edited = False
        self.steps_count = steps_count
        self.from_value_text = str(from_value)
        self.to_value_text = str(to_value)

        self.initialize()

    @property
    def slider_value(self):
        return self.slider.slider_value

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_rowconfigure(0, weight=1)
            self.frame.grid_columnconfigure(0, weight=0)
            self.frame.grid_columnconfigure(1, weight=1)
            self.frame.grid_columnconfigure(2, weight=0)
            self.frame.grid_propagate(False)

            self.from_field = TextField(parental_widget=self, master=self.frame,
                                        title="От",
                                        validation_method=lambda value:
                                        validate_number(string=value, name="От"),
                                        initial_text=self.from_value_text)
            self.from_field.frame.grid(row=0, column=0, sticky="w")
            self.add_widget(self.from_field)

            self.to_field = TextField(parental_widget=self, master=self.frame,
                                      title="До",
                                      validation_method=lambda value:
                                      validate_number(string=value, name="До"),
                                      initial_text=self.to_value_text)
            self.to_field.frame.grid(row=0, column=2, sticky="e")
            self.add_widget(self.to_field)

            from_int = int(self.from_value_text)
            to_int = int(self.to_value_text)
            self.slider = Slider(parental_widget=self, master=self.frame,
                                 from_=0, to=to_int,
                                 number_of_steps=self.steps_count)
            self.slider.slider.set(from_int)
            self.slider.slider.grid(row=0, column=1, sticky="nsew")
            self.add_widget(self.slider)

            self.fields = [self.from_field, self.to_field]
            return True
        return False

    def edit_all_fields(self):
        for field in self.fields:
            field.edit()

    def conf_all_fields(self):
        is_confirmed = True
        for field in self.fields:
            field.confirm()
            if field.is_confirmed is False:
                is_confirmed = False

        if is_confirmed:
            self.is_edited = True

             # поменять значения в границах слайдера
