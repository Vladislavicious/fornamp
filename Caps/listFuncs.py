"""Функции для работы со списком заказов"""
import json
from typing import List

from BaH.order import Order
from BaH.order import simpleEncoder


def listToHTML(orders: List[Order], title: str = "Отчёт") -> str:
    """Возвращает текст в формате HTML"""
    greentext = ""
    redtext = ""
    beggining = '<div class="container">\n'
    ending = "</div>"

    for order in orders:
        txt = beggining + order.toHTML() + ending
        if order.isDone and (not order.isVidan):
            greentext = greentext + txt
        else:
            redtext = redtext + txt
        
    text = \
    '<!DOCTYPE html>' + "\n"\
    '<html lang="ru" dir="ltr">' + "\n\n"\
    '<head>' + "\n"\
    '<meta http-equiv="Content-Type" content="text/html"; charset="utf-8" />' + "\n"\
    '<link rel="stylesheet" type="text/css" href="https://raw.githack.com/Vladislavicious/factory-engine/d3ba80a8ff5b191ecb327a7b3c3ae146404b8fff/web/Styles.css">' + "\n"\
    f'<title>{title}</title>' + "\n\n"\
    '</head>' + "\n"\
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


def listToPlainHTML(orders: List[Order], title: str = "Отчёт") -> str:
    """Возвращает текст в формате HTML с вложенными стилями"""
    greentext = ""
    redtext = ""
    beggining = '<div class="container">\n'
    ending = "</div>"

    for order in orders:
        txt = beggining + order.toHTML() + ending
        if order.isDone and (not order.isVidan):
            greentext = greentext + txt
        else:
            redtext = redtext + txt
        
    text = \
    '<!DOCTYPE html>' + "\n"\
    '<html lang="ru" dir="ltr">' + "\n\n"\
    '<head>' + "\n"\
    '<meta http-equiv="Content-Type" content="text/html"; charset="utf-8" />' + "\n"\
    '<style type="text/css">' + "\n"\
    '* {margin: 0;padding: 0;box-sizing: border-box;}' + "\n"\
    'main {display: flex;flex: 1;}' + "\n"\
    'aside {flex: 1;}' + "\n"\
    'section {flex: 3;}' + "\n"\
    '.flex-container {display: flex;flex-direction: column;min-height: 100vh;background: linear-gradient(70deg, #f7c6c6, #3d36f5, #fb83e5, #6cfa9b);}' + "\n"\
    '.flex-item {padding: 10px;font: 900 15px "Roboto", sans-serif;color: #fdfafa;text-align: center;text-shadow: 2px 1px 0 rgba(0, 0, 0, 0.2);}' + "\n"\
    '.green-container .container{background-color: #69fc9a;}' + "\n"\
    '.red-container .container{background-color: #f86d72;}' + "\n"\
    '.container{border: 1px solid black;margin: 1px;padding: 5px;}' + "\n"\
    '.green{color: rgb(0, 108, 0);}' + "\n"\
    '.red{color: rgb(210, 2, 2);}' + "\n"\
    'ol {text-align: left;margin-left: 20px;margin-top: 1em;}' + "\n"\
    'ol ul {margin-left: 20px;}' + "\n"\
    '@media screen and (max-width: 650px) {main {flex-direction: column;}}' + "\n"\
    '</style>' + "\n"\
    f'<title>{title}</title>' + "\n\n"\
    '</head>' + "\n"\
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


def listToFile(orders: List[Order], directory: str):
    for order in orders:
        order.toFile(directory)


def listToJSON(orders: List[Order]) -> str:
    return json.dumps(orders, cls=simpleEncoder, sort_keys=True, indent=4, ensure_ascii=False)


def listToJSONfile(orders: List[Order], filename: str):
    filepath = filename.lower()
    if not filename.endswith(".json"):
        filepath += ".json"
    
    with open(filepath, "w", encoding="utf-8") as opened_file:
        opened_file.write(listToJSON(orders))


def listFromJSONfile(filename: str) -> List[Order]:
    filepath = filename.lower()
    if not filename.endswith(".json"):
        filepath += ".json"
    
    with open(filepath, "r", encoding="utf-8") as opened_file:
        loaded_list = json.load(opened_file)
        
    return listFromJSONstr(loaded_list)


def listFromJSONstr(info: list) -> List[Order]:
    list_of_orders = list()
    for order in info:
        list_of_orders.append(Order.fromDict(order))
        
    return list_of_orders


def createHTMLfromJSON(jsonPath: str, htmlPath: str, htmlTitle: str = "Отчёт"):
    content = listToPlainHTML(listFromJSONfile(jsonPath), htmlTitle)

    with open(htmlPath, "w", encoding="utf-8") as file:
        file.write(content)


def createHTMLfromList(orders: List[Order], htmlPath: str, htmlTitle: str = "Отчёт"):
    """Сохраняет HTML файл по указанному пути"""
    content = listToPlainHTML(orders, htmlTitle)

    filepath = htmlPath.lower()
    if not htmlPath.endswith(".html"):
        filepath += ".html"

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)


def ContributionsFromOrdersList(orders: List[Order]):
    Contrs = list()
    for order in orders:
        for product in order.GetProducts():
            for step in product.GetSteps():
                Contrs = Contrs + step.GetContr()
    
    return Contrs


def StepsFromOrdersList(orders: List[Order]):
    Steps = list()
    for order in orders:
        for product in order.GetProducts():
            Steps = Steps + product.GetSteps()
    
    return Steps


def ProductsFromOrdersList(orders: List[Order]):
    Products = list()
    for order in orders:
        Products = Products + order.GetProducts()
    
    return Products