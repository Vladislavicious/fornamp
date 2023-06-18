import logging

from os import path
from typing import Tuple
from BaH.product import Product
from new_GUI.addProdField import addProductField
from UIadjusters.fontFabric import FontFabric
from ioconnection.App import App
from new_GUI.addOrderField import AddOrderField
from tkabs.scroller import Scroller
from tkabs.button import Button

from tkabs.frame import Frame
from uiabs.container import Container

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# настройка обработчика и форматировщика для logger
handler = logging.FileHandler(path.abspath(path.curdir)+f"\\logs\\{__name__}.log", mode='w', encoding="utf-8")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)

logger.info(f"Testing the custom logger for module {__name__}...")


class additionFrame(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 go_to_main_function,
                 width: int = 200, height: int = 200,
                 corner_radius: int | str | None = None,
                 border_width: int | str | None = None,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None,
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None,
                 overwrite_preferred_drawing_method: str | None = None, **kwargs):

        super().__init__(parental_widget, master, width,
                         height, corner_radius, border_width,
                         bg_color, fg_color, border_color,
                         background_corner_colors,
                         overwrite_preferred_drawing_method, **kwargs)
        self.back_function = go_to_main_function
        self.base_font = FontFabric.get_base_font()
        self.app = App()

        self.product_fields = list()
        self.current_product = None

        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():
            self.frame.grid_rowconfigure(0, weight=0)
            self.frame.grid_rowconfigure(1, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_columnconfigure(1, weight=3)
            self.frame.grid_columnconfigure(2, weight=3)

            self.back_button = Button(parental_widget=self, master=self.frame,
                                      text="Back", font=self.base_font,
                                      command=self.back_function)
            self.back_button.button.grid(row=0, column=0, pady=2, sticky="w")
            self.add_widget(self.back_button)

            self.save_button = Button(parental_widget=self, master=self.frame,
                                      text="Save", command=self.save_new_order, state="disabled")
            self.save_button.button.grid(row=0, column=0, pady=2, padx=2, sticky="e")
            self.add_widget(self.save_button)

            self.add_prod_button = Button(parental_widget=self, master=self.frame, text="Добавить Товар",
                                          command=self.create_product_addition)
            self.add_prod_button.button.grid(row=0, column=1, pady=2, sticky="w")
            self.add_widget(self.add_prod_button)

            self.template_button = Button(parental_widget=self, master=self.frame, text="Выбрать шаблон",
                                          command=self.choose_from_template, state="disabled")
            self.template_button.button.grid(row=0, column=1, pady=2, sticky="e")
            self.add_widget(self.template_button)

            self.add_step_button = Button(parental_widget=self, master=self.frame, text="Добавить Шаг",
                                          command=self.create_step_addition)
            self.add_step_button.button.grid(row=0, column=2, pady=2)
            self.add_widget(self.add_step_button)

            self.order_frame = Frame(parental_widget=self, master=self.frame,
                                     border_width=2)
            self.order_frame.frame.grid(row=1, column=0, sticky="nsew")
            self.order_frame.frame.grid_columnconfigure(index=0, weight=1)
            self.order_frame.frame.grid_rowconfigure(index=0, weight=1)
            self.add_widget(self.order_frame)

            self.product_frame = Scroller(parental_widget=self, master=self.frame,
                                          border_width=2)
            self.product_frame.scroller.grid(row=1, column=1, ipadx=2, sticky="nsew")
            self.product_frame.scroller.grid_columnconfigure(index=0, weight=1)
            self.add_widget(self.product_frame)

            self.step_frame = Scroller(parental_widget=self, master=self.frame,
                                       border_width=2)
            self.step_frame.scroller.grid(row=1, column=2, ipadx=2, sticky="nsew")
            self.step_frame.scroller.grid_columnconfigure(index=0, weight=1)
            self.add_widget(self.step_frame)

            self.__create_order_addition()
            self.create_product_addition()

            return True
        return False

    def show(self) -> bool:
        if super().show():
            self.save_button.hide()
            return True
        return False

    def __create_order_addition(self):
        self.addOrder = AddOrderField(parental_widget=self.order_frame, master=self.order_frame.frame,
                                      save_button=self.save_button)
        self.addOrder.frame.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
        self.add_widget(self.addOrder)
        self.addOrder.edit()

    def product_click(self, product: addProductField):
        if product is self.current_product:
            return
        self.current_product.hide_steps()
        product.show_steps()
        self.current_product = product

    def choose_from_template(self):
        pass

    def create_product_addition(self, product: Product = None):
        if self.current_product is not None:
            self.current_product.hide_steps()

        self.current_product = addProductField(parental_widget=self.addOrder, master=self.product_frame.scroller,
                                               product=product, step_frame=self.step_frame,
                                               click_function=self.product_click)
        self.current_product.frame.grid(pady=2, sticky="nsew")
        self.addOrder.add_widget(self.current_product)
        self.current_product.edit()
        self.product_fields.append(self.current_product)

    def create_step_addition(self):
        self.current_product.create_step_addition()

    def back_to_main(self):
        # указание мейн фрейму о том, что этот фрейм необходимо удалить
        self.back_function()

    def save_new_order(self):
        self.addOrder.save()

        products = list()
        for product_field in self.product_fields:
            products.append(product_field.product)

        order = self.addOrder.order
        order.addProductList(products)

        # Здесь код сохранения заказа в память и возвращения на мейн экран
        self.back_to_main()
