from tkinter import Canvas as cv
from tkabs.image import Image

from uiabs.container import Container


class Canvas(Container):
    def __init__(self, parental_widget, master, *args, **kwargs):

        super().__init__(parental_widget=parental_widget)

        self.canvas = cv(master, *args, **kwargs)

    @property
    def width(self) -> int:
        return self.canvas.winfo_width()

    @property
    def height(self) -> int:
        return self.canvas.winfo_height()

    def create_image(self, image: Image):
        self.canvas.create_image(0, 0, anchor="nw", image=image.image)

    def show(self) -> bool:
        if super().show():
            self.canvas.grid()
            return True
        return False

    def hide(self) -> bool:
        if super().hide():
            self.canvas.grid_remove()
            return True
        return False
