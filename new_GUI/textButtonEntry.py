"""Класс, представляющий собой лейбл с кнопкой, при нажатию на которую
   лейбл скрывается, на его место ставится Entry и открывается возможность поменять содержимое Entry
   на вход принимает Фрейм, в котором будет распологаться, а также функцию проверки"""
from typing import Tuple
from tkabs.button import Button
from tkabs.fontFabric import FontFabric
from tkabs.frame import Frame
from tkabs.label import Label
from tkabs.entry import Entry
from uiabs.container import Container


class textButtonEntry(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 validation_method, title: str,
                 placeholder_text: str = "", initial_text: str = "",
                 border_width: int | str | None = 1,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = "#123456", **kwargs):

        super().__init__(parental_widget, master, border_width,
                         bg_color=bg_color, fg_color=fg_color,
                         border_color=border_color, **kwargs)

        self.validation_method = validation_method
        self.placeholder_text = placeholder_text
        self.initial_text = initial_text
        self.title_text = title

        self.__is_being_edited = False
        self.is_edited = False

        self.base_font = FontFabric.get_base_font()
        self.initialize()

    @property
    def contained_text(self) -> str:
        return self.text_entry.entry.get()

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_columnconfigure(0, weight=3)
            self.frame.grid_columnconfigure(1, weight=1)
            self.frame.grid_rowconfigure(0, weight=1)
            self.frame.grid_rowconfigure(1, weight=3)

            self.title_label = Label(parental_widget=self, master=self.frame,
                                     text=self.title_text, font=self.base_font)
            self.title_label.label.grid(row=0, column=0, sticky="nsew")
            self.add_widget(self.title_label)

            self.text_label = Label(parental_widget=self, master=self.frame,
                                    text=self.initial_text, font=self.base_font)
            self.text_label.label.grid(row=1, column=0, sticky="nsew")
            self.add_widget(self.text_label)

            self.text_entry = Entry(parental_widget=self, master=self.frame,
                                    placeholder_text=self.placeholder_text,
                                    font=self.base_font)
            self.text_entry.entry.grid(row=1, column=0, sticky="nsew")
            self.add_widget(self.text_entry)

            self.button = Button(parental_widget=self, master=self.frame,
                                 text="Edit", font=self.base_font, command=self.__edit)
            self.button.button.grid(row=0, column=1, rowspan=2, sticky="nsew")
            self.add_widget(self.button)

            return True
        return False

    def show(self) -> bool:
        if super().show():
            if self.__is_being_edited:
                self.text_label.hide()
            else:
                self.text_entry.hide()
            return True
        return False

    def __edit(self):
        self.__is_being_edited = True
        self.button.button.configure(command=self.__confirm, text="confirm")
        self.hide()
        self.show()
        pass

    def __confirm(self):
        new_text = self.text_entry.entry.get()
        valid, report = self.validation_method(new_text)
        if valid:
            self.__is_being_edited = False
            self.is_edited = True
            self.button.button.configure(command=self.__edit, text="edit")

            self.text_label.label.configure(text=new_text)
            self.hide()
            self.show()
        else:
            self.text_entry.entry.delete(0, len(new_text))
            self.text_entry.entry.configure(placeholder_text=report, placeholder_text_color="#DC143C")
            self.button.button.focus()
