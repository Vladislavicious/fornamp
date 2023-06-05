"""Представляет собой один товар, состоит из textButton полей,
   на вход принимает помимо прочего frame для шагов, чтобы у каждого
   продукта был свой набор шагов, которые будут отображаться на один конкретный
   frame"""

from customtkinter import CTkFont
from BaH.product import Product
from tkabs.frame import Frame
from tkabs.label import Label
from uiabs.container import Container


def shorter(string: str, length: int = 60) -> str:
    string_len = len(string)

    new_string = "\n".join(list([string[i:i + length] for i in range(0, string_len, length)]))
    return new_string


class ProductField(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 product: Product, step_frame: Frame):
        border_width = 2
        border_color = "#B22222"
        super().__init__(parental_widget, master, border_width=border_width,
                         border_color=border_color)
        self.product = product
        self.step_frame = step_frame
        self.base_font = CTkFont(family="Century gothic", size=16)

        self.initialize()

    def __configure_string_length(self, string: str):

        string_length = len(string)
        if string_length > 60:
            new_string_length = 60
            return shorter(string, new_string_length)
        return string

    def initialize(self) -> bool:
        if super().initialize():
            if self.product.isDone:
                self.frame.configure(border_color="#FFA500")

            self.frame.rowconfigure(0, weight=1)
            self.frame.rowconfigure(1, weight=1)
            self.frame.rowconfigure(2, weight=1)

            self.frame.columnconfigure(0, weight=1)

            return True
        return False
