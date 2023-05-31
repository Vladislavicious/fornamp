import tkinter as tk
import customtkinter as ctk

from BaH.order import Order
from BaH.product import Product
from GUI.ProductField import ProductField


class TemplateField(ProductField):
    def __init__(self, app, parental_order: Order, personal_number: int,
                 add_window, button_add_step: ctk.CTkButton, product: Product = None) -> None:
        super().__init__(app, parental_order, personal_number,
                         add_window, button_add_step, product)

    def add_product(self, scroll_product, scroll_step):
        super().add_product(scroll_product, scroll_step)
        """
        изменить функцию при удалении,
        при "применить" сохранять изменения шаблона
        """

    def delete(self):
        super().delete()
        self.app.deleteTemplate(self.product)

    def parse_width_height(self):
        self.height = 435
        self.width = 350

    def add_buttons(self):
        self.button_choose_template = ctk.CTkButton(self.frame_product_field,
                                                    text="Выбрать", command=self.choose)
        self.button_choose_template.pack(side=tk.TOP, padx=10)

        self.button_apply = ctk.CTkButton(self.frame_product_field, text="Применить", command=self.apply)
        self.button_apply.pack(side=tk.LEFT, padx=10)

        self.button_delete = ctk.CTkButton(self.frame_product_field, text="Удалить",
                                           command=self.delete,
                                           fg_color="#d9071c", hover_color="#ad0314")
        self.button_delete.pack(side=tk.RIGHT, padx=10)

    def choose(self):
        self.add_window.choose_template(self.product)

    def edit(self):
        super().edit()
        self.button_add_step.configure(state="disabled")

    def apply_edit(self):
        super().apply_edit()
        self.button_add_step.configure(state="normal")
