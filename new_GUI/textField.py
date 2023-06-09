"""Класс, представляющий собой лейбл с кнопкой, при нажатию на которую
   лейбл скрывается, на его место ставится Entry и открывается возможность поменять содержимое Entry
   на вход принимает Фрейм, в котором будет распологаться, а также функцию проверки"""
from tkinter import Event
from typing import Tuple
from tkabs.button import Button
from tkabs.fontFabric import FontFabric
from tkabs.frame import Frame
from tkabs.label import Label
from tkabs.entry import Entry
from uiabs.container import Container
from uiabs.editable import Editable


class TextField(Frame, Editable):
    def __init__(self, parental_widget: Container, master: any,
                 validation_method, title: str,
                 placeholder_text: str = "", initial_text: str = "",
                 with_button: bool = False, width: int = 250,
                 border_width: int | str | None = 1,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 enter_pressed_function=None, **kwargs):

        Frame.__init__(self, parental_widget, master, border_width=border_width,
                       width=width, bg_color=bg_color, fg_color=fg_color,
                       border_color=border_color, **kwargs)
        Editable.__init__(self, parental_unit=parental_widget)

        self.validation_method = validation_method
        self.placeholder_text = placeholder_text
        self.initial_text = initial_text
        self.title_text = title

        self.__with_button = with_button

        self.enter_pressed_function = enter_pressed_function

        self.base_font = FontFabric.get_base_font()
        self.initialize()

    @property
    def contained_text(self) -> str:
        return self.get()

    def change_text(self, text: str):
        self.initial_text = text
        self.text_label.change_text(text)

    def get(self) -> str:
        if self.is_being_edited:
            return self.text_entry.contained_text
        else:
            return self.initial_text

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_columnconfigure(1, weight=0)
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

            self.text_entry = Entry(parental_widget=self, master=self.frame,
                                    placeholder_text=self.placeholder_text,
                                    font=self.base_font)
            self.text_entry.entry.grid(row=1, column=0, sticky="nsew")
            self.text_entry.entry.bind('<FocusIn>', lambda event: self.__focused_entry())
            self.text_entry.entry.bind('<FocusOut>', lambda event: self.__unfocused_entry())

            self.add_widget(self.text_entry)

            if self.__with_button:
                self.button = Button(parental_widget=self, master=self.frame, width=40,
                                     text="edit", font=self.base_font, command=self.edit)
                self.button.button.grid(row=0, column=1, rowspan=2, sticky="nsew")
                self.add_widget(self.button)

            return True
        return False

    def __check_for_enter(self, event: Event):
        if event.keysym == 'Return':
            if self.confirm():
                if self.enter_pressed_function is not None:
                    self.enter_pressed_function()

    def __focused_entry(self):
        self.text_entry.entry.bind('<Key>', command=self.__check_for_enter)

    def __unfocused_entry(self):
        self.text_entry.entry.unbind('<Key>')
        self.confirm()

    def show(self) -> bool:
        if super().show():
            if self.is_being_edited:
                self.text_label.hide()
            else:
                self.text_entry.hide()
            return True
        return False

    def edit(self):
        """редактирование поля"""
        Editable.edit(self)
        if self.__with_button:
            self.button.button.configure(command=self.confirm, text="conf")
        self.text_entry.place_text(self.initial_text)
        self.hide()
        self.show()

    def confirm(self) -> bool:
        """Проверка редакции поля, при успешном возвращает True"""
        new_text = self.text_entry.entry.get()
        valid, report = self.validation_method(new_text)
        if valid:
            Editable.confirm(self)
            if self.__with_button:
                self.button.button.configure(command=self.edit, text="edit")

            self.initial_text = new_text
            self.text_label.label.configure(text=new_text)
            self.hide()
            self.show()
            return True
        else:
            self.text_entry.entry.delete(0, len(new_text))
            self.text_entry.entry.configure(placeholder_text=report, placeholder_text_color="#DC143C")
            self.title_label.label.focus()
            return False
