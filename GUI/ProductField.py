import tkinter as tk
from typing import List
import customtkinter as ctk

from BaH.order import Order
from BaH.product import Product
from BaH.step import Step
from GUI.StepField import StepField


class ProductField():  # класс продукта
    def __init__(self, app, parental_order: Order, personal_number: int,
                 add_window, button_add_step: ctk.CTkButton, product: Product = None) -> None:
        self.app = app

        ###
        self.all_steps_are_visible = False

        self.button_add_step = button_add_step
        self.button_add_step.configure(state="disabled")

        self.step_field_list: List[StepField] = list()
        self.current_step_field: StepField = None

        self.parental_order = parental_order
        self.personal_number = personal_number
        self.add_window = add_window
        self.product = product

        self.name_text = ""
        self.selling_cost_text = ""
        self.production_cost_text = ""
        self.quantity_text = ""
        self.commentary_text = ""
        if self.product is not None:
            self.name_text = self.product.name
            self.selling_cost_text = str(self.product.selling_cost)
            self.production_cost_text = str(self.product.production_cost)
            self.quantity_text = str(self.product.quantity)
            self.commentary_text = self.product.commentary
        ###

        self.parse_width_height()

        self.is_saved: bool = False
        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.label_count: ctk.CTkLabel
        self.frame_product_field: ctk.CTkFrame
        self.label_name: ctk.CTkLabel
        self.entry_name: ctk.CTkEntry
        self.label_selling_cost: ctk.CTkLabel
        self.entry_selling_cost: ctk.CTkEntry
        self.label_production_cost: ctk.CTkLabel
        self.entry_production_cost: ctk.CTkEntry
        self.label_commentariy: ctk.CTkLabel
        self.label_quantity: ctk.CTkLabel
        self.entry_quantity: ctk.CTkEntry

        self.button_apply: ctk.CTkButton
        self.button_delete: ctk.CTkButton

        self.add_product(self.add_window.scroll_product, self.add_window.scroll_step)

    def create_step_field(self, step_scroll_panel: ctk.CTkFrame, step: Step = None, step_shown: bool = True):

        steps_count = len(self.step_field_list)

        self.current_step_field = StepField(app=self.app, master=step_scroll_panel,
                                            add_window=self.add_window, parental_product=self.product,
                                            step=step, personal_number=steps_count + 1,
                                            master_product_field=self, step_shown=step_shown)

        self.step_field_list.append(self.current_step_field)

    def add_product(self, scroll_product, scroll_step):  # создание поля нового пустого продукта

        self.scroll_product = scroll_product
        self.scroll_step = scroll_step

        self.label_count = ctk.CTkLabel(scroll_product, text="Товар № " + str(self.personal_number),
                                        font=self.font_)
        self.label_count.pack(anchor=tk.CENTER, pady=5)

        self.frame_product_field = ctk.CTkFrame(scroll_product,
                                                border_width=2, width=self.width, height=self.height)
        self.frame_product_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_product_field.pack_propagate(False)
        self.frame_product_field.bind('<Button-1>', self.reload)

        self.label_name = ctk.CTkLabel(self.frame_product_field, text="Введите название товара", font=self.fontmini)
        self.label_name.pack(anchor=tk.CENTER, pady=5)
        self.label_name.bind('<Button-1>', self.reload)

        self.entry_name = ctk.CTkEntry(self.frame_product_field)
        self.entry_name.insert(0, self.name_text)
        self.entry_name.pack(fill=tk.X, pady=5, padx=5)
        self.entry_name.bind('<Button-1>', self.reload)

        self.label_selling_cost = ctk.CTkLabel(self.frame_product_field, text="Введите стоимость продажи",
                                               font=self.fontmini)
        self.label_selling_cost.pack(anchor=tk.CENTER, pady=5)
        self.label_selling_cost.bind('<Button-1>', self.reload)

        self.entry_selling_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_selling_cost.insert(0, self.selling_cost_text)
        self.entry_selling_cost.pack(fill=tk.X, pady=5, padx=5)
        self.entry_selling_cost.bind('<Button-1>', self.reload)

        self.label_production_cost = ctk.CTkLabel(self.frame_product_field, text="Введите себестоимость товара",
                                                  font=self.fontmini)
        self.label_production_cost.pack(anchor=tk.CENTER, pady=5)
        self.label_production_cost.bind('<Button-1>', self.reload)

        self.entry_production_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_production_cost.insert(0, self.production_cost_text)
        self.entry_production_cost.pack(fill=tk.X, pady=5, padx=5)
        self.entry_production_cost.bind('<Button-1>', self.reload)

        self.label_quantity = ctk.CTkLabel(self.frame_product_field, text="Введите количество товаров",
                                           font=self.fontmini)
        self.label_quantity.pack(anchor=tk.CENTER, pady=5)
        self.label_quantity.bind('<Button-1>', self.reload)

        self.entry_quantity = ctk.CTkEntry(self.frame_product_field)
        self.entry_quantity.insert(0, self.quantity_text)
        self.entry_quantity.pack(fill=tk.X, pady=5, padx=5)
        self.entry_quantity.bind('<Button-1>', self.reload)

        self.label_commentariy = ctk.CTkLabel(self.frame_product_field, text="Введите описание ",
                                              font=self.fontmini)
        self.label_commentariy.pack(anchor=tk.CENTER, pady=5)
        self.label_commentariy.bind('<Button-1>', self.reload)

        self.entry_commentariy = ctk.CTkEntry(self.frame_product_field)
        self.entry_commentariy.insert(0, self.commentary_text)
        self.entry_commentariy.pack(fill=tk.X, pady=5, padx=5)
        self.entry_commentariy.bind('<Button-1>', self.reload)

        self.add_buttons()

    def parse_width_height(self):
        self.height = 415
        self.width = 350

    def add_buttons(self):
        self.button_apply = ctk.CTkButton(self.frame_product_field, text="Применить", command=self.apply)
        self.button_apply.pack(side=tk.LEFT, padx=10)

        self.button_delete = ctk.CTkButton(self.frame_product_field, text="Удалить",
                                           command=self.delete,
                                           fg_color="#d9071c", hover_color="#ad0314")
        self.button_delete.pack(side=tk.RIGHT, padx=10)

    def apply(self):     # кнопка подтверждения продукта и добавление его в список
        self.reload(tk.Event)

        if self.check_field() is True:
            self.product = Product(name=self.name_text, selling_cost=int(self.selling_cost_text),
                                   quantity=int(self.quantity_text),
                                   production_cost=int(self.production_cost_text),
                                   commentary=self.commentary_text, steps=list())

            self.button_apply.configure(fg_color="#2dba52", hover_color="#189e3b",
                                        text="Редактировать", command=self.edit)
            self.edit_state_step_button("disabled")

            self.is_saved = self.__check_if_all_saved()

            self.button_add_step.configure(state="normal")

    def edit(self):
        self.reload(tk.Event)
        self.edit_state_step_button("normal")
        self.button_apply.configure(fg_color="#3b8ed0", hover_color="#36719f",
                                    text="Применить", command=self.apply_edit)
        self.is_saved = False

    def __check_if_all_saved(self):
        check = 1
        if len(self.step_field_list) >= 1:
            for step in self.step_field_list:
                if step == 0:
                    check = 0
        return check

    def delete(self):
        self.add_window.delete_product_field(self)

    def apply_edit(self):
        if self.check_field() is True:

            self.product.name = self.name_text
            self.product.selling_cost = int(self.selling_cost_text)
            self.product.production_cost = int(self.production_cost_text)
            self.product.quantity = int(self.quantity_text)
            self.product.commentary = self.commentary_text

            self.is_saved = self.__check_if_all_saved()

            self.edit_state_step_button("disabled")
            self.button_apply.configure(fg_color="#2dba52", hover_color="#189e3b",
                                        text="Редактировать", command=self.edit)

    def destroy(self):
        for step_field in self.step_field_list:
            step_field.destroy()

        self.label_count.destroy()
        self.frame_product_field.destroy()

    def delete_step_field(self, step_field: StepField):
        index = -1
        for i, step_f in enumerate(self.step_field_list):
            if step_field is step_f:
                index = i
                break
        if index != -1:
            self.step_field_list.pop(index)
            step_field.destroy()

        self.__reenumerate_step_fields()

    def __reenumerate_step_fields(self):
        for i, step_f in enumerate(self.step_field_list):
            step_f.personal_number = i + 1
            step_f.reconfigure_personal_number()

    def reconfigure_personal_number(self):
        self.label_count.configure(text="Товар № " + str(self.personal_number))

    def edit_state_step_button(self, state_aply: str):
        self.entry_name.configure(state=state_aply)
        self.entry_selling_cost.configure(state=state_aply)
        self.entry_production_cost.configure(state=state_aply)
        self.entry_commentariy.configure(state=state_aply)
        self.entry_quantity.configure(state=state_aply)

        self.button_add_step.configure(state=state_aply)

    def check_field(self):   # проверка на введеные поля
        check = True

        if self.entry_name.get() == "":
            self.entry_name.configure(fg_color="#faebeb", border_color="#e64646",
                                      placeholder_text="Введите название", placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        elif len(self.entry_name.get()) > 25:
            self.entry_name.delete(first_index=0, last_index=len(self.entry_name.get()))
            self.entry_name.configure(fg_color="#faebeb", border_color="#e64646",
                                      placeholder_text="Длина названия должна быть не более 25 символов",
                                      placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        else:
            self.name_text = self.entry_name.get()
            self.entry_name.configure(fg_color="#f9f9fa", border_color="#61bf0d", placeholder_text="")

        if not self.entry_selling_cost.get().isdigit():
            self.entry_selling_cost.configure(fg_color="#faebeb", border_color="#e64646",
                                              placeholder_text="Допустим только ввод цифр",
                                              placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        else:
            self.selling_cost_text = self.entry_selling_cost.get()
            self.entry_selling_cost.configure(fg_color="#f9f9fa", border_color="#61bf0d", placeholder_text="")

        if not self.entry_production_cost.get().isdigit():
            self.entry_production_cost.configure(fg_color="#faebeb", border_color="#e64646",
                                                 placeholder_text="Допустим только ввод цифр",
                                                 placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        else:
            self.production_cost_text = self.entry_production_cost.get()
            self.entry_production_cost.configure(fg_color="#f9f9fa", border_color="#61bf0d", placeholder_text="")

        if not self.entry_quantity.get().isdigit():
            self.entry_quantity.configure(fg_color="#faebeb", border_color="#e64646",
                                          placeholder_text="Допустим только ввод цифр",
                                          placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        elif int(self.entry_quantity.get()) > 999 or int(self.entry_quantity.get()) <= 0:
            self.entry_quantity.configure(fg_color="#faebeb", border_color="#e64646",
                                          placeholder_text="Введено недопустимое количество",
                                          placeholder_text_color="#979da2")
            self.entry_quantity.delete(0, len(self.entry_quantity.get()))
            self.label_name.focus()
            check = False
        else:
            self.quantity_text = self.entry_quantity.get()
            self.entry_quantity.configure(fg_color="#f9f9fa", border_color="#61bf0d", placeholder_text="")

        if len(self.entry_commentariy.get()) > 60:
            self.entry_commentariy.delete(first_index=0, last_index=len(self.entry_commentariy.get()))
            self.entry_commentariy.configure(fg_color="#faebeb", border_color="#e64646",
                                             placeholder_text="Длина описания должна быть не более 60 символов",
                                             placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        else:
            self.commentary_text = self.entry_commentariy.get()
            self.entry_commentariy.configure(fg_color="#f9f9fa", border_color="#61bf0d", placeholder_text="")

        if not check:
            self.frame_product_field.configure(border_color="#e64646")
        else:
            self.frame_product_field.configure(border_color="#979da2")

        return check

    def reload(self, event):    # отображение шагов связанных с этим продуктом

        current_product_field = self.add_window.current_product_field

        if self.add_window.current_product_field != self:
            for step_field in current_product_field.step_field_list:
                step_field.destroy()
            current_product_field.all_steps_are_visisble = False

            for step_field in self.step_field_list:
                step_field.add_step(self.scroll_step)

            self.add_window.current_product_field = self

        elif self.all_steps_are_visible is False:
            for step_field in self.step_field_list:
                if not step_field.is_shown:
                    step_field.add_step(self.scroll_step)
            self.all_steps_are_visible = True
