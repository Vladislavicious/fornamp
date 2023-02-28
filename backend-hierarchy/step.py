import json
from datetime import date
from typing import List

from Contribution import Contribution
from Contribution import simpleEncoder




class Step:
    def __init__(self, name: str, isDone=False, complexity = 1, koef_value = 1, \
                      contributions = List[Contribution] ,  quantity = 1) -> None:
        self.isDone = isDone
        self.name = name
        self.complexity = complexity
        self.koef_value = koef_value
        self.quantity = quantity

        self.__contributions = contributions

    @property
    def isDone(self):
        return self.__isDone

    @isDone.setter
    def isDone(self):
        if self.number_of_made == self.quantity:
            self.isDone = True
        else:
            self.isDone = False

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

    @property
    def number_of_made(self) -> int:
        """То, сколько повторений уже выполнено"""
        number = 0
        for contr in self.__contributions:
            number += contr.number_of_made
        return number

    def __str__(self) -> str:
        if self.isDone:
            return f"Шаг {self.name} в количестве {self.quantity}. Исполнитель: {self.contributor}"
        return f"Шаг {self.name} не выполнен, текущий прогресс: {self.number_of_made} из {self.quantity}"
    
    def addContribution(self, contributor: str, data = date.today, number_of_made = 1) -> bool:
        if self.quantity - number_of_made >= 0 and self.quantity - (number_of_made + self.number_of_made) >= 0:
            contr = Contribution(contributor=contributor, number_of_made=number_of_made, date_of_creation=data)
            self.__contributions.append(contr)
            self.isDone = True
            return True
        return False

    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, jsonString: str):
        """Возвращает объект класса Step из строки(формата JSON)"""
        info = json.loads(jsonString)
        
        return Step.fromDict(info)

    @classmethod
    def fromDict(cls, info : dict):
        """Возвращает объект класса Step из словаря"""

        contr_list = list(Contribution.fromDict(contr) for contr in info["_Step__contributions"])

        return Step(name=info["_Step__name"],isDone=info["_Step__isDone"], \
                        complexity=info["_Step__complexity"], koef_value=info["_Step__koef_value"], \
                           contributions=contr_list , quantity=info["_Step__quantity"])


