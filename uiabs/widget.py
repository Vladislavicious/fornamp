"""Абстрактный класс, содержащий логику отображения/сокрытия/удаления элемента интерфейса"""


class Widget():
    def __init__(self, parental_widget) -> None:
        self.__is_visible = False
        self.__is_initialized = False
        self.parental_widget = parental_widget
        self.name = "Widget"

    @property
    def is_visible(self):
        return self.__is_visible

    @property
    def is_initialized(self):
        return self.__is_initialized

    def initialize(self) -> bool:
        """Если виджет уже инициализирован, возвращает False"""
        if self.is_initialized:
            return False
        self.__is_initialized = True
        return True

    def destroy(self) -> bool:
        """Если уже уничтожен, возвращает False"""
        if not self.is_initialized:
            return False
        self.__is_initialized = False
        return True

    def show(self) -> bool:
        """Если виджет и так показан, возвращает False"""
        if self.__is_visible:
            return False

        if not self.is_initialized:
            self.initialize()
        self.__is_visible = True
        return True

    def hide(self) -> bool:
        """Возвращает False, если виджет и так не показан"""
        if not self.is_visible:
            return False

        if not self.is_initialized:
            self.initialize()
        self.__is_visible = False
        return True
