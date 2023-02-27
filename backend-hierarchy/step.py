import json

class simpleEncoder(json.JSONEncoder):
    """Нужен для нормального перевода класса в JSON"""
    def default(self, o):
        return o.__dict__

class Step:
    def __init__(self, name: str, isDone=False, contributor="No-one", \
                    complexity = 1, koef_value = 1) -> None:
        self.isDone = isDone
        self.contributor = contributor
        self.name = name
        self.complexity = complexity
        self.koef_value = koef_value
    
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
        """Сложность шага, 1 - лёгкий, 2 - средний, 3 - тяжёлый"""
        self.__complexity = complexity

        if complexity < 1:
            self.__complexity = 1 # Easy
        if complexity > 3:
            self.__complexity = 3 # Hard

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
        
        return Step(info["_Step__name"], info["_Step__isDone"], info["_Step__contributor"], \
                        info["_Step__complexity"], info["_Step__koef_value"])

