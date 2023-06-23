from typing import Tuple
from PIL import Image as Img
from PIL import ImageTk

from uiabs.widget import Widget


class Image(Widget):
    def __init__(self, parental_widget, image_path: str,
                 size: Tuple[int, int] = ...):
        super().__init__(parental_widget)
        self.image_raw = Img.open(image_path)
        self.item = ImageTk.PhotoImage(self.image_raw, size)

    def resize(self, width, height):
        """Возвращает True, если размер изменился
        """
        img_width = self.item.width()
        img_height = self.item.height()
        if width == img_width and height == img_height:
            return False

        self.scaled_photo = self.image_raw.resize((width, height))

        self.item = ImageTk.PhotoImage(self.scaled_photo)
        return True
