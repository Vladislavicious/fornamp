from typing import Tuple
from customtkinter import CTkToplevel

from ioconnection.App import Singleton
from tkabs.frame import Frame

from uiabs.container import Container


class Dialog(CTkToplevel, Container, metaclass=Singleton):
    """Диалоговое окно, всегда одно на приложение, удаляется при закрытии приложения,
    в остальных случаях просто скрывается."""
    def __init__(self, *args, parental_widget, master,
                 fg_color: str | Tuple[str, str] | None = None, **kwargs):
        CTkToplevel.__init__(self, master, fg_color=fg_color, *args, **kwargs)
        Container.__init__(self, parental_widget)

        self.name = "Dialog"
        self.frame = None
        self.initialize()

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
            self.resizable(False, False)
            self.geometry("500x220+200+200")
            self.attributes("-toolwindow", True)
            self.grid_rowconfigure(0, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)

            self.protocol("WM_DELETE_WINDOW", lambda: self.hide())
            return True
        return False

    def set_name(self, name: str):
        self.title(name)

    def set_geometry(self, width: int = 800, height: int = 600,
                     xpos: int = 0, ypos: int = 0):
        string = str(width) + "x" + str(height) + "+" + str(xpos) + "+" + str(ypos)
        self.geometry(string)

    def set_frame(self, frame: Frame):
        if self.frame is not None:
            self.delete_widget(self.frame)

        self.frame = frame
        self.frame.show()
        self.frame.frame.grid(row=0, column=0, sticky="nsew")
        self.add_widget(self.frame)
