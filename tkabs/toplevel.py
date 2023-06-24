"""Абстракция понятия toplevel в tkinter'е"""
from customtkinter import CTkToplevel
from UIadjusters.colorFabric import ColorFabric
from uiabs.Container_tk import Container_tk


class TopLevel(CTkToplevel, Container_tk):
    def __init__(self, *args, parental_widget, master,
                 fg_color: str | None = None, **kwargs):
        self.cf = ColorFabric.get_instance()
        if fg_color is None:
            fg_color = self.cf.foreground
        CTkToplevel.__init__(self, master, fg_color=fg_color, *args, **kwargs)
        Container_tk.__init__(self, parental_widget)
        self.name = "TopLevel"

    def erase(self):
        self.withdraw()

    def draw(self):
        self.deiconify()

    def inner_delete(self):
        CTkToplevel.destroy(self)
        if self.parental_widget is not None:
            self.parental_widget.show()

    def initialize(self) -> bool:
        if Container_tk.initialize(self):
            self.grid_rowconfigure(0, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)

            self.protocol("WM_DELETE_WINDOW", lambda: self.delete())
            return True
        return False
