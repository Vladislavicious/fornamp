"""Абстракция понятия toplevel в tkinter'е"""
import tkinter as tk
from typing import Tuple
from customtkinter import CTkToplevel, CTkButton

from uiabs.container import Container


class TopLevel(CTkToplevel, Container):
    def __init__(self, *args, parental_widget,
                 fg_color: str | Tuple[str, str] | None = None, **kwargs):
        CTkToplevel.__init__(self, *args, parental_widget, fg_color=fg_color, **kwargs)
        Container.__init__(self, parental_widget)

        self.protocol("WM_DELETE_WINDOW", lambda: self.delete_window())

    def hide(self):
        if Container.hide(self):
            self.withdraw()
            return True
        return False

    def show(self) -> bool:
        if Container.show(self):
            self.deiconify()
            return True
        return False

    def delete_window(self):
        self.destroy()


class MainWindow(TopLevel):
    def __init__(self, *args, parental_widget,
                 fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, parental_widget=parental_widget,
                         fg_color=fg_color, **kwargs)

        self.title("Task manager")
        self.geometry("1000x600+250+100")
        self.resizable(True, True)

        self.button = CTkButton(master=self, text="Открыть Base",
                                command=self.press, width=40, height=10)
        self.button.pack(side=tk.BOTTOM, anchor=tk.E, padx=15)

    def press(self):
        print("нажатие в mainWindow")
        self.parental_widget.show()
        self.hide()
