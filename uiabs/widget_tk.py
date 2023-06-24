

from uiabs.widget import Widget


class Widget_tk(Widget):
    def __init__(self, parental_widget) -> None:
        super().__init__(parental_widget)
        self.name = "tk widget"

    def delete(self) -> bool:
        if super().delete():
            self.inner_delete()
            return True
        return False

    def hide(self) -> bool:
        if super().hide():
            self.erase()
            return True
        return False

    def show(self) -> bool:
        if super().show():
            self.draw()
            return True
        return False

    def bind(self, sequence: str, function, bind_to_childs: bool = False):
        """Функция для бинда комманд на виджет"""
        if self.item is not None:
            self.item.bind(sequence, function)

    def draw(self):
        self.item.grid()

    def erase(self):
        self.item.grid_remove()

    def inner_delete(self):
        self.item.destroy()
