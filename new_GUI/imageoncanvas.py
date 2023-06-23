from tkabs.canvas import Canvas

from tkabs.frame import Frame
from tkabs.image import Image
from uiabs.container import Container


class ImageOnCanvas(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 image_path: str, image_function=None,
                 width: int = 100, height: int = 100, **kwargs):

        super().__init__(parental_widget, master, width,
                         height, **kwargs)

        self.light_image_path = image_path
        self.image_function = image_function
        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            self.item.grid_columnconfigure(0, weight=1)
            self.item.grid_rowconfigure(0, weight=1)

            self.canvas = Canvas(parental_widget=self, master=self.item)
            self.canvas.item.grid(row=0, column=0, sticky="nsew")
            self.add_widget(self.canvas)

            self.image = Image(parental_widget=self.canvas,
                               image_path=self.light_image_path,
                               size=(self.width, self.height))
            self.add_widget(self.image)

            if self.image_function is not None:
                self.canvas.item.bind('<Button-1>', func=lambda event: self.image_function())
                self.canvas.item.configure(cursor="hand2")

            self.canvas.create_image(self.image)

            return True
        return False

    def fit(self):
        if self.image.resize(self.parental_widget.width, self.parental_widget.height):
            self.canvas.create_image(self.image)

    def show(self) -> bool:
        if super().show():
            self.fit()
            return True
        return False
