import logging

from os import path
from typing import List, Tuple
from BaH.App import App
from BaH.order import OrderPreview
from new_GUI.prodField import ProductField
from new_GUI.ordPreviewField import OrderPreviewField
from new_GUI.orderField import OrderField

from tkabs.frame import Frame
from tkabs.label import Label
from tkabs.scroller import Scroller
from tkabs.toplevel import TopLevel
from tkabs.button import Button

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


class MainWindow(TopLevel):
    def __init__(self, *args, parental_widget,
                 fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, parental_widget=parental_widget,
                         fg_color=fg_color, **kwargs)
        self.name = "MainWindow"
        self.app = App()
        self.current_order = None
        self.__order_previews = list()

        self.menu_opened = False

        self.initialize()

    @property
    def order_previews(self) -> List[OrderPreviewField]:
        return self.__order_previews

    def add_order_preview(self, order_preview: OrderPreviewField):
        self.__order_previews.append(order_preview)

    def clear_order_previews(self):
        self.__order_previews.clear()

    def change_order_preview(self, order_preview: OrderPreview):
        id = order_preview.id

        index, order_preview_field = self.__get_order_preview(id)
        if index == -1:
            logger.error("Попытка парсить несущетсвующий ордер превью")
            return

        order_preview_field.change_order_preview(order_preview)

    def delete_order_preview(self, id: int):
        index, order_preview = self.__get_order_preview(id)
        self.__order_previews.pop(index)

    def __get_order_preview(self, id: int) -> Tuple[int, OrderPreviewField]:
        for i, order_preview in enumerate(self.__order_previews):
            if order_preview.order_preview.id == id:
                return i, order_preview
        return -1, None

    def initialize(self) -> bool:
        if super().initialize():
            logger.debug(f"Инициализирую {self.name}")
            self.title("Main Window")
            self.geometry("1000x600+250+100")
            self.resizable(True, True)
            self.grid_rowconfigure(0, weight=0)
            self.grid_rowconfigure(1, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=6)

            # Настройка тайтлов

            self.menu_frame = Frame(height=25, parental_widget=self, master=self,
                                    border_width=1, border_color="#AF4214")
            self.menu_frame.frame.grid(row=0, column=0, sticky="nsew")
            self.menu_frame.frame.grid_columnconfigure(1, weight=1)

            self.menu_open_button = Button(parental_widget=self.menu_frame,
                                           master=self.menu_frame.frame,
                                           text="Menu", command=self.press, width=40, height=10)
            self.menu_open_button.button.grid(row=0, column=0, pady=3, sticky="w")

            self.menu_label = Label(parental_widget=self.menu_frame, master=self.menu_frame.frame,
                                    text="Меню")
            self.menu_label.label.grid(row=0, column=1, pady=3, sticky="nsew")

            self.menu_frame.add_widget(self.menu_open_button)
            self.menu_frame.add_widget(self.menu_label)

            self.__initialize_menu()

            self.right_title_frame = Frame(height=25, parental_widget=self, master=self,
                                           border_width=1, border_color="#BB1111")
            self.right_title_frame.frame.grid(row=0, column=1, sticky="nsew")
            self.right_title_frame.frame.grid_rowconfigure(0, weight=1)
            self.right_title_frame.frame.grid_columnconfigure(0, weight=1)

            self.add_widget(self.menu_frame)
            self.add_widget(self.right_title_frame)
            # Настройка левого фрейма

            self.left_frame = Frame(parental_widget=self, master=self,
                                    border_width=1, border_color="#AA0A00")

            self.left_frame.frame.grid(row=1, column=0, sticky="nsew")
            self.left_frame.frame.grid_columnconfigure(0, weight=1)
            self.left_frame.frame.grid_rowconfigure(1, weight=1)

            self.search_frame = Frame(parental_widget=self.left_frame,
                                      master=self.left_frame.frame, border_width=1,
                                      border_color="#CF1241")

            self.search_frame.frame.grid_columnconfigure(0, weight=1)
            self.search_frame.frame.grid_rowconfigure(0, weight=1)
            self.search_frame.frame.grid(row=0, column=0, sticky="nsew")
            self.left_frame.add_widget(self.search_frame)

            self.search_label = Label(parental_widget=self.search_frame,
                                      master=self.search_frame.frame, text="Поиск")
            self.search_label.label.grid(row=0, column=0, pady=3)

            self.search_frame.add_widget(self.search_label)

            self.scroller = Scroller(parental_widget=self.left_frame, master=self.left_frame.frame,
                                     border_width=1, border_color="#4E8BC7")
            self.scroller.scroller.grid_columnconfigure(0, weight=1)

            self.scroller.scroller.grid(row=1, column=0, sticky="nsew")

            self.left_frame.add_widget(self.scroller)

            self.__parse_order_previews()

            # Настройка правого фрейма
            self.right_frame = Frame(parental_widget=self, master=self,
                                     border_width=1, border_color="#2E8B57")

            self.right_frame.frame.grid(row=1, column=1, sticky="nsew")

            self.right_frame.frame.grid_columnconfigure(0, weight=0)
            self.right_frame.frame.grid_columnconfigure(1, weight=5)
            self.right_frame.frame.grid_rowconfigure(0, weight=1)

            self.__initialize_open_order()

            ###
            self.add_widget(self.left_frame)
            self.add_widget(self.right_frame)

            self.show()
            return True
        return False

    def __initialize_open_order(self):
        self.order_frame = Frame(parental_widget=self.right_frame, master=self.right_frame.frame,
                                 border_width=1, border_color="#EE8B57")
        self.order_frame.frame.grid_columnconfigure(0, weight=1)
        self.order_frame.frame.grid_rowconfigure(0, weight=1)
        self.order_frame.frame.grid(row=0, column=0, pady=0, sticky="nsew")
        self.right_frame.add_widget(self.order_frame)

        self.product_frame = Scroller(parental_widget=self.right_frame, master=self.right_frame.frame,
                                      border_width=1, border_color="#432B57")
        self.product_frame.scroller.grid(row=0, column=1, pady=0, sticky="nsew")
        self.product_frame.scroller.grid_columnconfigure(0, weight=1)
        self.right_frame.add_widget(self.product_frame)

    def __initialize_menu(self):
        self.menu_window = Frame(self, self)
        self.menu_window.frame.grid(column=0, row=0, rowspan=2, sticky="nsew")
        self.menu_frame.frame.lift()
        self.menu_window.hide()
        self.add_widget(self.menu_window)

    def press(self):
        logger.debug(f"нажатие в {self.name}")
        if not self.menu_opened:
            self.menu_open_button.button.configure(text="Close")
            self.menu_window.show()
            self.menu_window.frame.lift()
            self.menu_frame.frame.lift()
            self.menu_opened = True
        else:
            self.menu_open_button.button.configure(text="Menu")
            self.menu_opened = False
            self.menu_window.hide()

    def destroy(self) -> bool:
        if super().destroy():
            logger.debug(f"Закрываю {self.name}")
            self.parental_widget.destroy()
            return True
        return False

    def __parse_order_previews(self):
        logger.debug("Выводим заказы")
        if self.scroller.items_count == 0:
            for order_preview in self.app.sorted_order_previews:
                order_preview_field = OrderPreviewField(self.scroller, self.scroller.scroller,
                                                        order_preview=order_preview)
                self.scroller.add_widget(order_preview_field)
                order_preview_field.frame.grid(sticky="nsew", pady=2)
                order_preview_field.frame.configure(cursor="hand2")
                order_preview_field.frame.bind('<Button-1>', lambda event,
                                               ID=order_preview.id: self.open_info(ID))
                self.add_order_preview(order_preview_field)

    def open_info(self, id: int):
        logger.debug(f"Нажатие по заказу {id}")
        self.right_frame.delete_widget(self.order_frame)
        self.right_frame.delete_widget(self.product_frame)

        self.__initialize_open_order()

        order = self.app.getOrderByID(id)
        self.current_order = order

        self.save_button = Button(parental_widget=self.right_title_frame, master=self.right_title_frame.frame,
                                  text="Сохранить")
        self.save_button.button.grid(column=0, row=0, pady=3, padx=3, sticky="e")
        self.right_title_frame.add_widget(self.save_button)

        order_field = OrderField(parental_widget=self.order_frame, master=self.order_frame.frame,
                                 order=order, change_preview_func=self.change_order_preview,
                                 save_button=self.save_button)

        self.save_button.button.configure(command=order_field.save)
        self.save_button.hide()

        order_field.frame.grid(row=0, column=0, pady=0, ipady=5, sticky="nsew")
        self.order_frame.add_widget(order_field)

        for product in order.GetProducts():
            product_field = ProductField(parental_widget=order_field, master=self.product_frame.scroller,
                                         product=product)
            product_field.frame.grid(sticky="ew", pady=2, ipadx=1, ipady=5)
            order_field.add_widget(product_field)
