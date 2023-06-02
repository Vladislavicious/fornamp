"""Абстрактный класс, содержащий логику отображения элементов, содержащих виджеты внутри себя"""
from typing import List

from uiabs.widget import Widget


class Container(Widget):
    def __init__(self, parental_widget, widgets: List[Widget] = list()) -> None:
        super().__init__(parental_widget)

        self.__widgets = set()  # является множеством, чтобы исключить нахождение нескольких одинаковых виджетов

        self.__parse_widgets(widgets)

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
        widget.hide()

    def addWidget(self, widget: Widget):
        self.__widgets.add(widget)
        if self.is_visible:
            widget.show()

    def __hide_all_widgets(self):
        for widget in self.__widgets:
            widget.destroy()

    def __show_all_widgets(self):
        for widget in self.__widgets:
            widget.show()

    def __parse_widgets(self, widgets: List[Widget]):
        for widget in widgets:
            widget.parental_widget = self
            self.addWidget(widget)
