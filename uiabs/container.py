"""Абстрактный класс, содержащий логику отображения элементов, содержащих виджеты внутри себя"""
from typing import List

from uiabs.widget import Widget


class Container(Widget):
    def __init__(self, parental_widget) -> None:
        super().__init__(parental_widget)
        self.name = "Container"
        self.__widgets = set()  # является множеством, чтобы исключить нахождение нескольких одинаковых виджетов

    def initialize(self) -> bool:
        if super().initialize():
            self.__initialize_all_widgets()
            return True
        return False

    def destroy(self) -> bool:
        if super().destroy():
            self.__destroy_all_widgets()
            return True
        return False

    def hide(self) -> bool:
        if super().hide():
            self.__hide_all_widgets()
            return True
        return False

    def show(self) -> bool:
        if super().show():
            self.__show_all_widgets()
            return True
        return False

    def deleteWidget(self, widget: Widget):
        self.__widgets.discard(widget)
        widget.destroy()

    def addWidget(self, widget: Widget):
        self.__widgets.add(widget)
        if self.is_visible:
            widget.show()

    def __hide_all_widgets(self):
        for widget in self.__widgets:
            widget.hide()

    def __show_all_widgets(self):
        for widget in self.__widgets:
            widget.show()

    def __initialize_all_widgets(self):
        for widget in self.__widgets:
            widget.initialize()

    def __destroy_all_widgets(self):
        for widget in self.__widgets:
            widget.destroy()

    def __parse_widgets(self, widgets: List[Widget]):
        for widget in widgets:
            widget.parental_widget = self
            self.addWidget(widget)
