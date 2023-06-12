"""Класс, представляющий собой лейбл с кнопкой, при нажатию на которую
   лейбл скрывается, на его место ставится Entry и открывается возможность поменять содержимое Entry
   на вход принимает Фрейм, в котором будет распологаться, а также функцию проверки"""
from tkinter import Event
from typing import Tuple
from tkabs.button import Button
from UIadjusters.fontFabric import FontFabric
from tkabs.frame import Frame
from tkabs.label import Label
from tkabs.entry import Entry
from uiabs.container import Container


class labeledText(Frame):
    def __init__(self, parental_widget: Container, master: any, title: str,
                 initial_text: str = "", width: int = 250,
                 border_width: int | str | None = 1,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None, **kwargs):

        super().__init__(parental_widget, master, border_width=border_width,
                         width=width, bg_color=bg_color, fg_color=fg_color,
                         border_color=border_color, **kwargs)

        self.initial_text = initial_text
        self.title_text = title

        self.base_font = FontFabric.get_base_font()
        self.initialize()

    def change_title(self, title: str):
        self.title_text = title
        self.title_label.label.configure(text=title)

    def change_text(self, text: str):
        self.initial_text = text
        self.text_label.label.configure(text=text)

    def get(self) -> str:
        return self.initial_text

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_rowconfigure(0, weight=1)
            self.frame.grid_rowconfigure(1, weight=3)
            self.frame.grid_propagate(True)

            self.title_label = Label(parental_widget=self, master=self.frame,
                                     text=self.title_text,
                                     font=FontFabric.get_changed_font(weight='bold'))
            self.title_label.label.grid(row=0, column=0, sticky="nsew")
            self.add_widget(self.title_label)

            self.text_label = Label(parental_widget=self, master=self.frame,
                                    text=self.initial_text, font=self.base_font)
            self.text_label.label.grid(row=1, column=0, sticky="nsew")
            self.add_widget(self.text_label)

            return True
        return False

    def show(self) -> bool:
        if super().show():
            return True
        return False
