from datetime import date
from typing import Tuple
from Caps.validator import Validator
from BaH.order import Order
from new_GUI.FileInput import FileInput
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


class AddOrderField(Frame, Editable):
    def __init__(self, parental_widget: Container, master: any, save_button,
                 width: int = 250, height: int = 200,
                 border_width: int | str | None = 2,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None):

        Frame.__init__(self, parental_widget=parental_widget, master=master,
                       width=width, height=height,
                       border_width=border_width, bg_color=bg_color,
                       fg_color=fg_color, border_color=border_color)
        Editable.__init__(self, parental_unit=None)

        self.base_font = FontFabric.get_base_font()
        self.order = None

        self.id = str(Order.generate_id())
        self.customer = ""
        self.date_oc = ""
        self.date_ov = ""
        self.description = ""

        self.save_button = save_button
        self.initialize()

    def initialize(self) -> bool:
        if Frame.initialize(self):

            self.item.grid_columnconfigure(0, weight=1)
            self.item.grid_rowconfigure(5, weight=1)
            self.item.grid_propagate(False)

            self.confirm_button = Button(parental_widget=self, master=self.item, text="conf",
                                         command=self.confirm, font=self.base_font, width=40)
            self.confirm_button.item.grid(row=0, column=0, padx=3, pady=3, sticky="ne")
            self.confirm_button.item.grid_remove()
            self.add_widget(self.confirm_button)

            self.id_label = Label(self, self.item, text="id: " + self.id,
                                  font=FontFabric.get_changed_font(weight='bold'))
            self.id_label.item.grid(row=0, column=0, pady=3, sticky="n")
            self.add_widget(self.id_label)

            self.customer_field = TextField(parental_widget=self, master=self.item,
                                            validation_method=Validator.validate_name, title="Заказчик",
                                            placeholder_text="Введите заказчика", initial_text=self.customer)
            self.customer_field.item.grid(row=1, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.customer_field)

            self.date_oc_field = TextField(parental_widget=self, master=self.item,
                                           validation_method=Validator.validate_date, title="Дата создания",
                                           placeholder_text="ДД-ММ-ГГГГ", initial_text=self.date_oc)
            self.date_oc_field.item.grid(row=2, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.date_oc_field)

            self.date_ov_field = TextField(parental_widget=self, master=self.item,
                                           validation_method=Validator.validate_date_ov, title="Дата Выдачи",
                                           placeholder_text="ДД-ММ-ГГГГ", initial_text=self.date_ov)
            self.date_ov_field.item.grid(row=3, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.date_ov_field)

            self.description_field = TextField(parental_widget=self, master=self.item,
                                               validation_method=Validator.validate_description, title="Комментарий",
                                               placeholder_text="Уточнения по заказу",
                                               initial_text=self.description)
            self.description_field.item.grid(row=4, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.description_field)

            self.file_input = FileInput(parental_widget=self, master=self.item,
                                        purpose_name="Прикрепить фото к заказу",
                                        border_width=1)
            self.file_input.item.grid(row=5, column=0, padx=10, pady=3, sticky="nsew")
            self.add_widget(self.file_input)

            return True
        return False

    def edit(self):
        self.confirm_button.show()

        self.save_button.item.configure(state="disabled")
        self.save_button.hide()

        self.confirm_button.item.configure(text="conf", command=self.confirm)

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
            self.__enable_save_button()
            self.confirm_button.item.configure(text="edit", command=self.edit)

    def save(self):
        print("Сохраняю ордер")
        editable_list = self.get_class_instances(Editable)
        for widget in editable_list:
            widget.save()

        self.save_button.button.configure(state="disabled")
        self.save_button.hide()

        if Editable.save(self):
            self.__assemble_order()
            self.__parse_photos()
            return True
        return False

    def __parse_photos(self):
        for photo_path in self.file_input.contained_paths:
            print(photo_path)

    def __assemble_order(self):
        customer = self.customer_field.get()
        description = self.description_field.get()
        date_oc = get_date(self.date_oc_field.get())
        date_ov = get_date(self.date_ov_field.get())

        self.order = Order(int(self.id), zakazchik=customer,
                           date_of_creation=date_oc, date_of_vidacha=date_ov,
                           commentary=description)

    def __enable_save_button(self):
        if self.save_button is not None:
            self.save_button.button.configure(state="normal")
            self.save_button.show()
            return
