"""Абстракция на шрифт, с небольшими дополнениями"""

from dataclasses import dataclass
from typing import Literal
from customtkinter import CTkFont

from ioconnection.Singletone import Singleton

@dataclass
class FontStruct():
    family: str
    size: int


class FontFabric(metaclass=Singleton):
    """Фабрика customTkinter шрифтов"""
    def __init__(self, family: str = "Century gothic",
                 size: int = 16) -> None:
        self.__family = family
        self.__size = size

        self.change_base_font(family=family, size=size)

    def get_base_font(self):
        """Единый шрифт на всё приложение"""
        return self.__font

    def get_bold_font(self):
        """Единый шрифт на всё приложение"""
        return self.__bold_font

    def change_base_font(self, family: str, size: int = 16):
        self.__font = CTkFont(family, size)

        self.__bold_font = CTkFont(family, size, 'bold')

        self.__mean_width = self.__mean_width_calculation(self.__font)

    def get_changed_font(self, size: int | None = None,
                         weight: Literal['normal', 'bold'] = None,
                         slant: Literal['italic', 'roman'] = "roman",
                         underline: bool = False, overstrike: bool = False):
        return CTkFont(self.__family, size, weight, slant,
                       underline, overstrike)

    def get_font_struct(self) -> FontStruct:
        return FontStruct(family=self.__family, size=self.__size)

    def calculate_mean_width(self, font: CTkFont):
        if font == self.__font:
            return self.__mean_width

        return self.__mean_width_calculation(font)

    def __mean_width_calculation(self, font: CTkFont):
        text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" + \
               "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
               "1234567890"

        mean_value = font.measure(text) // len(text) + 1
        return mean_value
