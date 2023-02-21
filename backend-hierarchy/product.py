import json
from step import Step
from step import simpleEncoder

class Product:
    def __init__(self, name : str, selling_cost : int, \
                    production_cost = 0, commentary = "", \
                    steps = list(), isDone = False) -> None:

        self.__name = name.capitalize()
        self.__selling_cost = selling_cost
        self.__production_cost = production_cost
        self.__commentary = commentary
        self.__steps = steps
        self.__isDone = isDone
    
    def changeName(self, name : str):
        self.__name = name

    def GetName(self) -> str:
        return self.__name

    def GetSteps(self):
        return self.__steps

    def GetCommentary(self) -> str:
        return self.__commentary

    def ChangeCommentary(self, new_commentary: str):
        self.__commentary = new_commentary
    
    def addStep(self, step_name: str):
        self.__steps.append(Step(step_name))
    
    def CheckIfDone(self) -> bool:
        for step in self.__steps:
            if step.CheckIfDone() == False:
                return False
        self.__isDone = True
        return True

    def GetSellingCost(self) -> int:
        return self.__selling_cost

    def GetProfit(self) -> int:
        return self.__selling_cost - self.__production_cost

    def __str__(self) -> str:
        """вывод инф-и о классе для отладки"""
        step_str = "\n".join(list(step.__str__() for step in self.__steps))
        return f"{self.__name} стоит {self.__selling_cost}. Для выполнения нужно выполнить следующие шаги: \n{step_str}"

    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, jsonString):
        """Возвращает объект класса Product из строки(формата JSON)"""
        info = json.loads(jsonString)
        
        step_list = list(Step.fromDict(step) for step in info["_Product__steps"])

        return Product(info["_Product__name"], info["_Product__selling_cost"], info["_Product__production_cost"], \
                            info["_Product__commentary"], step_list, info["_Product__isDone"])            

    @classmethod
    def fromDICT(cls, info):
        """Возвращает объект класса Product из словаря"""
        
        step_list = list(Step.fromDict(step) for step in info["_Product__steps"])

        return Product(info["_Product__name"], info["_Product__selling_cost"], info["_Product__production_cost"], \
                            info["_Product__commentary"], step_list, info["_Product__isDone"])
    

#enc = simpleEncoder()
#new_dict = enc.default(prod)

#new_dict["_Product__data"] = new_dict["_Product__data"].isoformat()

#print(enc.default(prod))
"""
with open("test.json", "r", encoding="utf-8") as json_text:
    new_prod = Product.fromJSON(json_text.read())

for step in new_prod.GetSteps():
    step.MarkAsDone("lela")
"""

