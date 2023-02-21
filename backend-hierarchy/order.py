import json
from datetime import date

from step import Step
from step import simpleEncoder
from product import Product

import copy


class orderEncoder(json.JSONEncoder):
    """Нужен для нормального перевода класса в JSON
       исключения здесь нужны, потому что эта же функция рекурсивно применяется ко всем вложенным классам   
    """
    def default(self, o):
        slovar = o.__dict__
        try:
            slovar['_Order__date_of_order'] = slovar['_Order__date_of_order'].isoformat()
            slovar['_Order__date_of_vidacha'] = slovar['_Order__date_of_vidacha'].isoformat()
        except KeyError:
            pass
        return slovar

class Order:
    def __init__(self, id : int, zakazchik : str, date_of_order : date, \
                    date_of_vidacha : date, commentary = "", isDone = False, isVidan = False, products = list()) -> None:
        self.__id = id      # может какую хеш функцию использовать?
        self.__zakazchik = zakazchik
        self.__date_of_order = date_of_order
        self.__date_of_vidacha = date_of_vidacha
        self.__commentary = commentary
        self.__isDone = isDone
        self.__isVidan = isVidan
        self.__products = products

        self.__full_cost = self.__CountFullCost()

    def __str__(self) -> str:
        """вывод инф-и о классе для отладки"""
        prods_str = "\n".join(list(prod.__str__() for prod in self.__products))
        return f"Заказ {self.__id} стоит {self.__full_cost}, его надо выдать {self.__date_of_vidacha}.\
                    \nОн состоит из следующих товаров: \n{prods_str}"
    
    def __CountFullCost(self):
        sum = 0
        for prod in self.__products:
            sum += prod.GetSellingCost()
        return sum
    
    def GetCommentary(self) -> str:
        return self.__commentary

    def ChangeCommentary(self, new_commentary: str):
        self.__commentary = new_commentary
    
    def GetId(self) -> str:
        return self.__id
    
    def toJSON(self):
        return json.dumps(self, cls=orderEncoder, sort_keys=True, indent=4, ensure_ascii=False)





    
with open("test.json", "r", encoding="utf-8") as json_text:
    new_prod = Product.fromJSON(json_text.read())
    new_prod1 = copy.copy(new_prod)
    new_prod1.changeName("biba")
    new_prod2 = copy.copy(new_prod)
    new_prod2.changeName("boba")

zakaz = Order(105, "larisa", date(2023, 2, 20), date(2023, 2, 22), products=[new_prod, new_prod1, new_prod2])

print(zakaz.toJSON())