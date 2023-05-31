from datetime import date
import tkinter as tk
from typing import List
import customtkinter as ctk

from BaH import App
from BaH.order import Order
from BaH.product import Product
from BaH.step import Step
from Caps.listFuncs import ValidateDate
from GUI.TemplateField import TemplateField
from GUI.ProductField import ProductField


class WindowAdd(ctk.CTkToplevel):
    def __init__(self, MainWindow, app: App, order: Order = None):
        super().__init__(MainWindow)

        self.app = app
        self.MainWindow = MainWindow
        ###
        self.order_parsed = False
        self.zakazchik_text = ""
        self.date_text = ""
        self.order = order
        self.title_text = "Добавление заказа"
        if self.order is not None:
            self.order_parsed = True
            self.title_text = "Редактирование заказа"
            self.zakazchik_text = self.order.zakazchik
            self.date_text = self.order.date_of_vidacha.strftime("%d-%m-%Y")

        self.template_field_list: List[TemplateField] = list()

        self.product_field_list: List[ProductField] = list()
        self.current_product_field: ProductField = None
        ###

        self.init_window_add()

        if self.order is not None:
            self.parse_order()

    @property
    def templates(self) -> List[Product]:
        return self.app.product_templates

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
        self.button_add_product.pack(side=tk.RIGHT, pady=7)

        self.button_choose_from_template = ctk.CTkButton(self.frame_product_panel, text="Шаблоны",
                                                         command=self.choose_from_template)
        self.button_choose_from_template.pack(side=tk.LEFT, pady=7)

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
        self.entry_data_order.bind('<KeyRelease>', self.__edit_data)

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

    def parse_templates(self, templates: List[TemplateField]):
        for template in templates:
            template_field = self.add_template_field(template)
            for step in template.GetSteps():
                self.add_step_field(step, template_field)

    def add_product_field(self, product: Product = None):  # добавление новго продукта и добавление шага в список
        products_count = len(self.product_field_list)
        product_field = ProductField(app=self.app, parental_order=self.order,
                                     personal_number=products_count + 1, add_window=self,
                                     product=product, button_add_step=self.button_add_step)
        if products_count == 0:
            self.current_product_field = product_field

        self.product_field_list.append(product_field)

        return product_field

    def __add_product_from_template(self, template: Product):
        product_field = self.add_product_field(template)
        for step in template.GetSteps():
            self.add_step_field(step, product_field)

    def choose_template(self, template: Product):
        self.exit_template_view()
        self.__add_product_from_template(template)

    def add_template_field(self, template: Product):
        templates_count = len(self.template_field_list)
        template_field = TemplateField(app=self.app, parental_order=self.order,
                                       personal_number=templates_count + 1, add_window=self,
                                       product=template, button_add_step=self.button_add_step)
        if templates_count == 0:
            self.current_product_field = template_field

        self.template_field_list.append(template_field)

        return template_field

    def choose_from_template(self):
        """
        Пока что это пустая кнопка
        Вижу это как добавление в эту колонку всех продуктов из шаблонов
        их надо брать из App
        но это будут не просто продукты, а продукты в которых удалить - удаляет шаблон из
        списка шаблонов ( функцией в App ), а подтвердить - убирает все шаблоны с экрана,
        добавляет обратно все продукты, которые были добавлены пользователем, а также
        тот шаблон, который выбрал пользователь
        """
        self.button_choose_from_template.configure(text="Вернуться", command=self.exit_template_view)

        self.button_add_product.configure(state="disabled")

        self.destroy_products()

        self.parse_templates(self.templates)

        """
        убирает список нынешних товаров с экрана
        выключает кнопку добавить товар
        добавляет список шаблонов
        """
        pass

    def exit_template_view(self):

        """
        Создаём и добавляем шаблон в product_field
        """
        self.destroy_templates()

        for product_field in self.product_field_list:
            product_field.add_product(self.scroll_product, self.scroll_step)
        self.button_choose_from_template.configure(text="Шаблоны", command=self.choose_from_template)

        self.button_add_product.configure(state="normal")
        pass

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
                else:
                    self.button_add_order.configure(state="disabled")

    def destroy_products(self):
        for product_field in self.product_field_list:
            product_field.destroy()

    def destroy_templates(self):
        for template_field in self.template_field_list:
            template_field.destroy()

    def __check_if_all_saved(self):
        check = True
        for product_field in self.product_field_list:
            if product_field.is_saved is False:
                check = False
        return check

    def close_window(self):
        self.frame_order_panel.destroy()
        self.frame_product_panel.destroy()
        self.frame_step_panel.destroy()
        self.frame_common_panel.destroy()
        self.destroy()

        self.MainWindow.add_list_order()
        self.MainWindow.deiconify()

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

    def __edit_data_vidachi_field(self):  # редактирование поля ввода даты, если она введена неверно
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
            self.__edit_data_vidachi_field()
            check = False
        else:
            date = ValidateDate(self.date_text)
            if date is not None:
                self.dat_of_vidacha = date
                self.entry_data_order.configure(fg_color="#f9f9fa", border_color="#61bf0d",
                                                placeholder_text=date.strftime("%d-%m-%Y"))
            else:
                self.__edit_data_vidachi_field()
                check = False

        return check

    def __edit_data(self, event):
        length = len(event.widget.get())
        if length > 10:
            self.entry_data_order.delete(10, length)

    def add_new_order(self):
        """Проходит по каждому продукт-филду, в нём берёт список степ-филдов
           Из этих степ-филдов берёт список шагов, шаги пихает в продукт
           продукты пихает в список, спиоск продуктов в заказ
           заказ сохраняет"""
        if self.order_parsed is True:  # Если мы редактируем
            self.order.ClearProducts()

        for product_field in self.product_field_list:
            product = product_field.product

            for step_field in product_field.step_field_list:
                step = step_field.step
                product.AddStep(step)

            self.order.AddProduct(product)

        if self.order_parsed is False:
            self.app.addNewOrder(self.order)
        else:  # Если мы редактируем
            self.app.saveOrder(self.order)

        self.close_window()
