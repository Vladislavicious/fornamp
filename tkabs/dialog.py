from customtkinter import CTkToplevel
from UIadjusters.colorFabric import ColorFabric

from ioconnection.Singletone import Singleton
from tkabs.frame import Frame
from uiabs.container_tk import Container_tk


class Dialog(CTkToplevel, Container_tk, metaclass=Singleton):
    """Диалоговое окно, всегда одно на приложение, удаляется при закрытии приложения,
    в остальных случаях просто скрывается."""
    def __init__(self, parental_widget, master,
                 fg_color: str | None = None,
                 *args, **kwargs):

        self.cf = ColorFabric.get_instance()
        if fg_color is None:
            fg_color = self.cf.foreground
        CTkToplevel.__init__(self, master, fg_color=fg_color, *args, **kwargs)
        Container_tk.__init__(self, parental_widget)

        self.name = "Dialog"
        self.widget_frame = None
        self.initialize()

    @property
    def width(self) -> int:
        return self.winfo_width()

    @property
    def height(self) -> int:
        return self.winfo_height()

    def hide(self):
        if Container_tk.hide(self):
            return True
        return False

    def delete(self) -> bool:
        if Container_tk.delete(self):
            if self.parental_widget is not None:
                self.parental_widget.show()
            return True
        return False

    def draw(self):
        super().draw()
        self.deiconify()

    def erase(self):
        self.withdraw()

    def inner_delete(self):
        CTkToplevel.destroy(self)

    def disappear(self):
        self.hide()
        if self.widget_frame is not None:
            self.delete_widget(self.widget_frame)
            self.widget_frame = None

    def initialize(self) -> bool:
        if Container_tk.initialize(self):
            self.resizable(False, False)
            self.geometry("500x220+200+200")
            self.attributes("-toolwindow", True)
            self.grid_rowconfigure(0, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)

            self.frame = Frame(parental_widget=self, master=self)
            self.frame.item.grid(row=0, column=0, sticky="nsew")
            self.frame.item.grid_columnconfigure(0, weight=1)
            self.frame.item.grid_rowconfigure(0, weight=1)
            self.add_widget(self.frame)

            self.protocol("WM_DELETE_WINDOW", lambda: self.disappear())
            return True
        return False

    def set_name(self, name: str):
        self.title(name)

    def set_geometry(self, width: int = 800, height: int = 600,
                     xpos: int = 0, ypos: int = 0):
        string = str(width) + "x" + str(height) + "+" + str(xpos) + "+" + str(ypos)
        self.geometry(string)

    def center(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        window_width = int(screen_width * 2 / 3)
        window_height = int(screen_height * 2 / 3)

        offset_x = (screen_width - window_width) // 2
        offset_y = (screen_height - window_height) // 2

        self.set_geometry(window_width, window_height, offset_x, offset_y)

    def set_widget_frame(self, widget_frame: Frame):
        if self.widget_frame is not None:
            self.delete_widget(self.widget_frame)
            self.widget_frame = None

        self.widget_frame = widget_frame
        self.widget_frame.item.grid(row=0, column=0, sticky="nsew")
        self.add_widget(self.widget_frame)
