import json
from typing import List

from order import Order
from order import simpleEncoder

def listToHTML(orders : List[Order], title: str = "Отчёт") -> str:

    greentext = ""
    redtext = ""
    beggining = '<div class="container">\n'
    ending = "</div>"

    for order in orders:
        txt = beggining + order.toHTML() + ending
        if order.isDone:
            greentext = greentext + txt
        else:
            redtext = redtext + txt
        
    text = \
    '<!DOCTYPE html>' + "\n"\
    '<html lang="ru" dir="ltr">' + "\n\n"\
    '<head>' + "\n"\
    '<meta charset="utf-8" />' + "\n"\
    '<link rel="stylesheet" type="text/css" href="Styles.css">' + "\n"\
    f'<title>{title}</title>' + "\n\n"\
    '<body>' + "\n"\
    '<div class="flex-container">' + "\n"\
    '<main>' + "\n"\
    '<section class="flex-item green-container">' + "\n"\
    f'{greentext}' + "\n"\
    '</section>' + "\n"\
    '<section class="flex-item red-container">' + "\n"\
    f'{redtext}' + "\n"\
    '</section>' + "\n"\
    '</main>' + "\n"\
    '</div>' + "\n"\
    '</body>' + "\n\n"\
    '</html>'

    return text
    

def listToJSON(orders : List[Order]) -> str:
    return json.dumps(orders, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)

def listFromJSONfile(filename : str) -> List[Order]:
    filepath = filename.lower()
    if not filename.endswith(".json"):
        filepath += ".json"
    
    with open(filepath, "r", encoding="utf-8") as opened_file:
        loaded_list = json.load(opened_file)
        
    return listFromJSONstr(loaded_list)

def listFromJSONstr(info : list) -> List[Order]:
    list_of_orders = list()
    for order in info:
        list_of_orders.append(Order.fromDict(order))
        
    return list_of_orders