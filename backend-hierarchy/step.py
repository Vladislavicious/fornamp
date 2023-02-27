import json

class simpleEncoder(json.JSONEncoder):
    """Нужен для нормального перевода класса в JSON"""
    def default(self, o):
        return o.__dict__

class Step:
    def __init__(self, name: str, isDone=False, contributor="No-one") -> None:
        self.isDone = isDone
        self.contributor = contributor
        self.name = name
    
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

    def __str__(self) -> str:
        if self.__isDone:
            return f"Шаг {self.name}. Исполнитель: {self.contributor}"
        return f"Шаг {self.name} не выполнен"

    def MarkAsDone(self, contributor: str) -> None:
        """Меняет готовность на противоположную"""
        self.isDone = not (self.isDone)
        self.contributor = contributor 

    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, jsonString: str):
        """Возвращает объект класса Step из строки(формата JSON)"""
        info = json.loads(jsonString)
        
        return Step(info["_Step__name"], info["_Step__isDone"], info["_Step__contributor"])

    @classmethod
    def fromDict(cls, info : dict):
        """Возвращает объект класса Step из словаря"""
        
        return Step(info["_Step__name"], info["_Step__isDone"], info["_Step__contributor"])


aboba = Step("Шаг")

print(aboba.toJSON())