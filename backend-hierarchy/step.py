import json
from datetime import date

class simpleEncoder(json.JSONEncoder):
    """Нужен для нормального перевода класса в JSON"""
    def default(self, o):
        slovar = o.__dict__

        return slovar

class Step:
    def __init__(self, name: str, data = date.today(), isDone=False,  \
                    contributor="No-one", complexity = 1, koef_value = 1) -> None:
        self.isDone = isDone
        self.contributor = contributor
        self.name = name
        self.complexity = complexity
        self.koef_value = koef_value
        self.date_of_creation = data # на вход получаем в виде date, а храним всё в виде isoformat строки
    
    @property
    def date_of_creation(self) -> date:
        """Дата в iso формате"""
        return date.fromisoformat(self.__date_of_creation)
    
    @date_of_creation.setter
    def date_of_creation(self, value : date):
        self.__date_of_creation = value.isoformat()

    @property
    def isDone(self):
        return self.__isDone

    @isDone.setter
    def isDone(self, value : bool):
        self.__isDone = value 

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
    def koef_value(self):
        return self.__koef_value
    
    @koef_value.setter
    def koef_value(self, koef_value: float):
        """Цена шага отосительно товара"""
        self.__koef_value = koef_value

        if koef_value < 0 or koef_value > 1: 
            raise ValueError # Для отладки

    def __str__(self) -> str:
        if self.__isDone:
            return f"Шаг {self.name}. Исполнитель: {self.contributor}"
        return f"Шаг {self.name} не выполнен"

    def MarkAsDone(self, contributor: str, data : date, done = True) -> None:
        self.isDone = done
        self.contributor = contributor 
        self.date_of_creation = data

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
                        complexity=info["_Step__complexity"], koef_value=info["_Step__koef_value"], data=data_dat)


