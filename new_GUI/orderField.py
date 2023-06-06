from datetime import date
from typing import Tuple
from BaH.order import Order
from new_GUI.textField import TextField
from tkabs.button import Button
from tkabs.frame import Frame
from tkabs.label import Label
from tkabs.fontFabric import FontFabric
from uiabs.container import Container
from customtkinter import CTkFrame

def is_valid_string(s):
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя.,:/" ')
    return all(c in allowed_chars for c in s)


def validate_customer(string: str = "") -> Tuple[bool, str]:
    """Проверяет строку на соответствие параметрам"""
    length = len(string)
    if length < 2:
        return False, "Строка слишком короткая"
    if length > 32:
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


def validate_description(string: str = "") -> Tuple[bool, str]:
    if len(string) > 256:
        return False, "Слишком длинное описание"
    if is_valid_string(string.lower()):
        return True, ""
    return False, "Содержит неподобающие символы"


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
                 width: int = 250, height: int = 200,
                 border_width: int | str | None = 2,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = "#B22222"):

        super().__init__(parental_widget=parental_widget, master=master,
                         width=width, height=height,
                         border_width=border_width, bg_color=bg_color,
                         fg_color=fg_color, border_color=border_color)
        self.base_font = FontFabric.get_base_font()
        self.order = order
        self.is_edited = False
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
            self.frame.grid_propagate(False)

            self.edit_button = Button(parental_widget=self, master=self.frame, text="edit",
                                      command=self.edit_all_fields, font=self.base_font, width=40)
            self.edit_button.button.grid(row=0, column=0, padx=3, pady=3, sticky="ne")
            self.add_widget(self.edit_button)

            self.id_label = Label(self, self.frame, text="id: " + self.id,
                                  font=FontFabric.get_changed_font(weight='bold'))
            self.id_label.label.grid(row=0, column=0, pady=3, sticky="n")
            self.add_widget(self.id_label)

            self.customer_field = TextField(parental_widget=self, master=self.frame,
                                            validation_method=validate_customer, title="Заказчик",
                                            placeholder_text="Введите заказчика", initial_text=self.customer)
            self.customer_field.frame.grid(row=2, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.customer_field)

            self.date_oc_field = TextField(parental_widget=self, master=self.frame,
                                           validation_method=validate_date, title="Дата создания",
                                           placeholder_text="ДД-ММ-ГГГГ", initial_text=self.date_oc)
            self.date_oc_field.frame.grid(row=3, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.date_oc_field)

            self.date_ov_field = TextField(parental_widget=self, master=self.frame,
                                           validation_method=validate_date_ov, title="Дата Выдачи",
                                           placeholder_text="ДД-ММ-ГГГГ", initial_text=self.date_ov)
            self.date_ov_field.frame.grid(row=4, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.date_ov_field)

            self.description_field = TextField(parental_widget=self, master=self.frame,
                                               validation_method=validate_description, title="Комментарий",
                                               placeholder_text="Уточнения по заказу",
                                               initial_text=self.description)
            self.description_field.frame.grid(row=5, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.description_field)

            self.fields = [self.customer_field, self.date_oc_field,
                           self.date_ov_field, self.description_field]
            return True
        return False

    def edit_all_fields(self):
        self.edit_button.button.configure(text="conf", command=self.conf_all_fields)
        for field in self.fields:
            field.edit()

    def conf_all_fields(self):
        is_confirmed = True
        for field in self.fields:
            field.confirm()
            if field.is_confirmed is False:
                is_confirmed = False

        if is_confirmed:
            self.is_edited = True
            self.edit_button.button.configure(text="edit", command=self.edit_all_fields)

            # Сохранение изменений в заказе
