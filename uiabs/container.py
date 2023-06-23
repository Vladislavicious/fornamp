"""Абстрактный класс, содержащий логику отображения элементов, содержащих виджеты внутри себя"""
from uiabs.widget import Widget


class Container(Widget):
    def __init__(self, parental_widget) -> None:
        super().__init__(parental_widget)
        self.name = "Container"
        self.__widgets = set()  # является множеством, чтобы исключить нахождение нескольких одинаковых виджетов

    @property
    def widgets(self):
        return self.__widgets

    @property
    def items_count(self) -> int:
        return len(self.__widgets)

    def get_class_instances(self, class_type):
        new_spis = list()
        for i in self.widgets:
            if isinstance(i, class_type):
                new_spis.append(i)
        return new_spis

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

    def remove_widget(self, widget: Widget):
        self.__widgets.discard(widget)

    def delete_widget(self, widget: Widget):
        self.remove_widget(widget)
        widget.destroy()

    def add_widget(self, widget: Widget):
        self.__widgets.add(widget)
        if self.is_visible:
            widget.show()

    def clear_widgets(self):
        self.__widgets.clear()

    def bind(self, sequence: str, function, bind_to_childs: bool = False):
        if self.item is not None:
            self.item.bind(sequence, function)

        if not bind_to_childs:
            return

        for widget in self.widgets:
            widget.bind(sequence, function, bind_to_childs)

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
