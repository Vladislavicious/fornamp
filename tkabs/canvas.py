from tkinter import Canvas as cv
from tkabs.image import Image
from uiabs.Container_tk import Container_tk


class Canvas(Container_tk):
    def __init__(self, parental_widget, master, *args, **kwargs):

        super().__init__(parental_widget=parental_widget)
        self.__drawn_image = None

        self.item = cv(master, *args, **kwargs)

    @property
    def width(self) -> int:
        return self.item.winfo_width()

    @property
    def height(self) -> int:
        return self.item.winfo_height()

    def create_image(self, image: Image):
        self.__drawn_image = image.item
        self.item.create_image(0, 0, anchor="nw", image=self.__drawn_image)
