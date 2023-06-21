from typing import Tuple
from BaH.product import Product
from Caps.validator import Validator
from new_GUI.stepField import stepField
from new_GUI.textField import TextField
from tkabs.button import Button
from tkabs.frame import Frame
from UIadjusters.fontFabric import FontFabric
from uiabs.container import Container
from uiabs.editable import Editable


class ProductField(Frame, Editable):
    def __init__(self, parental_widget: Container, master: any,
                 product: Product, border_width: int | str | None = 2,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = "#B22222"):
        Frame.__init__(self, parental_widget=parental_widget, master=master,
                       border_width=border_width, bg_color=bg_color,
                       fg_color=fg_color, border_color=border_color)
        Editable.__init__(self, parental_unit=parental_widget)
        self.product = product
        self.base_font = FontFabric.get_base_font()
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

        self.step_fields = list()
        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            if self.product.isDone:
                self.item.configure(border_color="#7FFF00")

            self.item.grid_columnconfigure(0, weight=1)

            self.edit_button = Button(parental_widget=self, master=self.item, text="edit",
                                      command=self.edit, font=self.base_font, width=40)
            self.edit_button.item.grid(row=0, column=0, padx=3, pady=3, sticky="ne")
            self.add_widget(self.edit_button)

            self.prod_name_field = TextField(parental_widget=self, master=self.item,
                                             validation_method=Validator.validate_name, title="Название",
                                             placeholder_text="Введите название", initial_text=self.prod_name)
            self.prod_name_field.item.grid(row=1, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.prod_name_field)

            self.quantity_field = TextField(parental_widget=self, master=self.item,
                                            validation_method=lambda value:
                                            Validator.validate_number(string=value, name="Количество"),
                                            title="Количество", placeholder_text="Введите количество, шт.",
                                            initial_text=self.quantity)
            self.quantity_field.item.grid(row=2, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.quantity_field)

            self.prod_cost_field = TextField(parental_widget=self, master=self.item,
                                             validation_method=lambda value:
                                             Validator.validate_number(string=value, name="Стоимость производства"),
                                             title="Стоимость производства", initial_text=self.production_cost,
                                             placeholder_text="Введите стоимость, ₽")
            self.prod_cost_field.item.grid(row=3, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.prod_cost_field)

            self.selling_cost_field = TextField(parental_widget=self, master=self.item,
                                                validation_method=lambda value:
                                                Validator.validate_number(string=value, name="Стоимость продажи"),
                                                title="Стоимость продажи", placeholder_text="Введите стоимость, ₽",
                                                initial_text=self.selling_cost)
            self.selling_cost_field.item.grid(row=4, column=0, padx=10, pady=3, sticky="ew")

            self.add_widget(self.selling_cost_field)

            self.description_field = TextField(parental_widget=self, master=self.item,
                                               validation_method=Validator.validate_description, title="Описание",
                                               placeholder_text="Описание товара",
                                               initial_text=self.description)
            self.description_field.item.grid(row=5, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.description_field)

            self.step_frame = Frame(parental_widget=self, master=self.item)
            self.step_frame.item.grid(row=6, column=0, padx=10, pady=3, sticky="nsew")
            self.step_frame.item.grid_columnconfigure(0, weight=1)
            self.step_frame.item.grid_columnconfigure(1, weight=1)
            self.add_widget(self.step_frame)

            self.__parse_steps()

            return True
        return False

    def edit(self):
        self.edit_button.item.configure(text="conf", command=self.confirm)
        for field in self.get_class_instances(Editable):
            field.edit()
        Editable.edit(self)

    def confirm(self):
        is_confirmed = True

        for field in self.get_class_instances(Editable):
            field.confirm()
            if field.is_confirmed is False:
                is_confirmed = False

        if is_confirmed:
            Editable.confirm(self)
            self.set_as_edited()
            self.edit_button.item.configure(text="edit", command=self.edit)
            return True
        return False

    def save(self):
        print("Сохраняю товар")
        for widget in self.get_class_instances(Editable):
            widget.save()
        if Editable.save(self):

            self.__assemble_product()

            return True
        return False

    def __assemble_product(self):
        name = self.prod_name_field.get()
        quantity = int(self.quantity_field.get())
        prod_cost = int(self.prod_cost_field.get())
        sell_cost = int(self.selling_cost_field.get())
        description = self.description_field.get()

        self.product.name = name
        self.product.quantity = quantity
        self.product.production_cost = prod_cost
        self.product.selling_cost = sell_cost
        self.product.commentary = description

        self.prod_name = name
        self.quantity = quantity
        self.production_cost = prod_cost
        self.selling_cost = sell_cost
        self.description = description

        self.__parse_steps()
        if self.product.CheckIfDone():
            self.item.configure(border_color="#7FFF00")
        else:
            self.item.configure(border_color="#B22222")

    def __parse_steps(self):
        if len(self.step_fields) != 0:
            for step_field in self.step_fields:
                self.delete_widget(step_field)
            self.step_fields.clear()

        steps = self.product.GetSteps()
        length = len(steps)
        for i, step in enumerate(steps):
            step_field = stepField(parental_widget=self, master=self.step_frame.item,
                                   step=step)
            if length % 2 == 1 and i == length - 1:
                step_field.item.grid(row=i // 2, columnspan=2, padx=2, pady=2, sticky="nsew")
            else:
                step_field.item.grid(row=i // 2, column=i % 2, padx=2, pady=2, sticky="nsew")

            self.add_widget(step_field)
            self.step_fields.append(step_field)
