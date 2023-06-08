"""
Интерфейс для обеспечения изменяемости класса
"""


class Editable():
    def __init__(self, parental_unit=None) -> None:
        self.__is_being_edited = False
        self.__is_edited = False
        self.__parental_unit = parental_unit

    @property
    def is_edited(self) -> bool:
        return self.__is_edited

    def set_as_edited(self) -> bool:
        """Если не был изменён до этого, возвращает True"""
        if not self.__is_edited:
            self.__is_edited = True
            if self.__parental_unit is not None:
                self.__parental_unit.set_as_edited()
            return True
        return False

    @property
    def is_confirmed(self) -> bool:
        return not self.__is_being_edited

    @property
    def is_being_edited(self) -> bool:
        return self.__is_being_edited

    def edit(self):
        """редактирование поля"""
        self.__is_being_edited = True

    def confirm(self) -> bool:
        """Возвращает True, если до этого был в состоянии редактирования"""
        if self.__is_being_edited is True:
            self.set_as_edited()
            self.__is_being_edited = False
            return True
        return False

    def save(self) -> bool:
        """метод сохранения
           при успешном сохранении, возвращает True"""
        if not self.__is_being_edited:
            self.__is_edited = False
            return True
        return False
