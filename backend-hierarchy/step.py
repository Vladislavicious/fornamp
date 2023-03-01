import json
from datetime import date
from typing import List

from Contribution import Contribution
from Contribution import simpleEncoder




class Step:
    def __init__(self, name: str, contributions : List[Contribution] = list(), \
                 quantity : int = 1, isDone=False, complexity = 1, koef_value = 1) -> None:
        self.name = name
        self.complexity = complexity
        self.koef_value = koef_value

        self.__contributions = contributions

        self.quantity = quantity
        self.isDone = isDone

    @property
    def isDone(self):
        return self.__isDone

    @isDone.setter
    def isDone(self, value : bool): #value здесь "просто так"
        if self.number_of_made == self.quantity:
            self.__isDone = True
        else:
            self.__isDone = False

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name.lower()

    @property
    def complexity(self):
        return self.__complexity
    
    @complexity.setter
    def complexity(self, complexity: int):
        """Сложность шага, 1 - лёгкий, 3 - средний, 5 - тяжёлый"""
        self.__complexity = complexity

        if complexity < 1:
            self.__complexity = 1 # Easy
        if complexity > 5:
            self.__complexity = 5 # Hard

    @property
    def koef_value(self):
        return self.__koef_value
    
    @koef_value.setter
    def koef_value(self, koef_value: float):
        """Цена шага отосительно товара"""
        self.__koef_value = koef_value

        if koef_value < 0 or koef_value > 1: 
            raise ValueError # Для отладки
        
    @property
    def total_koef(self):
        return self.koef_value * self.number_of_made
    
    @property
    def quantity(self):
        """Общее число повторений шага, равно количеству товара"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value : int):
        if value < 0:
            raise ValueError
        self.__quantity = value
        self.isDone = True # та же проверка

    @property
    def contr_length(self) -> int:
        num = 0
        for item in self.__contributions:
            num = num + 1
        return num

    @property
    def number_of_made(self) -> int:
        """То, сколько повторений уже выполнено"""
        number = 0
        if self.contr_length > 0:
            for contr in self.__contributions:
                number += contr.number_of_made
        return number
    
    @property
    def koef_value_done(self) -> float:
        """То, сколько стоит шаг на данный момент"""
        return self.number_of_made * self.koef_value
    
    def AddContr(self, contr : Contribution):
        if self.contr_length == 0 and contr.number_of_made < self.quantity: 
            self.__contributions.append(contr)
        elif contr.number_of_made + self.number_of_made <= self.quantity:
            self.__contributions.append(contr)
        self.isDone = True #так мы запрашиваем проверку на готовность шага

    def GetContr(self):
        return self.__contributions

    def __str__(self) -> str:
        contributors_str = "\n".join(list(contr.__str__() for contr in self.__contributions))

        if self.isDone:
            return f"Шаг {self.name} в количестве {self.quantity} исполнен. Исполнители: \n{contributors_str}"
        return f"Шаг {self.name} не выполнен, текущий прогресс: {self.number_of_made} из {self.quantity}"
    

    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, json_string: str):
        """Возвращает объект класса Step из строки(формата JSON)"""
        info = json.loads(json_string)
        
        return Step.fromDict(info)

    @classmethod
    def fromDict(cls, info : dict):
        """Возвращает объект класса Step из словаря"""

        contr_list = list(Contribution.fromDict(contr) for contr in info["_Step__contributions"])

        return Step(name=info["_Step__name"], \
                        complexity=info["_Step__complexity"], koef_value=info["_Step__koef_value"], \
                           contributions=contr_list , quantity=info["_Step__quantity"], isDone=info["_Step__isDone"])
