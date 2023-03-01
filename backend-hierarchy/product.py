import json
from typing import List #Типизированный список
from copy import deepcopy

from step import Step
from Contribution import simpleEncoder



class Product:
    def __init__(self, name : str, selling_cost : int, steps : List[Step] = list(), \
                    quantity = 1, production_cost = 0, commentary = "", \
                    isDone = False) -> None:

        self.name = name
        self.selling_cost = selling_cost
        self.production_cost = production_cost
        self.commentary = commentary
        self.isDone = isDone
        self.quantity = quantity

        self.__steps = steps
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name.capitalize()

    @property
    def isDone(self):
        return self.__isDone

    @isDone.setter
    def isDone(self, value : bool):
        self.__isDone = value 

    @property
    def selling_cost(self):
        return self.__selling_cost

    @selling_cost.setter
    def selling_cost(self, value : float):
        if value < 0:
            raise ValueError
        
        self.__selling_cost = value 

    @property
    def production_cost(self):
        return self.__production_cost

    @production_cost.setter
    def production_cost(self, value : float):
        if value < 0:
            raise ValueError
        
        self.__production_cost = value 

    @property
    def profit(self):
        """Прибыль от продажи единицы товара"""
        return self.selling_cost - self.production_cost
    
    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value : int):
        if value < 0:
            raise ValueError
        self.__quantity = value
    
    @property
    def commentary(self):
        return self.__commentary

    @commentary.setter
    def commentary(self, value : str):
        self.__commentary = value 

    def GetSteps(self):
        return self.__steps

    def AddStep(self, step: Step):
        
        step.quantity = self.quantity
        self.__steps.append(step)
        self.EvaluateSteps()


    def DeleteStep(self, step_name: str):
        step_for_deletion = None
        for step in self.__steps:
            if step.name == step_name.lower():
                step_for_deletion = step
        
        if step_for_deletion != None:
            self.__steps.remove(step_for_deletion)

    def __CountBaseVal(self) -> float:
        """Считает сколько стоит самый простой шаг в расчете на коичество единиц товара и возвращает значение между (0 , 1)"""
        total = 0.
        for step in self.__steps:
            total += step.complexity
        
        if total != 0:
            return 1 / total
        else:
            return None
                
    def EvaluateSteps(self) -> None:
        base_value = self.__CountBaseVal()

        if base_value != None:
            for step in self.__steps:
                step.koef_value = base_value * step.complexity

    def CheckIfDone(self) -> bool:
        """проверяет Готовность всех шагов"""
        for step in self.__steps:
            if step.isDone == False:
                self.isDone = False
                return False
        self.isDone = True
        return True

    def __str__(self) -> str:
        """вывод инф-и о классе для отладки"""
        step_str = "\n".join(list(step.__str__() for step in self.__steps))
        return f"Товар {self.name} стоит {self.selling_cost}. Для выполнения {self.quantity} штук нужно выполнить следующие шаги: \n{step_str}"

    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)

    @classmethod
    def fromJSON(cls, jsonString : str):
        """Возвращает объект класса Product из строки(формата JSON)"""
        info = json.loads(jsonString)
        
        return Product.fromDict(info)            

    @classmethod
    def fromDict(cls, info : dict):
        """Возвращает объект класса Product из словаря"""
        
        step_list = list(Step.fromDict(step) for step in info["_Product__steps"])

        return Product(name=info["_Product__name"], selling_cost=info["_Product__selling_cost"], steps=step_list, \
                        production_cost=info["_Product__production_cost"], commentary=info["_Product__commentary"], \
                        isDone=info["_Product__isDone"], quantity=info["_Product__quantity"])
    
"""
prod = Product("Пряник", 150, quantity=15)

with open("step.json", "r", encoding="utf-8") as opened_file:

    new_step = Step.fromJSON(opened_file.read())
    #print(new_step)
    prod.AddStep(new_step)

    n_step = deepcopy(new_step)
    n_step.GetContr().pop()
    n_step.GetContr().pop()
    n_step.name = "Выпечь"
    n_step.complexity = 3
    prod.AddStep(n_step)

    for steps in prod.GetSteps():
        print(steps.name, steps.koef_value_done)

with open("product.json", "w", encoding="utf-8") as opened_file:
    opened_file.write(prod.toJSON())
"""