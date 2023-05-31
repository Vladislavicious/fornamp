from datetime import date
import tkinter as tk
from typing import List
import customtkinter as ctk

from BaH import App
from BaH.order import Order
from BaH.product import Product
from BaH.step import Step
from Caps.listFuncs import ValidateDate
from GUI.ProductField import ProductField


class WindowAdd(ctk.CTkToplevel):
    def __init__(self, MainWindow, app: App, order: Order = None):
        super().__init__(MainWindow)

        self.app = app
        self.MainWindow = MainWindow
        ###
        self.zakazchik_text = ""
        self.date_text = ""
        self.order = order
        self.title_text = "Добавление заказа"
        if self.order is not None:
            self.title_text = "Редактирование заказа"
            self.zakazchik_text = self.order.zakazchik
            self.date_text = self.order.date_of_vidacha.strftime("%d-%m-%Y")

        self.product_field_list: List[ProductField] = list()
        self.current_product_field: ProductField = None
        ###

        self.init_window_add()

        if self.order is not None:
            self.parse_order()

    def init_window_add(self) -> None:
        self.geometry("1000x600+250+100")
        self.resizable(False, False)

        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window())

        self.panel_add()
        self.add_area_order()
        self.add_area_product()
        self.add_area_step()

        self.MainWindow.withdraw()

    def panel_add(self):    # панель добавления шагов, продуктов, заказа
        self.topbar = ctk.CTkFrame(master=self, height=50, border_width=3, fg_color="#FFFFFF")
        self.title_name_label = ctk.CTkLabel(self.topbar, text=self.title_text, fg_color="transparent",
                                             font=ctk.CTkFont(family="Arial", size=24))
        self.title_name_label.place(relx=0.37, rely=0.2)

        self.topbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.topbar.pack_propagate(False)

        self.frame_common_panel = ctk.CTkFrame(self, border_width=0, width=1000,
                                               corner_radius=0, height=40)
        self.frame_common_panel.pack(anchor=tk.W, side=tk.TOP)
        self.frame_common_panel.pack_propagate(False)

        self.frame_order_panel = ctk.CTkFrame(self.frame_common_panel, border_width=1,
                                              width=250, corner_radius=0, height=40)
        self.frame_product_panel = ctk.CTkFrame(self.frame_common_panel, border_width=1,
                                                width=375, corner_radius=0, height=40)
        self.frame_step_panel = ctk.CTkFrame(self.frame_common_panel, border_width=1,
                                             width=375, corner_radius=0, height=40)

        self.frame_order_panel.pack(side=tk.LEFT)
        self.frame_order_panel.pack_propagate(False)

        self.frame_product_panel.pack(side=tk.LEFT)
        self.frame_product_panel.pack_propagate(False)

        self.frame_step_panel.pack(side=tk.LEFT)
        self.frame_step_panel.pack_propagate(False)

        self.button_add_order = ctk.CTkButton(self.frame_order_panel, text="Добавить заказ",
                                              command=self.add_new_order, state="disabled")
        self.button_add_order.pack(side=tk.TOP, pady=7)

        self.button_add_product = ctk.CTkButton(self.frame_product_panel, text="Добавить товар",
                                                command=self.add_product_field)
        self.button_add_product.pack(side=tk.TOP, pady=7)

        self.button_add_step = ctk.CTkButton(self.frame_step_panel, text="Добавить шаг",
                                             command=self.add_step_field)
        self.button_add_step.pack(side=tk.TOP, pady=7)

        self.button_add_product.configure(state="disabled")
        self.button_add_step.configure(state="disabled")

    def add_area_order(self):   # создание области в которой создается заказ
        self.frame_order = ctk.CTkFrame(self, border_width=1, width=250, height=560, corner_radius=0)

        self.add_order_field()
        self.frame_order.pack(side=tk.LEFT)
        self.frame_order.pack_propagate(False)

    def add_area_product(self):     # создание области в которой создается продукт
        self.frame_product = ctk.CTkFrame(master=self, border_width=0, width=375, height=560)
        self.frame_product.pack(side=tk.LEFT)
        self.frame_product.pack_propagate(False)

        self.scroll_product = ctk.CTkScrollableFrame(master=self.frame_product, height=560)
        self.scroll_product.pack(padx=5, pady=5, fill=tk.X)

    def add_area_step(self):    # создание области в которой создается шаг
        self.frame_step = ctk.CTkFrame(master=self, border_width=0, width=375, height=560)
        self.frame_step.pack(side=tk.LEFT)
        self.frame_step.pack_propagate(False)

        self.scroll_step = ctk.CTkScrollableFrame(master=self.frame_step, height=560)
        self.scroll_step.pack(padx=5, pady=5, fill=tk.X)

    def add_order_field(self):  # поля ввода для создания заказа и конпка выхода в главное меню
        frame_order_field = ctk.CTkFrame(self.frame_order, width=250, height=560, corner_radius=0)
        frame_order_field.pack(side=tk.TOP, padx=1, pady=1)
        frame_order_field.pack_propagate(False)

        self.label_date = ctk.CTkLabel(master=frame_order_field,
                                       text="Введите дату выдачи", font=self.font_)
        self.label_date.pack(anchor=tk.CENTER, pady=5)

        self.entry_data_order = ctk.CTkEntry(master=frame_order_field,
                                             placeholder_text="ДД-ММ-ГГГГ")
        if self.date_text != "":
            self.entry_data_order.insert(0, self.date_text)

        self.entry_data_order.pack(fill=tk.X, pady=5)
        self.entry_data_order.bind('<KeyRelease>', self.edit_data)

        self.label_zakazchik = ctk.CTkLabel(master=frame_order_field,
                                            text="Введите заказчика", font=self.font_)
        self.label_zakazchik.pack(anchor=tk.CENTER, pady=5)

        self.entry_zakazchik_order = ctk.CTkEntry(frame_order_field)
        self.entry_zakazchik_order.insert(0, self.zakazchik_text)
        self.entry_zakazchik_order.pack(fill=tk.X, pady=5)

        self.label_error = ctk.CTkLabel(master=frame_order_field, text="",
                                        font=self.font_, text_color="#e64646")
        self.label_error.pack(anchor=tk.CENTER, pady=5)

        self.button_close = ctk.CTkButton(master=frame_order_field, text="Закрыть",
                                          command=self.close_window, width=40, height=10)
        self.button_close.pack(side=tk.BOTTOM, anchor=tk.E)

        self.button_confirm = ctk.CTkButton(master=frame_order_field, text="Подтвердить",
                                            command=self.confirm_order, width=40, height=10)
        self.button_confirm.pack(side=tk.BOTTOM, anchor=tk.E)

    def add_step_field(self, step: Step = None, product_field=None):   # добавление новго шага
        if product_field is None:
            self.current_product_field.create_step_field(self.scroll_step, step, step_shown=True)
        else:  # В случае, если мы откуда-то берём уже готовые товары ( редактируем или шаблоны )
            product_field.create_step_field(self.scroll_step, step, step_shown=False)

    def parse_order(self):
        for product in self.order.GetProducts():
            product_field = self.add_product_field(product)
            for step in product.GetSteps():
                self.add_step_field(step, product_field)

    def add_product_field(self, product: Product = None):  # добавление новго продукта и добавление шага в список
        products_count = len(self.product_field_list)
        product_field = ProductField(app=self.app, parental_order=self.order,
                                     personal_number=products_count + 1, add_window=self,
                                     product=product, button_add_step=self.button_add_step)
        if products_count == 0:
            self.current_product_field = product_field

        self.product_field_list.append(product_field)

        return product_field

    def confirm_order(self):
        if self.check_order_field():
            if self.order is None:
                self.order = Order(id=0, zakazchik=self.zakazchik_text, date_of_creation=date.today(),
                                   date_of_vidacha=self.dat_of_vidacha, products=list())
            else:
                self.order.zakazchik = self.zakazchik_text
                self.order.date_of_creation = date.today()
                self.order.date_of_vidacha = self.dat_of_vidacha
            self.button_add_product.configure(state="normal")
            self.button_add_step.configure(state="normal")

            if len(self.product_field_list) >= 1:
                if self.__check_if_all_saved() is True:
                    self.button_add_order.configure(state="normal")

    def __check_if_all_saved(self):
        check = True
        for product_field in self.product_field_list:
            if product_field.is_saved is False:
                check = False
        return check

    def close_window(self):
        for product in self.product_field_list:
            product.destroy()
        self.product_field_list.clear()

        self.MainWindow.add_list_order()
        self.MainWindow.deiconify()
        self.destroy()

    def delete_product_field(self, product_field: ProductField):
        index = -1
        for i, prod_f in enumerate(self.product_field_list):
            if product_field is prod_f:
                index = i
                break
        if index != -1:
            self.product_field_list.pop(index)
            product_field.destroy()

        self.__reenumerate_product_fields()
        self.button_add_step.configure(state="disabled")

    def __reenumerate_product_fields(self):
        for i, prod_f in enumerate(self.product_field_list):
            prod_f.personal_number = i + 1
            prod_f.reconfigure_personal_number()

    def edit_data_vidachi_field(self):  # редактирование поля ввода даты, если она введена неверно
        self.entry_data_order.delete(first_index=0, last_index=len(self.entry_data_order.get()))
        self.entry_data_order.configure(fg_color="#faebeb", border_color="#e64646",
                                        placeholder_text="ДД-ММ-ГГГГ", placeholder_text_color="#979da2")
        self.label_date.focus()

    def check_order_field(self):
        check = True
        self.zakazchik_text = self.entry_zakazchik_order.get()
        self.date_text = self.entry_data_order.get()
        if self.zakazchik_text == "":
            self.entry_zakazchik_order.configure(fg_color="#faebeb", border_color="#e64646",
                                                 placeholder_text="Заполните это поле",
                                                 placeholder_text_color="#979da2")
            self.label_zakazchik.focus()
            check = False
        elif len(self.entry_zakazchik_order.get()) >= 25:
            self.entry_zakazchik_order.configure(fg_color="#faebeb", border_color="#e64646")
            self.label_error.configure(text="Введите не больше 25 символов")
            check = False
        else:
            self.entry_zakazchik_order.configure(fg_color="#f9f9fa", border_color="#61bf0d", placeholder_text="")

        if len(self.date_text) != 10:
            self.edit_data_vidachi_field()
            check = False
        else:
            date = ValidateDate(self.date_text)
            if date is not None:
                self.dat_of_vidacha = date
                self.entry_data_order.configure(fg_color="#f9f9fa", border_color="#61bf0d",
                                                placeholder_text=date.strftime("%d-%m-%Y"))
            else:
                self.edit_data_vidachi_field()
                check = False

        return check

    def edit_data(self, event):
        length = len(event.widget.get())
        if length > 10:
            self.entry_data_order.delete(10, length)

    def add_new_order(self):
        """Проходит по каждому продукт-филду, в нём берёт список степ-филдов
           Из этих степ-филдов берёт список шагов, шаги пихает в продукт
           продукты пихает в список, спиоск продуктов в заказ
           заказ сохраняет"""
        for product_field in self.product_field_list:
            product = product_field.product

            for step_field in product_field.step_field_list:
                step = step_field.step
                product.AddStep(step)

            self.order.AddProduct(product)

        self.app.addNewOrder(self.order)

        self.close_window()
