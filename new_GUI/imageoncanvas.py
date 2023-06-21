from typing import Tuple
from tkabs.canvas import Canvas

from tkabs.frame import Frame
from tkabs.image import Image
from uiabs.container import Container




class ImageOnCanvas(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 image_path: str, image_function=None,
                 width: int = 100, height: int = 100,
                 corner_radius: int | str | None = None,
                 border_width: int | str | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
                 overwrite_preferred_drawing_method: str | None = None, **kwargs):

        super().__init__(parental_widget, master, width,
                         height, corner_radius, border_width,
                         bg_color, fg_color, border_color,
                         background_corner_colors,
                         overwrite_preferred_drawing_method, **kwargs)

        self.light_image_path = image_path
        self.image_function = image_function
        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_rowconfigure(0, weight=1)

            self.canvas = Canvas(parental_widget=self, master=self.frame)
            self.canvas.canvas.grid(row=0, column=0, sticky="nsew")
            self.add_widget(self.canvas)

            self.image = Image(parental_widget=self.canvas,
                               image_path=self.light_image_path,
                               size=(self.width, self.height))
            self.add_widget(self.image)

            if self.image_function is not None:
                self.canvas.canvas.bind('<Button-1>', func=lambda event: self.image_function())

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