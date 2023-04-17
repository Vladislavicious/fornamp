"""функции для сортировки заказов и их составляющих"""
import pandas as pd
from typing import List
from typing import Dict
from dataclasses import dataclass
from collections import defaultdict

from BaH.step import *
from BaH.order import *
from BaH.Contribution import *


@dataclass
class ContrID:
    """Структура для нахождения контрибушна в списке заказов"""
    Order_id: int
    product_name: str
    step_name: str
    koef_value: int


def getContributionsByContributor(contributor: str, orderList: List[Order]) -> Dict[Contribution, ContrID]:
    """Возвращает словарь Contribution : ContrID"""
    dictionary = dict()
    
    for order in orderList:
        for product in order.GetProducts():
            for step in product.GetSteps():
                for contr in step.GetContr():
                    if contr.contributor == contributor:
                        dictionary[contr] = ContrID(order.id, product.name, step.name, step.koef_value_done)
    
    return dictionary

def getKoefSum(dictionary: Dict[Contribution, ContrID]) -> pd.Series:
    """Возвращает словарь Дата : выполненные коэф-ты"""
    koef_dict = defaultdict(lambda: 0.)
    for index in dictionary.keys():
        koef_dict[index.date_of_creation] += dictionary[index].koef_value

    
    koef_series = pd.Series(koef_dict).sort_index() 
    koef_series.index = pd.to_datetime(koef_series.index)

    for contr, contrID in dictionary.items():
        koef_series.name = contr.contributor
        break
    return koef_series