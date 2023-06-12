from datetime import date
from typing import Tuple
from ioconnection.App import App
from BaH.order import Order
from new_GUI.textField import TextField
from tkabs.button import Button
from tkabs.frame import Frame
from tkabs.label import Label
from UIadjusters.fontFabric import FontFabric
from uiabs.container import Container

from uiabs.editable import Editable


def get_date(date_string: str) -> date:
    days = int(date_string[:2])
    month = int(date_string[3:5])
    years = int(date_string[6:10])
    data = date(years, month, days)
    return data


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

        date(years, month, days)

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


class OrderField(Frame, Editable):
    def __init__(self, parental_widget: Container, master: any, save_button,
                 order: Order = None, width: int = 250, height: int = 200,
                 border_width: int | str | None = 2,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = "#B22222",
                 change_preview_func=None):

        Frame.__init__(self, parental_widget=parental_widget, master=master,
                       width=width, height=height,
                       border_width=border_width, bg_color=bg_color,
                       fg_color=fg_color, border_color=border_color)
        Editable.__init__(self, parental_unit=None)

        self.base_font = FontFabric.get_base_font()
        self.order = order
        # все характеристики order будут в виде строк
        if order is not None:
            self.id = str(order.id)
            self.customer = order.zakazchik
            self.date_oc = order.date_of_creation.strftime("%d/%m/%Y")
            self.date_ov = order.date_of_vidacha.strftime("%d/%m/%Y")
            self.description = order.commentary
            self.vidan = order.isVidan
            self.isDone = order.isDone
        else:
            self.id = ""
            self.customer = ""
            self.date_oc = ""
            self.date_ov = ""
            self.description = ""
            self.vidan = False
            self.isDone = False

        self.change_preview_func = change_preview_func
        self.save_button = save_button
        self.vidat_button = None
        self.initialize()

    def set_as_edited(self) -> bool:
        if Editable.set_as_edited(self):
            self.__enable_save_button()

    def initialize(self) -> bool:
        if Frame.initialize(self):

            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_propagate(False)

            self.__add_vidat_button()

            self.edit_button = Button(parental_widget=self, master=self.frame, text="edit",
                                      command=self.edit, font=self.base_font, width=40)
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

            self.__configure_colors()

            return True
        return False

    def edit(self):
        self.edit_button.button.configure(text="conf", command=self.confirm)
        for field in self.get_class_instances(Editable):
            field.edit()
        Editable.edit(self)

    def confirm(self) -> bool:
        is_confirmed = True
        for field in self.get_class_instances(Editable):
            field.confirm()
            if field.is_confirmed is False:
                is_confirmed = False

        if is_confirmed:
            Editable.confirm(self)
            self.edit_button.button.configure(text="edit", command=self.edit)

    def save(self):
        print("Сохраняю ордер")
        editable_list = self.get_class_instances(Editable)
        for widget in editable_list:
            widget.save()

        self.save_button.hide()

        if Editable.save(self):
            self.__assemble_order()

            return True
        return False

    def __configure_colors(self):
        if self.order is not None and self.order.CheckIfDone():
            if self.order.isVidan:
                self.frame.configure(border_color="#7FFF00")
            else:
                self.frame.configure(border_color="#FFA500")
        else:
            self.frame.configure(border_color="#B22222")

    def __assemble_order(self):
        customer = self.customer_field.get()
        date_oc = get_date(self.date_oc_field.get())
        date_ov = get_date(self.date_ov_field.get())

        if self.order is None:
            print("Надо собрать заказ")
            return
        else:
            self.order.zakazchik = customer
            self.order.date_of_creation = date_oc
            self.order.date_of_vidacha = date_ov
            self.order.isVidan = self.vidan
            self.isDone = self.order.CheckIfDone()

        if self.change_preview_func is not None:
            self.change_preview_func(self.order.createPreview())

        self.__add_vidat_button()
        self.__configure_colors()

        app_reference = App()

        app_reference.saveOrder(self.order)

    def __enable_save_button(self):
        if self.save_button is not None:
            self.save_button.show()
            return

    def __add_vidat_button(self):
        if not self.vidan and self.isDone:
            self.vidat_button = Button(parental_widget=self, master=self.frame, text="Выдать",
                                       command=self.__vidat_order, font=self.base_font, width=40)
            self.vidat_button.button.grid(row=0, column=0, padx=3, pady=3, sticky="nw")
            self.add_widget(self.vidat_button)
        else:
            if self.vidat_button is not None:
                self.delete_widget(self.vidat_button)
                self.vidat_button.hide()
            self.vidat_button = None

    def __vidat_order(self):
        self.vidan = True
        self.vidat_button.hide()
        self.set_as_edited()
