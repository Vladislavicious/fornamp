import os
import shutil
import pickle
from typing import List, Tuple
from cryptography.fernet import Fernet

from BaH.order import Order
from BaH.order import OrderPreview
from BaH.product import Product
from BaH.uh import UserHandler
from Caps.listFuncs import createHTMLfromList
from Caps.cm import ConfigManager


class FileManager():
    """
    Класс для работы с файлами приложения.
    Создаётся при открытии приложения. Содержит конфиг менеджера. Внутри также содержит
    user_handler'а, с помощью которого делаются все
    операции над пользователями в приложении
    """
    def __init__(self) -> None:
        self.config_manager = ConfigManager.standard_cm()

        self.__parseOrderFilenames()

        self.user_handler = UserHandler(self.key, self.accounts_filepath)

    def clearOrderFilenames(self):
        self.ordered_filenames.clear()

    @property
    def orders_dir_path(self) -> str:
        return self.config_manager.orders_dir_path

    @property
    def statistics_dir_path(self) -> str:
        return self.config_manager.statistics_dir_path

    @property
    def accounts_filepath(self) -> str:
        return self.config_manager.accounts_filepath

    @property
    def key(self) -> bytes:
        return self.config_manager.key

    def changeConfig(self, orders_dir_path: str = None, statistics_dir_path: str = None,
                     accounts_filepath: str = None) -> bool:
        """Интерфейс для изменения элементов конфига пользователя
           позволяет изменять места хранения заказов, статистик и аккаунтов
           Возвращает True, если хоть что-то сохранил"""
        need_to_save = False
        if orders_dir_path is not None:
            if os.path.isdir(orders_dir_path):
                self.config_manager.orders_dir_path = orders_dir_path
                need_to_save = True

        if statistics_dir_path is not None:
            if os.path.isdir(statistics_dir_path):
                self.config_manager.statistics_dir_path = statistics_dir_path
                need_to_save = True

        if accounts_filepath is not None:
            if os.path.isdir(accounts_filepath):
                self.config_manager.accounts_filepath = accounts_filepath
                need_to_save = True
        if need_to_save:
            self.config_manager.save()

        return need_to_save

    def parseOrderPreviews(self) -> List[OrderPreview]:
        order_preview_list = list()
        try:
            with open(self.orders_dir_path + "\\orderPreviews.b", "rb") as file:
                text = file.read()
                order_preview_list = pickle.loads(text)
        except FileNotFoundError:

            order_list = self.getOrderList()
            for order in order_list:
                order_preview = order.createPreview()
                order_preview_list.append(order_preview)

            self.saveOrderPreviewList(order_preview_list)

        return order_preview_list

    def parseTemplates(self) -> List[Product]:
        """Считывает файл с шаблонами из папки с заказами"""
        templates = list()
        try:
            with open(self.orders_dir_path + "\\Templates.b", "rb") as file:
                text = file.read()
                templates = pickle.loads(text)
        except FileNotFoundError:
            with open(self.orders_dir_path + "\\Templates.b", "wb") as file:
                pass
        except EOFError:
            print("Файл с шаблонами пуст")
            pass

        return templates

    def saveTemplates(self, templates: List[Product]):
        with open(self.orders_dir_path + "\\Templates.b", "wb") as file:
            file.write(pickle.dumps(templates))

    def saveOrderPreviewList(self, order_preview_list: List[OrderPreview]):
        with open(self.orders_dir_path + "\\orderPreviews.b", "wb") as file:
            file.write(pickle.dumps(order_preview_list))

    def getOrderList(self) -> List[Order]:
        """Возвращает список всех заказов"""
        order_list = list()
        for key in self.ordered_filenames.keys():
            order_list.append(self.getOrderByID(key))

        return order_list

    def CreateStatusHTML(self) -> Tuple[List[Order], str]:
        orders = self.getOrderList()

        filepath = createHTMLfromList(orders, self.orders_dir_path + "\\otchet")

        return orders, filepath

    def __parseOrderFilenames(self):
        os.makedirs(self.orders_dir_path, exist_ok=True)

        order_filenames = os.listdir(self.orders_dir_path)

        order_filenames = [order for order in order_filenames if not order.endswith(".b")]

        self.ordered_filenames = self.__getOrderStatusPairs(order_filenames)

    def __getOrderStatusPairs(self, order_filenames):
        """Возвращает словарь Айди заказа: статус"""
        orders = dict()
        for ord_file in order_filenames:
            status = ord_file[0]
            id = ord_file[1:12]
            orders[id] = status
        return orders

    def getOrderByID(self, ID: int):
        """Возвращает Order либо None"""
        filename = self.__getOrderFilename(ID)
        if filename == "":
            return None

        return Order.fromFile(filename)

    def deleteOrderByID(self, ID: int) -> bool:
        """Удаляет как файл, так и элемент словаря"""
        filename = self.__getOrderDirectory(ID)
        if filename == "":
            return False

        shutil.rmtree(filename)
        del self.ordered_filenames[str(ID)]
        return True

    def saveOrder(self, order: Order):
        """Если ордер с таким айди уже существовал, удаляет его"""
        previous_order_filename = self.__getOrderDirectory(order.id)
        if previous_order_filename != "":
            shutil.rmtree(previous_order_filename)

        firstLetter = "N"   # G - если заказ выдан, D - если заказ сделан, N - если заказ не сделан
        if order.isDone:
            firstLetter = "D"
        if order.isVidan:
            firstLetter = "G"
        self.ordered_filenames[str(order.id)] = firstLetter

        Order.toFile(order, self.orders_dir_path)

    def __getOrderFilename(self, ID: int):
        """Возвращает имя файла, либо '' """
        id_str = str(ID)
        try:
            directory_name = self.orders_dir_path + "\\" + self.ordered_filenames[id_str] + id_str
            filename = directory_name + "\\" + self.ordered_filenames[id_str] + id_str + ".order"
        except KeyError:
            filename = ""

        return filename

    def __getOrderDirectory(self, ID: int):
        id_str = str(ID)
        try:
            directory_name = self.orders_dir_path + "\\" + self.ordered_filenames[id_str] + id_str
        except KeyError:
            directory_name = ""

        return directory_name
