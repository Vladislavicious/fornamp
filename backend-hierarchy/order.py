import json
from datetime import date
from typing import List #Типизированный список

from Contribution import simpleEncoder
from product import Product


class Order:
    def __init__(self, id : int, zakazchik : str, date_of_creation : date, \
                    date_of_vidacha : date, commentary = "", isDone = False, \
                        isVidan = False, products = List[Product]) -> None:
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
        return self.__id
    
    @id.setter
    def id(self, id: int):
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
        for prod in self.__products:
            sum += prod.selling_cost
        return sum
    
    def GetProducts(self):
        return self.__products

    def AddProduct(self, step: Product):
        self.__products.append(step)


    def DeleteProduct(self, product_name: str): # Скорее всего надо будет добавить и товарам айди, чтобы не удалить случайно чего лишнего
        product_for_deletion = None
        for product in self.__products:
            if product.name == product_name.capitalize():
                product_for_deletion = product
        
        if product_for_deletion != None:
            self.__products.remove(product_for_deletion)

    def __str__(self) -> str:
        """вывод инф-и о классе для отладки"""
        prods_str = "\n".join(list(prod.__str__() for prod in self.__products))
        return f"Заказ {self.id} стоит {self.full_cost}, его надо выдать {self.date_of_vidacha}.\
                    \nОн состоит из следующих товаров: \n{prods_str}"
    
    
    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, jsonString: str):
        """Возвращает объект класса Order из строки(формата JSON)"""
        info = json.loads(jsonString)
        
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