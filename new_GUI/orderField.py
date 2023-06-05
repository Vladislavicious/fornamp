from datetime import date
from typing import Tuple
from BaH.order import Order
from new_GUI.textField import TextField
from tkabs.frame import Frame
from tkabs.label import Label
from tkabs.fontFabric import FontFabric
from uiabs.container import Container


def is_valid_string(s):
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя., ')
    return all(c in allowed_chars for c in s)


def validate_customer(string: str = "") -> Tuple[bool, str]:
    """Проверяет строку на соответствие параметрам"""
    if len(string) > 32:
        return False, "Строка слишком длинная"
    if not is_valid_string(string.lower()):
        return False, "Содержит неподобающие символы"
    return True, ""


def validate_date(parsed_date: str) -> Tuple[bool, str]:
    """Проверяет дату на соответствие ДД-ММ-ГГГГ"""
    try:
        days = int(parsed_date[:2])
        month = int(parsed_date[3:5])
        years = int(parsed_date[6:10])
        data = date(years, month, days)

        return True, ""
    except ValueError:
        return False, "Введена невозможная дата"


def validate_date_ov(parsed_date: str) -> Tuple[bool, str]:
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


class OrderField(Frame):
    def __init__(self, parental_widget: Container, master: any, order: Order = None,
                 width: int = 200, height: int = 200,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = "#B22222", **kwargs):

        super().__init__(parental_widget=parental_widget, master=master,
                         width=width, height=height,
                         border_width=2, bg_color=bg_color,
                         fg_color=fg_color, border_color=border_color, **kwargs)

        self.base_font = FontFabric.get_base_font()
        self.order = order
        # все характеристики order будут в виде строк
        if order is not None:
            self.id = str(order.id)
            self.customer = order.zakazchik
            self.date_oc = order.date_of_creation.strftime("%d/%m/%Y")
            self.date_ov = order.date_of_vidacha.strftime("%d/%m/%Y")
            self.description = order.commentary
        else:
            self.id = ""
            self.customer = ""
            self.date_oc = ""
            self.date_ov = ""
            self.description = ""

        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            if self.order.isDone:
                if self.order.isVidan:
                    self.frame.configure(border_color="#7FFF00")
                else:
                    self.frame.configure(border_color="#FFA500")

            self.frame.grid_columnconfigure(0, weight=1)

            self.id_label = Label(self, self.frame, text="id: " + self.id, font=self.base_font)
            self.id_label.label.grid(row=0, column=0, padx=3, pady=3, sticky="w")
            self.add_widget(self.id_label)

            self.customer_field = TextField(parental_widget=self, master=self.frame,
                                            validation_method=validate_customer, title="Заказчик",
                                            placeholder_text="Введите заказчика", initial_text=self.customer)
            self.customer_field.frame.grid(row=1, column=0, padx=3, pady=3, sticky="w")
            self.add_widget(self.customer_field)

            self.date_oc_field = TextField(self, self.frame, validate_date, "Дата создания",
                                           "ДД-ММ-ГГГГ", initial_text=self.date_oc)
            self.date_oc_field.frame.grid(row=2, column=0, padx=3, pady=3, sticky="w")
            self.add_widget(self.date_oc_field)

            self.date_ov_field = TextField(self, self.frame, validate_date_ov, "Дата Выдачи",
                                           "ДД-ММ-ГГГГ", initial_text=self.date_ov)
            self.date_ov_field.frame.grid(row=3, column=0, padx=3, pady=3, sticky="w")
            self.add_widget(self.date_ov_field)

            return True
        return False
