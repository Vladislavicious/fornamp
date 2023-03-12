import json
from typing import List #Типизированный список
from copy import deepcopy

from BaH.step import Step
from BaH.Contribution import simpleEncoder



class Product:
    def __init__(self, name : str, selling_cost : int, steps : List[Step] = list(), \
                    quantity = 1, production_cost = 0, commentary = "", \
                    isDone = False) -> None:

        self.name = name
        self.selling_cost = selling_cost
        self.production_cost = production_cost
        self.commentary = commentary
        self.isDone = isDone
        
        self.__steps = steps
    
        self.quantity = quantity

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
    def total_cost(self):
        return self.selling_cost * self.quantity
    
    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value : int):
        if value < 0:
            raise ValueError
        self.__quantity = value
        for step in self.GetSteps():
            step.quantity = value
    
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
        self.CheckIfDone()

    def DeleteStep(self, step_name: str):
        step_for_deletion = None
        for step in self.__steps:
            if step.name == step_name.lower():
                step_for_deletion = step
        
        if step_for_deletion != None:
            self.__steps.remove(step_for_deletion)
        self.CheckIfDone()

    def EvaluateSteps(self) -> None:
        base_value = self.__CountBaseVal()

        if base_value != None:
            for step in self.__steps:
                step.koef_value = base_value * step.complexity

    def CheckIfDone(self) -> bool:
        """проверяет Готовность всех шагов"""
        for step in self.GetSteps():
            if step.isDone == False:
                self.isDone = False
                return False
        self.isDone = True
        return True

    def __CountBaseVal(self) -> float:
        """Считает сколько стоит самый простой шаг в расчете на коичество единиц товара и возвращает значение между (0 , 1)"""
        total = 0.
        for step in self.__steps:
            total += step.complexity
        
        if total != 0:
            return 1 / total
        else:
            return None
                
    def __str__(self) -> str:
        """вывод инф-и о классе для отладки"""
        step_str = "\n".join(list(step.__str__() for step in self.GetSteps()))

        self.CheckIfDone()

        return f"Товар {self.name} стоит {self.selling_cost}. Для выполнения {self.quantity} штук нужно выполнить следующие шаги: \n{step_str}"
    
    def __hash__(self) -> int:
        return id(self)*self.selling_cost*self.quantity

    def __eq__(self, other):
        sc = self.__verify_data(other)
        return self.total_cost == sc.total_cost and self.quantity == sc.quantity and self.selling_cost == sc.selling_cost and self.production_cost == sc.production_cost
    
    def __lt__(self, other):
        sc = self.__verify_data(other)
        if self.total_cost == sc.total_cost:
            if self.selling_cost == sc.selling_cost:
                if self.production_cost == sc.production_cost:
                    if self.quantity == sc.quantity:
                        return False
                    return self.quantity < sc.quantity
                return self.production_cost < sc.production_cost
            return self.selling_cost < sc.selling_cost
        return self.total_cost < sc.total_cost
    
    def __gt__(self, other):
        sc = self.__verify_data(other)
        if self.total_cost == sc.total_cost:
            if self.selling_cost == sc.selling_cost:
                if self.production_cost == sc.production_cost:
                    if self.quantity == sc.quantity:
                        return False
                    return self.quantity > sc.quantity
                return self.production_cost > sc.production_cost
            return self.selling_cost > sc.selling_cost
        return self.total_cost > sc.total_cost
    
    def __le__(self, other):
        sc = self.__verify_data(other)
        return self < sc or self==sc
    
    def __ge__(self, other):
        sc = self.__verify_data(other)
        return self > sc or self==sc
    
    @classmethod
    def __verify_data(cls, other):
        if not isinstance(other, cls):
            raise TypeError(f"Операнд справа должен иметь тип {cls}")
        
        return other

    


    def toHTML(self) -> str:
        steps = "\n".join(list(step.toHTML() for step in self.GetSteps()))
        step_str = "<ul>\n" + steps + "\n</ul>"

        if self.CheckIfDone():
            beginning = f'<li class="green">Товар {self.name} выполнен. '
        else:
            beginning = f'<li class="red">Товар {self.name} не готов. '
        
        stroka = f"Стоимость {self.selling_cost}. <br>Для выполнения {self.quantity} штук нужно выполнить следующие шаги: \n{step_str}"

        text = beginning + stroka + "\n</li>"
        return text

    def toJSON(self):
        return json.dumps(self, cls=simpleEncoder, indent=4, ensure_ascii=False)
    
    def SaveAsTemplate(self) -> None:
        copy = deepcopy(self) # Чтобы не калечить нынешний товар

        for step in copy.GetSteps():
            step.GetContr().clear()

        filename = copy.name.lower() + ".json"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(copy.toJSON())
        
    @classmethod
    def fromTemplate(cls, template_name : str):
        """Возвращает объект по шаблону, не имеет каких-либо проверок на существование файла"""
        filename = template_name.lower()
        if not filename.endswith(".json"):
            filename = filename + ".json"

        with open(filename, "r", encoding="utf-8") as file:
            obj = Product.fromJSON(file.read())
        # если понадобится, то уже здесь можно будет кастомизировать Товар
        return obj

    @classmethod
    def fromJSON(cls, json_string : str):
        """Возвращает объект класса Product из строки(формата JSON)"""
        info = json.loads(json_string)
        
        return Product.fromDict(info)            

    @classmethod
    def fromDict(cls, info : dict):
        """Возвращает объект класса Product из словаря"""
        
        step_list = list(Step.fromDict(step) for step in info["steps"])

        return Product(name=info["name"], selling_cost=info["selling_cost"], steps=step_list, \
                        production_cost=info["production_cost"], commentary=info["commentary"], \
                        isDone=info["isDone"], quantity=info["quantity"])
    
