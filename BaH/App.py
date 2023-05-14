"""Управляющий внутренностями класс"""
from typing import List

from BaH.order import Order
from BaH.order import OrderPreview
from Caps.fm import FileManager


class App:
    def __init__(self) -> None:
        self.file_manager = FileManager()

        self.order_previews = self.file_manager.parseOrderPreviews()     

        self.__orders = dict()

    @property
    def order_previews(self):
        """Список структур для предварительного просмотра заказа"""
        return self.__order_previews
    
    @order_previews.setter
    def order_previews(self, value: List[OrderPreview]):
        self.__order_previews = value

    def getOrderByID(self, ID: int):
        """Возвращает None, если Order не найден."""
        try:
            order = self.__orders[ID]
        except KeyError:
            order = self.__parseOrderByID(ID)
        
        return order
    
    def saveNewOrderPreviews(self):
        """Эта функция 'обновляет' файл в превью
           её надо вызывать при любых изменениях нынешних заказов
           или при появлении новых старых заказов
           то есть почти при каждом действии"""
        self.file_manager.saveOrderPreviewList(self.order_previews)
    
    def __getOrderPreviewIndexByID(self, ID: int):
        index = -1
        for i, ord_preview in enumerate(self.order_previews):
            if ord_preview.id == ID:
                index = i
                break
        return index

    def __parseOrderByID(self, ID: int):
        """Возвращает либо order, либо None"""
        order = self.file_manager.getOrderByID(ID)
        if order is not None:
            self.__orders[order.id] = order

        return order

    def addNewOrder(self, order: Order):
        self.__orders[order.id] = order
        self.order_previews.append(order.createPreview())
    
    def deleteOrderByID(self, ID: int) -> bool:
        """Возвращает True, если удаление прошло успешно
           Сам вызывает сохранение нужных файлов"""
        success = True
        if not self.file_manager.deleteOrderByID(ID):
            success = False

        index = self.__getOrderPreviewIndexByID(ID)
        
        if index != -1:
            self.order_previews.pop(index)
            self.saveNewOrderReviews()  
        else:
            success = False
        try:
            del self.__orders[ID]
        except KeyError:        # На случай, если мы ещё не загрузили в оперативу заказ
            success = False
        
        return success
    
    def saveOrder(self, order: Order):
        """Функция сохранения заказа в свой файл
           её необходимо вызывать при изменении заказа"""
        Order.toFile(order, self.file_manager.orders_dir_path)

    def saveOrderByID(self, ID: int):
        """то же, что и сверху"""
        order = self.__orders[ID]
        self.saveOrder(order)

        