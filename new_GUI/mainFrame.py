import logging

from os import path
from typing import List, Tuple
from BaH.order import OrderPreview
from new_GUI.menu import Menu
from new_GUI.prodField import ProductField
from UIadjusters.fontFabric import FontFabric
from ioconnection.App import App
from new_GUI.ordPreviewField import OrderPreviewField
from new_GUI.orderField import OrderField
from tkabs.scroller import Scroller
from tkabs.button import Button

from tkabs.frame import Frame
from tkabs.label import Label
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


class mainFrame(Frame):
    def __init__(self, parental_widget: Container, master: any,
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

        self.current_order = None
        self.__order_previews = list()
        self.base_font = FontFabric.get_base_font()
        self.app = App()
        self.initialize()

    @property
    def order_previews(self) -> List[OrderPreviewField]:
        return self.__order_previews

    def add_order_preview_field(self, order_preview: OrderPreviewField):
        self.__order_previews.append(order_preview)

    def clear_order_previews(self):
        self.__order_previews.clear()

    def change_order_preview(self, order_preview: OrderPreview):
        id = order_preview.id

        index, order_preview_field = self.__get_order_preview(id)
        if index == -1:
            logger.error("Попытка парсить несуществующий ордер превью")
            return

        order_preview_field.change_order_preview(order_preview)

    def delete_order_preview(self, id: int):
        index, order_preview = self.__get_order_preview(id)
        self.__order_previews.pop(index)

        order_preview.hide()
        self.scroller.delete_widget(order_preview)
        del order_preview

    def __get_order_preview(self, id: int) -> Tuple[int, OrderPreviewField]:
        for i, order_preview in enumerate(self.__order_previews):
            if order_preview.order_preview.id == id:
                return i, order_preview
        return -1, None

    def initialize(self) -> bool:
        if super().initialize():
            self.item.grid_rowconfigure(0, weight=0)
            self.item.grid_rowconfigure(1, weight=1)
            self.item.grid_columnconfigure(0, weight=1)
            self.item.grid_columnconfigure(1, weight=6)

            # Настройка тайтлов

            self.right_title_frame = Frame(height=25, parental_widget=self, master=self.item,
                                           border_width=1, border_color="#BB1111")
            self.right_title_frame.item.grid(row=0, column=1, sticky="nsew")
            self.right_title_frame.item.grid_rowconfigure(0, weight=1)
            self.right_title_frame.item.grid_columnconfigure(0, weight=1)

            self.add_widget(self.right_title_frame)
            # Настройка левого фрейма

            self.left_frame = Frame(parental_widget=self, master=self.item,
                                    border_width=1, border_color="#AA0A00")

            self.left_frame.item.grid(row=1, column=0, sticky="nsew")
            self.left_frame.item.grid_columnconfigure(0, weight=1)
            self.left_frame.item.grid_rowconfigure(1, weight=1)

            self.search_frame = Frame(parental_widget=self.left_frame,
                                      master=self.left_frame.item, border_width=1,
                                      border_color="#CF1241")

            self.search_frame.item.grid_columnconfigure(0, weight=1)
            self.search_frame.item.grid_rowconfigure(0, weight=1)
            self.search_frame.item.grid(row=0, column=0, sticky="nsew")
            self.left_frame.add_widget(self.search_frame)

            self.search_label = Label(parental_widget=self.search_frame,
                                      master=self.search_frame.item, text="Поиск")
            self.search_label.item.grid(row=0, column=0, pady=3)

            self.search_frame.add_widget(self.search_label)

            self.scroller = Scroller(parental_widget=self.left_frame, master=self.left_frame.item,
                                     border_width=1, border_color="#4E8BC7")
            self.scroller.item.grid_columnconfigure(0, weight=1)

            self.scroller.item.grid(row=1, column=0, sticky="nsew")

            self.left_frame.add_widget(self.scroller)

            self.__parse_order_previews()

            # Настройка правого фрейма
            self.right_frame = Frame(parental_widget=self, master=self.item,
                                     border_width=1, border_color="#2E8B57")

            self.right_frame.item.grid(row=1, column=1, sticky="nsew")

            self.right_frame.item.grid_columnconfigure(0, weight=0)
            self.right_frame.item.grid_columnconfigure(1, weight=5)
            self.right_frame.item.grid_rowconfigure(0, weight=1)

            self.__initialize_open_order()

            ###
            self.add_widget(self.left_frame)
            self.add_widget(self.right_frame)

            self.show()

            self.save_button = None
            self.delete_button = None
            return True
        return False

    def insert_menu(self, menu: Menu):
        self.menu_frame = menu
        menu.change_open_function(self.open_menu)
        menu.change_close_function(self.close_menu)
        self.menu_frame.item.grid(row=0, column=0, sticky="nsew")

    def open_menu(self):
        self.menu_frame.item.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.menu_frame.item.lift()

    def close_menu(self):
        self.menu_frame.item.grid(row=0, column=0, rowspan=1, sticky="nsew")

    def __initialize_open_order(self):
        self.order_frame = Frame(parental_widget=self.right_frame, master=self.right_frame.item,
                                 border_width=1, border_color="#EE8B57")
        self.order_frame.item.grid_columnconfigure(0, weight=1)
        self.order_frame.item.grid_rowconfigure(0, weight=1)
        self.order_frame.item.grid(row=0, column=0, pady=0, sticky="nsew")
        self.right_frame.add_widget(self.order_frame)

        self.product_frame = Scroller(parental_widget=self.right_frame, master=self.right_frame.item,
                                      border_width=1, border_color="#432B57")
        self.product_frame.item.grid(row=0, column=1, pady=0, sticky="nsew")
        self.product_frame.item.grid_columnconfigure(0, weight=1)
        self.right_frame.add_widget(self.product_frame)

    def __parse_order_previews(self):
        logger.debug("Выводим заказы")
        if self.scroller.items_count == 0:
            for order_preview in self.app.sorted_order_previews:
                self.add_order_preview(order_preview)

    def add_order_preview(self, order_preview: OrderPreview):
        order_preview_field = OrderPreviewField(self.scroller, self.scroller.item,
                                                order_preview=order_preview)

        index = len(self.order_previews)
        order_preview_field.item.grid(row=index, column=0, pady=2, sticky="nsew")
        order_preview_field.item.configure(cursor="hand2")
        order_preview_field.item.bind('<Button-1>', lambda event,
                                      ID=order_preview.id: self.open_info(ID))
        self.scroller.add_widget(order_preview_field)
        self.add_order_preview_field(order_preview_field)

    def __clear_right_frame(self):
        self.right_frame.delete_widget(self.order_frame)
        self.right_frame.delete_widget(self.product_frame)

        if self.delete_button is not None:
            self.right_title_frame.delete_widget(self.delete_button)
            del self.delete_button
            self.delete_button = None

        if self.save_button is not None:
            self.right_title_frame.delete_widget(self.save_button)
            del self.save_button
            self.save_button = None

        self.__initialize_open_order()

    def __delete_order(self, id: int, order_field: OrderField):
        order_field.hide()
        self.order_frame.delete_widget(order_field)

        self.__clear_right_frame()
        self.delete_order_preview(id)
        self.app.deleteOrderByID(id)

    def __delete_product(self, order_field: OrderField, product_field: ProductField):
        product_field.hide()
        order_field.delete_widget(product_field)

        order = order_field.order
        product = product_field.product
        order.DeleteProduct(product.name)

        del product_field

    def open_info(self, id: int):
        logger.debug(f"Нажатие по заказу {id}")
        self.__clear_right_frame()

        order = self.app.getOrderByID(id)
        self.current_order = order

        self.save_button = Button(parental_widget=self.right_title_frame, master=self.right_title_frame.item,
                                  text="Сохранить", font=self.base_font, width=40, fg_color="#FFFF99",
                                  hover_color="#000000", text_color="#765432")
        self.save_button.item.grid(row=0, column=1, pady=3, padx=3, sticky="e")
        self.right_title_frame.add_widget(self.save_button)

        self.edit_button = Button(parental_widget=self.right_title_frame, master=self.right_title_frame.item,
                                  text="Редактировать", font=self.base_font, width=40)
        self.edit_button.item.grid(row=0, column=2, padx=3, pady=3, sticky="e")
        self.add_widget(self.edit_button)

        order_field = OrderField(parental_widget=self.order_frame, master=self.order_frame.item,
                                 order=order, change_preview_func=self.change_order_preview,
                                 save_button=self.save_button, edit_button=self.edit_button)

        self.save_button.item.configure(command=order_field.save, state="disabled")
        self.save_button.hide()

        self.edit_button.item.configure(command=order_field.edit)

        order_field.item.grid(row=0, column=0, pady=0, ipady=5, sticky="nsew")
        self.order_frame.add_widget(order_field)

        for product in order.GetProducts():
            product_field = ProductField(parental_widget=order_field, master=self.product_frame.item,
                                         product=product)
            product_field.insert_deletion_method(func=lambda product_field:
                                                 self.__delete_product(order_field=order_field,
                                                                       product_field=product_field))
            product_field.item.grid(sticky="ew", pady=2, ipadx=1, ipady=5)
            order_field.add_widget(product_field)

        self.delete_button = Button(parental_widget=self.right_title_frame, master=self.right_title_frame.item,
                                    text="Удалить", fg_color="#AA0A00",
                                    hover_color="#AA0AE0", font=self.base_font,
                                    command=lambda: self.__delete_order(order.id, order_field))

        self.delete_button.item.grid(column=0, row=0, pady=3, padx=3, sticky="e")
        self.right_title_frame.add_widget(self.delete_button)

        order_field.show()
