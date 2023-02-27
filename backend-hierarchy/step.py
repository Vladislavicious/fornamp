import json
from datetime import date

class simpleEncoder(json.JSONEncoder):
    """Нужен для нормального перевода класса в JSON"""
    def default(self, o):
        slovar = o.__dict__

        return slovar

class Step:
    def __init__(self, name: str, data = date.today(), isDone=False,  \
                    contributor="No-one", complexity = 1, koef_value = 1, \
                         quantity = 1, number_of_made = 0) -> None:
        self.isDone = isDone
        self.contributor = contributor
        self.name = name
        self.complexity = complexity
        self.koef_value = koef_value
        self.date_of_creation = data # на вход получаем в виде date, а храним всё в виде isoformat строки
        self.number_of_made = number_of_made
        self.quantity = quantity
    
    @property
    def date_of_creation(self) -> date:
        """Дата, когда был выполнен шаг в iso формате"""
        return date.fromisoformat(self.__date_of_creation)
    
    @date_of_creation.setter
    def date_of_creation(self, value : date):
        self.__date_of_creation = value.isoformat()

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
    def contributor(self):
        return self.__contributor
    
    @contributor.setter
    def contributor(self, contributor: str):
        self.__contributor = contributor.capitalize() 

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
    def number_of_made(self):
        return self.__number_of_made
    
    @number_of_made.setter
    def number_of_made(self, number: int):
        if number > self.quantity:
            number = self.quantity
        if number < 0:
            number = 0
        self.__number_of_made = number

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

    def __str__(self) -> str:
        if self.__isDone:
            return f"Шаг {self.name} в количестве {self.quantity}. Исполнитель: {self.contributor}"
        return f"Шаг {self.name} не выполнен, текущий прогресс: {self.number_of_made} из {self.quantity}"

    def MarkAsDone(self, contributor: str, data : date, number_of_made = 1) -> None:
        """Шаг считается выполненным, когда все повторения выполнены"""
        self.contributor = contributor 
        self.date_of_creation = data
        self.number_of_made = number_of_made

        
        self.isDone = True

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
        data_dat = date.fromisoformat(info["_Step__date_of_creation"])

        return Step(name=info["_Step__name"],isDone=info["_Step__isDone"],contributor=info["_Step__contributor"], \
                        complexity=info["_Step__complexity"], koef_value=info["_Step__koef_value"], \
                            data=data_dat, number_of_made=info["_Step__number_of_made"], quantity=info["_Step__quantity"])


