import logging

from os import path
from UIadjusters.fontFabric import FontFabric
from new_GUI.imageoncanvas import ImageOnCanvas
from tkabs.dialog import Dialog

from tkabs.frame import Frame
from tkabs.label import Label
from uiabs.Container_tk import Container_tk
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# настройка обработчика и форматировщика для logger
handler = logging.FileHandler(path.abspath(path.curdir)+f"\\logs\\{__name__}.log", mode='w', encoding="utf-8")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)

logger.info(f"Testing the custom logger for module {__name__}...")


class Photo(Frame):
    def __init__(self, parental_widget: Container_tk, master: any,
                 photopath: str,
                 width: int = 200, height: int = 200,
                 border_width: int | None = None,
                 bg_color: str | None = None,
                 fg_color: str | None = None,
                 border_color: str | None = None, **kwargs):

        super().__init__(parental_widget, master, width,
                         height, border_width, bg_color,
                         fg_color, border_color, **kwargs)
        self.dialog = None
        self.photopath = photopath
        self.ff = FontFabric.get_instance()
        self.font = self.ff.get_base_font()
        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():

            self.item.grid_rowconfigure(0, weight=1)
            self.item.grid_columnconfigure(0, weight=1)

            _, _, self.name = self.photopath.rpartition("\\")

            self.label = Label(parental_widget=self, master=self.item,
                               text=self.name, font=self.font)
            self.label.item.grid(row=1, column=0, pady=2, sticky="nsew")
            self.add_widget(self.label)

            self.canvas = ImageOnCanvas(parental_widget=self, master=self.item,
                                        image_path=self.photopath, image_function=self.press)
            self.canvas.item.grid(row=0, column=0, pady=1, sticky="ns")
            self.add_widget(self.canvas)

            return True
        return False

    def withdraw_dialog(self):
        self.dialog.disappear()

    def press(self):
        if self.dialog is None:
            self.dialog = Dialog.get_instance()

        self.dialog.set_name(self.name)
        self.dialog.center()

        frame = ImageOnCanvas(parental_widget=self.dialog, master=self.dialog.frame.item,
                              image_path=self.photopath, width=self.dialog.width,
                              image_function=self.withdraw_dialog, height=self.dialog.height)

        self.dialog.set_widget_frame(frame)

        self.dialog.show()
        frame.fit()

    def draw(self):
        self.item.update_idletasks()
        super().draw()
