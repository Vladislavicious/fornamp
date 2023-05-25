import json
from datetime import date
from copy import deepcopy


class simpleEncoder(json.JSONEncoder):
    """Нужен для нормального перевода класса в JSON"""
    def default(self, o):
        slovar = deepcopy(o.__dict__)
        className = "_" + type(o).__name__ + "__"

        slovarKeys = list(slovar.keys())
        properNames = list(name.replace(className, "") for name in slovarKeys)

        for i in properNames:
            slovar[i] = slovar.pop(className + i)

        return slovar


class Contribution:
    def __init__(self, contributor: str, number_of_made: int = 1, date_of_creation: date = date.today()) -> None:
        self.date_of_creation = date_of_creation  # на вход получаем в виде date, а храним всё в виде isoformat строки
        self.contributor = contributor
        self.number_of_made = number_of_made

    @property
    def date_of_creation(self) -> date:
        """Дата, когда был выполнен шаг в iso формате"""
        return date.fromisoformat(self.__date_of_creation)

    @date_of_creation.setter
    def date_of_creation(self, value: date):
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
        return f"{getValidData(self.date_of_creation)} {self.contributor} выполнил {self.number_of_made}"

    def __hash__(self) -> int:
        return id(self)*self.date_of_creation.day*(self.number_of_made**len(self.contributor))

    def __eq__(self, other):
        sc = self.__verify_data(other)
        return (self.number_of_made == sc.number_of_made and self.contributor == sc.contributor
                and self.date_of_creation == sc.date_of_creation)

    def __lt__(self, other):
        sc = self.__verify_data(other)
        if self.date_of_creation == sc.date_of_creation:
            if self.number_of_made == sc.number_of_made:
                if self.contributor == sc.contributor:
                    return False
                return self.contributor < sc.contributor
            return self.number_of_made < sc.number_of_made
        return self.date_of_creation < sc.date_of_creation

    def __gt__(self, other):
        sc = self.__verify_data(other)
        if self.date_of_creation == sc.date_of_creation:
            if self.number_of_made == sc.number_of_made:
                if self.contributor == sc.contributor:
                    return False
                return self.contributor > sc.contributor
            return self.number_of_made > sc.number_of_made
        return self.date_of_creation > sc.date_of_creation

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

    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, json_string: str):
        """Возвращает объект класса Contribution из строки(формата JSON)"""
        info = json.loads(json_string)

        return Contribution.fromDict(info)

    @classmethod
    def fromDict(cls, info: dict):
        """Возвращает объект класса Contribution из словаря"""
        data_dat = date.fromisoformat(info["date_of_creation"])

        return Contribution(contributor=info["contributor"],
                            number_of_made=info["number_of_made"], date_of_creation=data_dat)


def getValidData(data: date) -> str:
    """Возвращает дату в удобочитаемом виде (ДД-ММ-ГГГГ)"""
    return data.strftime("%d-%m-%Y")
