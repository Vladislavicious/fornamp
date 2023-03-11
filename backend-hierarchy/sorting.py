from typing import List
from datetime import date
from dataclasses import dataclass

from step import *
from order import *
from listFuncs import *
from mail import *
from Contribution import *


@dataclass
class ContributionID:
    Order_id: int
    product_name: str
    step_name: str
    koef_value: int

def getContributionsByContributor(contributor: str, orderList: List[Order]):
    """Возвращает словарь Contribution : ContributionID"""
    dictionary = dict()
    
    for order in orderList:
        for product in order.GetProducts():
            for step in product.GetSteps():
                for contr in step.GetContr():
                    print(contr.__str__())
                    if contr.contributor == contributor:
                        dictionary[contr] = ContributionID(order.id, product.name, step.name, step.koef_value_done)
    
    return dictionary