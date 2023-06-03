"""Абстракция понятия toplevel в tkinter'е"""
from typing import Tuple
from customtkinter import CTkToplevel


from uiabs.container import Container


class TopLevel(CTkToplevel, Container):
    def __init__(self, *args, parental_widget,
                 fg_color: str | Tuple[str, str] | None = None, **kwargs):
        CTkToplevel.__init__(self, *args, parental_widget, fg_color=fg_color, **kwargs)
        Container.__init__(self, parental_widget)
        self.name = "TopLevel"

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

    def destroy(self) -> bool:
        if Container.destroy(self):
            CTkToplevel.destroy(self)
            if self.parental_widget is not None:
                self.parental_widget.show()
            return True
        return False

    def initialize(self) -> bool:
        if Container.initialize(self):
            self.grid_rowconfigure(0, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)

            self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
            return True
        return False
