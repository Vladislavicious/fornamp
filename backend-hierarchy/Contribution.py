import json
from datetime import date

class simpleEncoder(json.JSONEncoder):
    """Нужен для нормального перевода класса в JSON"""
    def default(self, o):
        slovar = o.__dict__

        return slovar

class Contribution:
    def __init__(self, contributor : str, number_of_made : int = 1, date_of_creation : date = date.today()) -> None:
        self.date_of_creation = date_of_creation # на вход получаем в виде date, а храним всё в виде isoformat строки
        self.contributor = contributor
        self.number_of_made = number_of_made

    @property
    def date_of_creation(self) -> date:
        """Дата, когда был выполнен шаг в iso формате"""
        return date.fromisoformat(self.__date_of_creation)
    
    @date_of_creation.setter
    def date_of_creation(self, value : date):
        self.__date_of_creation = value.isoformat()

    @property
    def contributor(self):
        return self.__contributor
    
    @contributor.setter
    def contributor(self, contributor: str):
        self.__contributor = contributor.capitalize()
    
    @property
    def number_of_made(self):
        return self.__number_of_made
    
    @number_of_made.setter
    def number_of_made(self, number: int):
        if number < 0:
            self.__number_of_made = 0
        else:
            self.__number_of_made = number

    def __str__(self) -> str:
        return f"{self.date_of_creation.isoformat()} {self.contributor} выполнил {self.number_of_made}"

    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, json_string: str):
        """Возвращает объект класса Contribution из строки(формата JSON)"""
        info = json.loads(json_string)
        
        return Contribution.fromDict(info)
    
    @classmethod
    def fromDict(cls, info : dict):
        """Возвращает объект класса Contribution из словаря"""
        data_dat = date.fromisoformat(info["_Contribution__date_of_creation"])

        return Contribution(contributor=info["_Contribution__contributor"], \
                            number_of_made=info["_Contribution__number_of_made"], date_of_creation=data_dat)


    