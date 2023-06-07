from typing import Tuple
from BaH.product import Product
from new_GUI.stepField import stepField
from new_GUI.textField import TextField
from tkabs.button import Button
from tkabs.frame import Frame
from tkabs.fontFabric import FontFabric
from uiabs.container import Container


def is_valid_string(s):
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя.,:/" ')
    return all(c in allowed_chars for c in s)


def validate_name(string: str = "") -> Tuple[bool, str]:
    """Проверяет строку на соответствие параметрам"""
    length = len(string)
    if length < 2:
        return False, "Название слишком короткое"
    if length > 32:
        return False, "Название слишком длинное"
    if not is_valid_string(string.lower()):
        return False, "Содержит неподобающие символы"
    return True, ""


def validate_number(string: str = "", name: str = "Количество") -> Tuple[bool, str]:
    if string.isdecimal():
        if int(string) <= 0:
            return False, f"{name} меньше 1"
        return True, ""
    elif len(string) == 0:
        return False, f"Введите {name}"
    return False, "Введите число"


def validate_description(string: str = "") -> Tuple[bool, str]:
    if len(string) > 256:
        return False, "Слишком длинное описание"
    if is_valid_string(string.lower()):
        return True, ""
    return False, "Содержит неподобающие символы"


class ProductField(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 product: Product, border_width: int | str | None = 2,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = "#B22222"):
        super().__init__(parental_widget=parental_widget, master=master,
                         border_width=border_width, bg_color=bg_color,
                         fg_color=fg_color, border_color=border_color)
        self.product = product
        self.base_font = FontFabric.get_base_font()
        self.is_edited = False
        # все характеристики product будут в виде строк
        if product is not None:
            self.prod_name = product.name
            self.quantity = str(product.quantity)
            self.production_cost = str(product.production_cost)
            self.selling_cost = str(product.selling_cost)
            self.description = product.commentary
        else:
            self.prod_name = ""
            self.quantity = ""
            self.production_cost = ""
            self.selling_cost = ""
            self.description = ""

        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            if self.product.isDone:
                self.frame.configure(border_color="#7FFF00")

            self.frame.grid_columnconfigure(0, weight=1)

            self.edit_button = Button(parental_widget=self, master=self.frame, text="edit",
                                      command=self.edit_all_fields, font=self.base_font, width=40)
            self.edit_button.button.grid(row=0, column=0, padx=3, pady=3, sticky="ne")
            self.add_widget(self.edit_button)

            self.prod_name_field = TextField(parental_widget=self, master=self.frame,
                                             validation_method=validate_name, title="Название",
                                             placeholder_text="Введите название", initial_text=self.prod_name)
            self.prod_name_field.frame.grid(row=1, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.prod_name_field)

            self.quantity_field = TextField(parental_widget=self, master=self.frame,
                                            validation_method=lambda value:
                                            validate_number(string=value, name="Количество"),
                                            title="Количество", placeholder_text="Введите количество, шт.",
                                            initial_text=self.quantity)
            self.quantity_field.frame.grid(row=2, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.quantity_field)

            self.prod_cost_field = TextField(parental_widget=self, master=self.frame,
                                             validation_method=lambda value:
                                             validate_number(string=value, name="Стоимость производства"),
                                             title="Стоимость производства", initial_text=self.production_cost,
                                             placeholder_text="Введите стоимость, ₽")
            self.prod_cost_field.frame.grid(row=3, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.prod_cost_field)

            self.selling_cost_field = TextField(parental_widget=self, master=self.frame,
                                                validation_method=lambda value:
                                                validate_number(string=value, name="Стоимость продажи"),
                                                title="Стоимость продажи", placeholder_text="Введите стоимость, ₽",
                                                initial_text=self.selling_cost)
            self.selling_cost_field.frame.grid(row=4, column=0, padx=10, pady=3, sticky="ew")

            self.add_widget(self.selling_cost_field)

            self.description_field = TextField(parental_widget=self, master=self.frame,
                                               validation_method=validate_description, title="Описание",
                                               placeholder_text="Описание товара",
                                               initial_text=self.description)
            self.description_field.frame.grid(row=5, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.description_field)

            self.step_frame = Frame(parental_widget=self, master=self.frame)
            self.step_frame.frame.grid(row=6, column=0, padx=10, pady=3, sticky="nsew")
            self.step_frame.frame.grid_columnconfigure(0, weight=1)
            self.step_frame.frame.grid_columnconfigure(1, weight=1)
            self.add_widget(self.step_frame)

            self.__parse_steps()

            self.fields = [self.prod_name_field, self.quantity_field,
                           self.selling_cost_field, self.prod_cost_field, self.description_field]

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

    def __parse_steps(self):
        steps = self.product.GetSteps()
        length = len(steps)
        for i, step in enumerate(steps):
            step_field = stepField(parental_widget=self.step_frame, master=self.step_frame.frame,
                                   step=step)
            if length % 2 == 1 and i == length - 1:
                step_field.frame.grid(row=i // 2, columnspan=2, padx=2, pady=2, sticky="nsew")
            else:
                step_field.frame.grid(row=i // 2, column=i % 2, padx=2, pady=2, sticky="nsew")
            self.step_frame.add_widget(step_field)
