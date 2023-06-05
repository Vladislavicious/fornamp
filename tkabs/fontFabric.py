"""Абстракция на шрифт, с небольшими дополнениями"""

from typing import Literal
from customtkinter import CTkFont


class FontFabric():
    """Фабрика customTkinter шрифтов"""
    initialized = False

    @classmethod
    def initialize_base_font(cls, family: str | None = "Century gothic", size: int | None = 16,
                             weight: Literal['normal', 'bold'] = None,
                             slant: Literal['italic', 'roman'] = "roman",
                             underline: bool = False, overstrike: bool = False):
        cls.initialized = True
        cls.family = family
        cls.size = size
        cls.weight = weight
        cls.slant = slant
        cls.underline = underline
        cls.overstrike = overstrike

        cls.font = CTkFont(family, size, weight, slant,
                           underline, overstrike)

        cls.bold_font = CTkFont(family, size, 'bold',
                                slant, underline, overstrike)

        cls.mean_width = cls.__mean_width_calculation(cls.font)

    @classmethod
    def get_base_font(cls):
        """Единый шрифт на всё приложение"""
        if not cls.initialized:
            cls.initialize_base_font()
        return cls.font

    @classmethod
    def get_bold_font(cls):
        """Единый шрифт на всё приложение"""
        if not cls.initialized:
            cls.initialize_base_font()
        return cls.bold_font

    @classmethod
    def get_changed_font(cls, size: int | None = None,
                         weight: Literal['normal', 'bold'] = None,
                         slant: Literal['italic', 'roman'] = "roman",
                         underline: bool = False, overstrike: bool = False):
        if not cls.initialized:
            cls.initialize_base_font()
        return CTkFont(cls.family, size, weight, slant,
                       underline, overstrike)

    @classmethod
    def calculate_mean_width(cls, font: CTkFont):
        if font == cls.font:
            return cls.mean_width

        return cls.__mean_width_calculation(font)

    @classmethod
    def __mean_width_calculation(cls, font: CTkFont):
        text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" + \
               "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + \
               "1234567890"

        mean_value = font.measure(text) // len(text) + 1
        return mean_value
