"""Абстракция на шрифт, с небольшими дополнениями"""

from typing import Literal
from customtkinter import CTkFont

from ioconnection.App import Singleton


class FontFabric(metaclass=Singleton):
    """Фабрика customTkinter шрифтов"""
    def __init__(self, family: str | None = "Century gothic", size: int | None = 16,
                 weight: Literal['normal', 'bold'] = "normal",
                 slant: Literal['italic', 'roman'] = "roman",
                 underline: bool = False, overstrike: bool = False) -> None:
        self.initialized = True
        self.family = family
        self.size = size
        self.weight = weight
        self.slant = slant
        self.underline = underline
        self.overstrike = overstrike

        self.font = CTkFont(family, size, weight, slant,
                            underline, overstrike)

        self.bold_font = CTkFont(family, size, 'bold',
                                 slant, underline, overstrike)

        self.mean_width = self.__mean_width_calculation(self.font)

    def get_base_font(self):
        """Единый шрифт на всё приложение"""
        return self.font

    def get_bold_font(self):
        """Единый шрифт на всё приложение"""
        return self.bold_font

    def get_changed_font(self, size: int | None = None,
                         weight: Literal['normal', 'bold'] = None,
                         slant: Literal['italic', 'roman'] = "roman",
                         underline: bool = False, overstrike: bool = False):
        return CTkFont(self.family, size, weight, slant,
                       underline, overstrike)

    def calculate_mean_width(self, font: CTkFont):
        if font == self.font:
            return self.mean_width

        return self.__mean_width_calculation(font)

    def __mean_width_calculation(self, font: CTkFont):
        text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" + \
               "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
               "1234567890"

        mean_value = font.measure(text) // len(text) + 1
        return mean_value
