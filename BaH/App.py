"""Управляющий внутренностями класс"""
from email.mime.multipart import MIMEMultipart
import os
from typing import List, Tuple

from BaH.order import Order
from BaH.order import OrderPreview
from Caps.fm import FileManager
from Caps.mail import MailAccount


class App:
    def __init__(self) -> None:
        self.file_manager = FileManager()

        self.order_previews = self.file_manager.parseOrderPreviews()     

        self.__orders = dict()

    @property
    def current_user(self):
        return self.file_manager.user_handler.lastUser

    @property
    def mail_account(self) -> MailAccount:
        return self.__mail_account

    @mail_account.setter
    def mail_account(self, value: Tuple[str, str]):
        login, password = value
        if login != "" and password != "":
            self.__mail_account = MailAccount(login, password)
        else:
            self.__mail_account = None

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

    def mergeOrders(self, orders: List[Order]):
        self.__orders = self.__orders | orders

    def saveNewOrderPreviews(self):
        """Эта функция 'обновляет' файл в превью
           её надо вызывать при любых изменениях нынешних заказов
           или при появлении новых заказов,
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
        """Возвращает Order, либо None"""
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

    def AuthentificateMail(self) -> Tuple[int, str]:
        """Возвращает 0 при успешном входе, 1 при отсуствии данных о почте
           2 при неудачном входе"""

        self.mail_account = (self.current_user.email,
                             self.current_user.emailpassword)

        if self.mail_account is None:
            return (1, "Данные почты не введены")

        is_authentificated, error_msg = self.mail_account.authentificate()

        if is_authentificated is True:
            return (0, "Успешно")
        else:
            return (2, error_msg)

    def __CreateOtchetMessage(self, TO: str, msg_text: str = ""):
        orders, filepath = self.file_manager.CreateStatusHTML()
        dict()
        orders_dict = dict(list((order.id, order) for order in orders))

        self.mergeOrders(orders_dict)

        message = self.mail_account.createMessage(TO=TO, message=msg_text,
                                                  filepaths=[filepath])

        os.remove(filepath)

        return message

    def __sendMail(self, message: MIMEMultipart):
        self.mail_account.sendMessage(message)

    def sendOtchetMail(self, TO: str, msg_text: str = "")  -> Tuple[int, str]:
        """Функция, которая отправляет на указанную почту сообщение с прикреплённым
           html-файлом со всеми заказами.
           перед использованием необходимо вызвать функцию AuthentificateMail"""
        if self.mail_account.smtp is None:
            return (1, "Аккаунт почты не авторизован")

        message = self.__CreateOtchetMessage(TO=TO, msg_text=msg_text)
        self.__sendMail(message=message)

        return (0, "Успешно")
