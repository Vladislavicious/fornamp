from dataclasses import dataclass
import json
import datetime
from operator import attrgetter
import os
from datetime import date
import pickle
from typing import List, Tuple
from random import Random

from BaH.Contribution import getValidData
from BaH.Contribution import simpleEncoder
from BaH.product import Product


@dataclass(repr=False)
class OrderPreview:
    id: int
    date_of_vidacha: date
    zakazchik: str
    isDone: bool
    isVidan: bool

    def __repr__(self) -> str:
        zakazchik = f"Заказчик: {self.zakazchik}\n"
        date_end = f"Дата выдачи: {getValidData(self.date_of_vidacha)}\n"
        return zakazchik + date_end


class OrderPreviewSorter:
    """Абстрактный класс, нужен только чтобы скомпоновать методы"""
    @classmethod
    def ByVidachaDate(cls, ord_prevs: List[OrderPreview], reverse=False) -> List[OrderPreview]:
        return sorted(ord_prevs,
                      key=lambda order_preview: order_preview.date_of_vidacha, reverse=reverse)

    @classmethod
    def ByName(cls, ord_prevs: List[OrderPreview], reverse=False) -> List[OrderPreview]:
        return sorted(ord_prevs,
                      key=lambda order_preview: order_preview.zakazchik, reverse=reverse)

    @classmethod
    def Multisort(cls, ord_prevs: List[OrderPreview], sorting_params: List[Tuple[str, bool]]) -> List[OrderPreview]:
        """сортировка по нескольким аргументам
           в параметрах указывать кортеж из название поля и обратная/прямая сортировка,
           например: ('date_of_vidacha', True) - сортируем по полю даты выдачи в восходящем порядке"""
        for key, reverse in reversed(sorting_params):
            ord_prevs.sort(key=attrgetter(key), reverse=reverse)
        return ord_prevs


class Order:
    def __init__(self, id: int, zakazchik: str, date_of_creation: date,
                 date_of_vidacha: date, products: List[Product] = list(), commentary="",
                 isDone=False, isVidan=False) -> None:
        self.id = id
        self.zakazchik = zakazchik
        self.date_of_creation = date_of_creation
        self.date_of_vidacha = date_of_vidacha
        self.commentary = commentary
        self.isDone = isDone
        self.isVidan = isVidan

        self.__products = products

    @property
    def id(self):
        """Случайное одиннадцатизначное число, задаваемое seed'ом"""
        return self.__id

    @id.setter
    def id(self, id: int):
        if id <= 10000000000 or id >= 99999999999:
            today = datetime.datetime.today()
            number = (today.year * today.day // today.month) + (today.hour * today.minute + today.second * id)
            rand = Random()
            rand.seed(number)
            self.__id = rand.randint(10000000000, 99999999999)
        else:
            self.__id = id

    @property
    def zakazchik(self):
        return self.__zakazchik

    @zakazchik.setter
    def zakazchik(self, zakazchik: str):
        self.__zakazchik = zakazchik.capitalize()

    @property
    def date_of_creation(self) -> date:
        """Дата в iso формате"""
        return date.fromisoformat(self.__date_of_creation)

    @date_of_creation.setter
    def date_of_creation(self, value: date):
        self.__date_of_creation = value.isoformat()

    @property
    def date_of_vidacha(self) -> date:
        """Дата в iso формате"""
        return date.fromisoformat(self.__date_of_vidacha)

    @date_of_vidacha.setter
    def date_of_vidacha(self, value: date):
        self.__date_of_vidacha = value.isoformat()

    @property
    def commentary(self):
        return self.__commentary

    @commentary.setter
    def commentary(self, value: str):
        self.__commentary = value

    @property
    def isDone(self):
        return self.__isDone

    @isDone.setter
    def isDone(self, value: bool):
        self.__isDone = value

    @property
    def isVidan(self):
        return self.__isVidan

    @isVidan.setter
    def isVidan(self, value: bool):
        self.__isVidan = value

    @property
    def total_cost(self) -> float:
        sum = 0
        for prod in self.GetProducts():
            sum += prod.total_cost
        return sum

    def CheckIfDone(self) -> bool:
        """проверяет Готовность всех товаров"""
        for product in self.GetProducts():
            if not product.CheckIfDone():
                self.isDone = False
                return False
        self.isDone = True
        return True

    def GetProducts(self):
        return self.__products

    def AddProduct(self, product: Product):
        self.__products.append(product)
        self.CheckIfDone()

    def DeleteProduct(self, product_name: str):
        product_for_deletion = None
        for product in self.GetProducts():
            if product.name == product_name.capitalize():
                product_for_deletion = product

        if product_for_deletion is not None:
            self.__products.remove(product_for_deletion)

        self.CheckIfDone()

    def ClearProducts(self):
        self.__products.clear()

    def __str__(self) -> str:
        """вывод инф-и о классе для отладки"""
        prods_str = "\n".join(list(prod.__str__() for prod in self.GetProducts()))

        return f"Заказ {self.id} стоит {self.total_cost}, его надо выдать {getValidData(self.date_of_vidacha)}.\
                    \nОн состоит из следующих товаров: \n{prods_str}"

    def __hash__(self) -> int:
        return id(self)*self.date_of_vidacha.day + self.id

    def __eq__(self, other):
        sc = self.__verify_data(other)
        return (self.total_cost == sc.total_cost and self.date_of_vidacha == sc.date_of_vidacha
                and self.date_of_creation == sc.date_of_creation)

    def __lt__(self, other):
        """Сортировка в порядке: дата выдачи, общая цена, дата создания"""
        sc = self.__verify_data(other)
        if self.date_of_vidacha == sc.date_of_vidacha:
            if self.total_cost == sc.total_cost:
                if self.date_of_creation == sc.date_of_creation:
                    return False
                return self.date_of_creation < sc.date_of_creation
            return self.total_cost < sc.total_cost
        return self.date_of_vidacha < sc.date_of_vidacha

    def __gt__(self, other):
        sc = self.__verify_data(other)
        if self.date_of_vidacha == sc.date_of_vidacha:
            if self.total_cost == sc.total_cost:
                if self.date_of_creation == sc.date_of_creation:
                    return False
                return self.date_of_creation > sc.date_of_creation
            return self.total_cost > sc.total_cost
        return self.date_of_vidacha > sc.date_of_vidacha

    def __le__(self, other):
        sc = self.__verify_data(other)
        return self < sc or self == sc

    def __ge__(self, other):
        sc = self.__verify_data(other)
        return self > sc or self == sc

    @classmethod
    def __verify_data(cls, other):
        if not isinstance(other, cls):
            raise TypeError(f"Операнд справа должен иметь тип {cls}")

        return other

    def createPreview(self) -> OrderPreview:
        return OrderPreview(id=self.id, date_of_vidacha=self.date_of_vidacha,
                            isDone=self.isDone, zakazchik=self.zakazchik, isVidan=self.isVidan)

    def toHTML(self) -> str:
        prod = "\n".join(list(prod.toHTML() for prod in self.GetProducts()))

        prods_str = '<ol>\n' + prod + "\n</ol>"

        if self.CheckIfDone():
            beginning = '<em class="green">'
        else:
            beginning = '<em class="red">'
        text = beginning + f"Заказ {self.id} стоит {self.total_cost}, его" + \
                           f" надо выдать {getValidData(self.date_of_vidacha)}</em>" + \
                           f"\n<br>Он состоит из следующих товаров: \n{prods_str}"

        return text

    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, indent=4, ensure_ascii=False)

    def toJSONFile(self, directory: str = ""):
        """Сохраняет заказ в указанной директории, по умолчанию в рабочей. указывать абсолютный путь
           Возвращает True при успешном сохранении"""
        if directory == "":
            directory = os.getcwd()

        if not os.path.exists(directory):
            return False
        firstLetter = "N"   # G - если заказ выдан, D - если заказ сделан, N - если заказ не сделан
        if self.isDone:
            firstLetter = "D"
        elif self.isVidan:
            firstLetter = "G"

        filename = directory + "\\" + firstLetter + str(self.id) + ".order"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.toJSON())
        return True

    def toFile(self, directory: str = ""):
        """Сохраняет заказ в указанной директории, по умолчанию в рабочей. указывать абсолютный путь
           Возвращает True при успешном сохранении"""
        if directory == "":
            directory = os.getcwd()

        if not os.path.exists(directory):
            return False
        firstLetter = "N"   # G - если заказ выдан, D - если заказ сделан, N - если заказ не сделан
        if self.isDone:
            firstLetter = "D"
        elif self.isVidan:
            firstLetter = "G"

        filename = directory + "\\" + firstLetter + str(self.id) + ".order"

        with open(filename, "wb") as file:
            pickle.dump(self, file)

        return True

    @classmethod
    def fromFile(cls, filepath: str):
        with open(filepath, "rb") as file:
            return pickle.load(file)

    @classmethod
    def fromJSONFile(cls, filepath: str):
        with open(filepath, "r", encoding="utf-8") as file:
            return cls.fromJSON(file.read())

    @classmethod
    def fromJSON(cls, json_string: str):
        """Возвращает объект класса Order из строки(формата JSON)"""
        info = json.loads(json_string)

        return Order.fromDict(info)

    @classmethod
    def fromDict(cls, info: dict):
        """Возвращает объект класса Order из словаря"""

        product_list = list(Product.fromDict(prod) for prod in info["products"])

        data_creat = date.fromisoformat(info["date_of_creation"])
        data_vid = date.fromisoformat(info["date_of_vidacha"])

        return Order(zakazchik=info["zakazchik"], id=info["id"], date_of_creation=data_creat,
                     date_of_vidacha=data_vid, commentary=info["commentary"],
                     isDone=info["isDone"], isVidan=info["isVidan"], products=product_list)
