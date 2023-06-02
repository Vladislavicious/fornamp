"""Абстрактный класс, содержащий логику отображения/сокрытия/удаления элемента интерфейса"""


class Widget():
    def __init__(self, parental_widget) -> None:
        self.__is_visible = False
        self.parental_widget = parental_widget

    @property
    def is_visible(self):
        return self.__is_visible

    def show(self) -> bool:
        """Если виджет и так показан, возвращает False"""
        if self.__is_visible:
            return False
        self.__is_visible = True
        return True

    def hide(self) -> bool:
        """Возвращает False, если виджет и так не показан"""
        if not self.is_visible:
            return False
        self.__is_visible = False
        return True
