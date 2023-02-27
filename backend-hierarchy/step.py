import json
from datetime import date

class simpleEncoder(json.JSONEncoder):
    """Нужен для нормального перевода класса в JSON"""
    def default(self, o):
        slovar = o.__dict__
        try:
            slovar['_Step__date_of_creation'] = slovar['_Step__date_of_creation'].isoformat()
            slovar['_Order__date_of_creation'] = slovar['_Order__date_of_creation'].isoformat()
            slovar['_Order__date_of_vidacha'] = slovar['_Order__date_of_vidacha'].isoformat()
        except KeyError:
            pass
        return slovar

class Step:
    def __init__(self, name: str, data = date.today().isoformat(), isDone=False,  \
                    contributor="No-one", complexity = 1, koef_value = 1) -> None:
        self.isDone = isDone
        self.contributor = contributor
        self.name = name
        self.complexity = complexity
        self.koef_value = koef_value
        self.date_of_creation = data
    
    @property
    def date_of_creation(self) -> date:
        """Дата в iso формате"""
        return self.__date_of_creation
    
    @date_of_creation.setter
    def date_of_creation(self, isoformatted_value : str):
        self.__date_of_creation = date.fromisoformat(isoformatted_value)

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

    def MarkAsDone(self, contributor: str, done = True) -> None:
        self.isDone = done
        self.contributor = contributor 

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
        

        return Step(name=info["_Step__name"],isDone=info["_Step__isDone"],contributor=info["_Step__contributor"], \
                        complexity=info["_Step__complexity"], koef_value=info["_Step__koef_value"], data=info["_Step__date_of_creation"])


#aboba = Step("Выпечь", data=date(year=2003, month=7, day=18).isoformat())

#print(aboba.toJSON())

#print(Step.fromJSON(aboba.toJSON()))

with open("step.json", "r", encoding="utf-8") as file:
    aboba = Step.fromJSON(file.read())
    print(type(aboba.toJSON()))
