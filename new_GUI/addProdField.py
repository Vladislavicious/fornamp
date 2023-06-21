from typing import Tuple
from BaH.product import Product
from BaH.step import Step
from Caps.validator import Validator
from new_GUI.addStepField import addStepField
from new_GUI.textField import TextField
from tkabs.button import Button
from tkabs.frame import Frame
from UIadjusters.fontFabric import FontFabric
from tkabs.scroller import Scroller
from uiabs.container import Container
from uiabs.editable import Editable


class addProductField(Frame, Editable):
    def __init__(self, parental_widget: Container, master: any,
                 step_frame: Scroller, click_function,
                 product: Product = None,
                 border_width: int | str | None = 2,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None):
        Frame.__init__(self, parental_widget=parental_widget, master=master,
                       border_width=border_width, bg_color=bg_color,
                       fg_color=fg_color, border_color=border_color)
        Editable.__init__(self, parental_unit=parental_widget)
        self.product = product
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

        self.click_function = click_function
        self.step_frame = step_frame
        self.base_font = FontFabric.get_base_font()

        self.step_fields = list()

        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_columnconfigure(0, weight=1)

            self.edit_button = Button(parental_widget=self, master=self.frame, text="edit",
                                      command=self.edit, font=self.base_font, width=40)
            self.edit_button.button.grid(row=0, column=0, padx=3, pady=3, sticky="ne")
            self.add_widget(self.edit_button)

            self.prod_name_field = TextField(parental_widget=self, master=self.frame,
                                             validation_method=Validator.validate_name, title="Название",
                                             placeholder_text="Введите название", initial_text=self.prod_name)
            self.prod_name_field.frame.grid(row=1, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.prod_name_field)

            self.quantity_field = TextField(parental_widget=self, master=self.frame,
                                            validation_method=lambda value:
                                            Validator.validate_number(string=value, name="Количество"),
                                            title="Количество", placeholder_text="Введите количество, шт.",
                                            initial_text=self.quantity)
            self.quantity_field.frame.grid(row=2, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.quantity_field)

            self.prod_cost_field = TextField(parental_widget=self, master=self.frame,
                                             validation_method=lambda value:
                                             Validator.validate_number(string=value, name="Стоимость производства"),
                                             title="Стоимость производства", initial_text=self.production_cost,
                                             placeholder_text="Введите стоимость, ₽")
            self.prod_cost_field.frame.grid(row=3, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.prod_cost_field)

            self.selling_cost_field = TextField(parental_widget=self, master=self.frame,
                                                validation_method=lambda value:
                                                Validator.validate_number(string=value, name="Стоимость продажи"),
                                                title="Стоимость продажи", placeholder_text="Введите стоимость, ₽",
                                                initial_text=self.selling_cost)
            self.selling_cost_field.frame.grid(row=4, column=0, padx=10, pady=3, sticky="ew")

            self.add_widget(self.selling_cost_field)

            self.description_field = TextField(parental_widget=self, master=self.frame,
                                               validation_method=Validator.validate_description, title="Описание",
                                               placeholder_text="Описание товара",
                                               initial_text=self.description)
            self.description_field.frame.grid(row=5, column=0, padx=10, pady=3, sticky="ew")
            self.add_widget(self.description_field)

            self.__parse_steps()

            self.frame.bind('<Button-1>', command=lambda event: self.click_function(self))

            return True
        return False

    def edit(self):
        self.edit_button.button.configure(text="conf", command=self.confirm)
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
            self.edit_button.button.configure(text="edit", command=self.edit)
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

    def hide_steps(self):
        for step in self.step_fields:
            step.hide()

    def show_steps(self):
        for step in self.step_fields:
            step.show()

    def __assemble_product(self):
        name = self.prod_name_field.get()
        quantity = int(self.quantity_field.get())
        prod_cost = int(self.prod_cost_field.get())
        sell_cost = int(self.selling_cost_field.get())
        description = self.description_field.get()

        steps = list()
        for step_field in self.step_fields:
            steps.append(step_field.step)

        self.product = Product(name=name, selling_cost=sell_cost,
                               quantity=quantity, production_cost=prod_cost,
                               commentary=description)
        self.product.UpdateSteps(steps=steps)

    def __parse_steps(self):
        if self.product is not None:
            steps = self.product.GetSteps()
            for step in steps:
                self.create_step_addition(step=step)
        else:
            # Здесь должно быть добавление одного пустого шага
            self.create_step_addition()

    def create_step_addition(self, step: Step = None):
        step_field = addStepField(parental_widget=self,
                                  master=self.step_frame.scroller, step=step)
        step_field.frame.grid(padx=2, pady=2, sticky="nsew")
        self.add_widget(step_field)
        step_field.edit()
        self.step_fields.append(step_field)


"""
Клик происходит где-то на территории товара, после этого информация о клике переходит в additionFrame,
в котором есть currentProduct. Если этот currentProduct != тому, в котором клик, то
скрываем куррент, открываем новый
"""