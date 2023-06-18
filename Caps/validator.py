

from datetime import date
from typing import Tuple


class Validator():
    @classmethod
    def is_valid_string(cls, string: str) -> bool:
        """Проверяет строку на соответствие обычному тексту"""
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя.,:/" ')
        return all(c in allowed_chars for c in string)

    @classmethod
    def validate_name(cls, string: str = "") -> Tuple[bool, str]:
        """Проверяет строку на соответствие параметрам"""
        length = len(string)
        if length < 2:
            return False, "Строка слишком короткая"
        if length > 32:
            return False, "Строка слишком длинная"
        if not Validator.is_valid_string(string.lower()):
            return False, "Содержит неподобающие символы"
        return True, ""

    @classmethod
    def validate_date(cls, parsed_date: str) -> Tuple[bool, str]:
        """Проверяет дату на соответствие ДД-ММ-ГГГГ"""
        try:
            days = int(parsed_date[:2])
            month = int(parsed_date[3:5])
            years = int(parsed_date[6:10])

            date(years, month, days)

            return True, ""
        except ValueError:
            return False, "Введена невозможная дата"

    @classmethod
    def validate_description(cls, string: str = "") -> Tuple[bool, str]:
        if len(string) > 256:
            return False, "Слишком длинное описание"
        if Validator.is_valid_string(string.lower()):
            return True, ""
        return False, "Содержит неподобающие символы"

    @classmethod
    def validate_date_ov(cls, parsed_date: str) -> Tuple[bool, str]:
        try:
            days = int(parsed_date[:2])
            month = int(parsed_date[3:5])
            years = int(parsed_date[6:10])
            data = date(years, month, days)

            if data >= date.today():
                return True, ""
            else:
                return False, "Выдача не может быть в прошлом"
        except ValueError:
            return False, "Введена невозможная дата"

    @classmethod
    def validate_number(cls, string: str = "", name: str = "Количество") -> Tuple[bool, str]:
        if string.isdecimal():
            if int(string) <= 0:
                return False, f"{name} меньше 1"
            return True, ""
        elif len(string) == 0:
            return False, f"Введите {name}"
        return False, "Введите число"
