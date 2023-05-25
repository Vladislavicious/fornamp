import json
from datetime import date
from typing import List

from BaH.Contribution import Contribution
from BaH.Contribution import simpleEncoder


class Step:
    def __init__(self, name: str, contributions: List[Contribution] = list(),
                 quantity: int = 1, isDone=False, complexity=1, koef_value=1) -> None:
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
    def isDone(self, value: bool):              # value здесь "просто так"
        if self.number_of_made >= self.quantity:
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
            self.__complexity = 1        # Easy
        if complexity > 5:
            self.__complexity = 5        # Hard

    @property
    def koef_value(self):
        return self.__koef_value

    @koef_value.setter
    def koef_value(self, koef_value: float):
        """Цена шага отосительно товара"""
        self.__koef_value = koef_value

        if koef_value < 0 or koef_value > 1:
            raise ValueError                # Для отладки

    @property
    def total_koef(self):
        return self.koef_value * self.number_of_made

    @property
    def quantity(self):
        """Общее число повторений шага, равно количеству товара"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError
        self.__quantity = value
        self.isDone = True               # та же проверка

    @property
    def number_of_made(self) -> int:
        """То, сколько повторений уже выполнено"""
        number = 0
        if len(self.__contributions) > 0:
            for contr in self.__contributions:
                number += contr.number_of_made
        return number

    @property
    def koef_value_done(self) -> float:
        """То, сколько стоит шаг на данный момент"""
        return self.number_of_made * self.koef_value

    def Contribute(self, contributor: str, number_of_made: int = 1, date_of_creation: date = date.today()):
        """Метод, используемый для создания контрибушнов извне.
           contributor - логин пользователя, number_of_made - сколько
           экземпляров шага выполнено."""
        contr = Contribution(contributor, number_of_made, date_of_creation)
        self.__AddContr(contr)

    def __AddContr(self, contr: Contribution):
        """Позволяет 'переполнять' quantity, потому что в этом нет чего-то плохого"""
        self.__contributions.append(contr)
        self.isDone = True    # так мы запрашиваем проверку на готовность шага

    def GetContr(self):
        return self.__contributions

    def __str__(self) -> str:
        contributors_str = "\n".join(list(contr.__str__() for contr in self.__contributions))

        if self.isDone:
            return f"Шаг {self.name} в количестве {self.quantity} исполнен. Исполнители: \n{contributors_str}"
        return f"Шаг {self.name} не выполнен, текущий прогресс: {self.number_of_made} из {self.quantity}"

    def __hash__(self) -> int:
        return id(self)*self.complexity*self.quantity

    def __eq__(self, other):
        sc = self.__verify_data(other)
        return (self.koef_value == sc.koef_value and self.quantity == sc.quantity
                and self.complexity == sc.complexity and self.name == sc.name)

    def __lt__(self, other):
        sc = self.__verify_data(other)
        if self.koef_value == sc.koef_value:
            if self.quantity == sc.quantity:
                if self.complexity == sc.complexity:
                    if self.name == sc.name:
                        return False
                    return self.name < sc.name
                return self.complexity < sc.complexity
            return self.quantity < sc.quantity
        return self.koef_value < sc.koef_value

    def __gt__(self, other):
        sc = self.__verify_data(other)
        if self.koef_value == sc.koef_value:
            if self.quantity == sc.quantity:
                if self.complexity == sc.complexity:
                    if self.name == sc.name:
                        return False
                    return self.name > sc.name
                return self.complexity > sc.complexity
            return self.quantity > sc.quantity
        return self.koef_value > sc.koef_value

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

    def toHTML(self) -> str:
        if self.isDone:
            return '<li class="green">' + f"Шаг {self.name} в количестве "\
                    f"{self.quantity} исполнен." + '</li>'
        return '<li class="red">' + f"Шаг {self.name} не выполнен, " \
               f"текущий прогресс: {self.number_of_made} из {self.quantity}" + '</li>'

    def toJSON(self) -> str:
        return json.dumps(self, cls=simpleEncoder, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, json_string: str):
        """Возвращает объект класса Step из строки(формата JSON)"""
        info = json.loads(json_string)

        return Step.fromDict(info)

    @classmethod
    def fromDict(cls, info: dict):
        """Возвращает объект класса Step из словаря"""

        contr_list = list(Contribution.fromDict(contr) for contr in info["contributions"])

        return Step(name=info["name"], complexity=info["complexity"], koef_value=info["koef_value"],
                    contributions=contr_list, quantity=info["quantity"], isDone=info["isDone"])
