import json
import datetime
from datetime import date
from typing import List #Типизированный список
from copy import deepcopy
from random import Random

from Contribution import simpleEncoder
from product import Product


class Order:
    def __init__(self, id : int, zakazchik : str, date_of_creation : date, \
                    date_of_vidacha : date, products : List[Product] = list(), commentary = "", isDone = False, \
                        isVidan = False) -> None:
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
        today = datetime.datetime.today()
        number = (today.year * today.day // today.month) + (today.hour * today.minute + today.second * id)
        rand = Random()
        rand.seed(number)
        self.__id = rand.randint(10000000000, 99999999999)
        
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
    def date_of_creation(self, value : date):
        self.__date_of_creation = value.isoformat()

    @property
    def date_of_vidacha(self) -> date:
        """Дата в iso формате"""
        return date.fromisoformat(self.__date_of_vidacha)
    
    @date_of_vidacha.setter
    def date_of_vidacha(self, value : date):
        self.__date_of_vidacha = value.isoformat()

    @property
    def commentary(self):
        return self.__commentary

    @commentary.setter
    def commentary(self, value : str):
        self.__commentary = value 

    @property
    def isDone(self):
        return self.__isDone

    @isDone.setter
    def isDone(self, value : bool):
        self.__isDone = value 
    
    @property
    def isVidan(self):
        return self.__isVidan

    @isDone.setter
    def isVidan(self, value : bool):
        self.__isVidan = value 

    @property
    def full_cost(self) -> float:
        sum = 0
        for prod in self.GetProducts():
            sum += prod.selling_cost * prod.quantity
        return sum
    
    def GetProducts(self):
        return self.__products

    def AddProduct(self, step: Product):
        self.__products.append(step)


    def DeleteProduct(self, product_name: str): # Скорее всего надо будет добавить и товарам айди, чтобы не удалить случайно чего лишнего
        product_for_deletion = None
        for product in self.GetProducts():
            if product.name == product_name.capitalize():
                product_for_deletion = product
        
        if product_for_deletion != None:
            self.__products.remove(product_for_deletion)

    def __str__(self) -> str:
        """вывод инф-и о классе для отладки"""
        prods_str = "\n".join(list(prod.__str__() for prod in self.GetProducts()))

        return f"Заказ {self.id} стоит {self.full_cost}, его надо выдать {self.date_of_vidacha}.\
                    \nОн состоит из следующих товаров: \n{prods_str}"
    
    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, json_string: str):
        """Возвращает объект класса Order из строки(формата JSON)"""
        info = json.loads(json_string)
        
        return Order.fromDict(info)

    @classmethod
    def fromDict(cls, info : dict):
        """Возвращает объект класса Order из словаря"""

        product_list = list(Product.fromDict(prod) for prod in info["_Order__products"])

        data_creat = date.fromisoformat(info["_Order__date_of_creation"])
        data_vid = date.fromisoformat(info["_Order__date_of_vidacha"])

        return Order(zakazchik=info["_Order__zakazchik"], id=info["_Order__id"], date_of_creation=data_creat, \
                        date_of_vidacha=data_vid, commentary=info["_Order__commentary"], \
                        isDone=info["_Order__isDone"], isVidan=info["_Order__isVidan"], products=product_list)
    

def listToJSON(orders : List[Order]) -> str:
    return json.dumps(orders, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)
"""
"""
def listFromJSON(filename : str) -> List[Order]:
    filepath = filename.lower()
    if not filename.endswith(".json"):
        filepath += ".json"
    
    with open(filepath, "r", encoding="utf-8") as opened_file:
        loaded_list = json.load(opened_file)
        
    return listFromJSONlist(loaded_list)

def listFromJSONlist(info : list) -> List[Order]:
    list_of_orders = list()
    for order in info:
        list_of_orders.append(Order.fromDict(order))
        
    return list_of_orders