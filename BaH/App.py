"""Управляющий внутренностями класс"""
from email.mime.multipart import MIMEMultipart
import os
from typing import List, Tuple

from BaH.order import Order, OrderPreviewSorter
from BaH.order import OrderPreview
from BaH.product import Product
from BaH.user import User
from Caps.fm import FileManager
from Caps.mail import MailAccount


class App:
    def __init__(self) -> None:
        self.file_manager = FileManager()

        self.order_previews = self.file_manager.parseOrderPreviews()

        self.product_templates = self.file_manager.parseTemplates()

        self.__orders = dict()

    def destroy(self):
        """Вызывается при закрытии приложения
           сохраняет всё, что ещё не было сохранено"""
        self.__saveNewOrderPreviews()
        self.__saveTemplates()
        self.file_manager.clearOrderFilenames()
        self.__clearOrderPreviews()
        self.__clearOrders()
        self.__clearProductTemplates()

    @property
    def current_user(self) -> User:
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
    def sorted_order_previews(self) -> List[OrderPreview]:
        """Список структур для предварительного просмотра заказа
           по умолчанию возвращает отсортированным"""
        sorted_previews = OrderPreviewSorter.Multisort(self.__order_previews,
                                                       [("isVidan", True), ("isDone", True),
                                                        ("date_of_vidacha", False)])
        self.order_previews = sorted_previews
        return sorted_previews

    @property
    def order_previews(self) -> List[OrderPreview]:
        """Список структур для предварительного просмотра заказа"""
        return self.__order_previews

    @order_previews.setter
    def order_previews(self, value: List[OrderPreview]):
        self.__order_previews = value

    def __clearOrderPreviews(self):
        self.__order_previews.clear()

    @property
    def product_templates(self) -> List[Product]:
        """Список шаблонов товаров"""
        return self.__product_templates

    @product_templates.setter
    def product_templates(self, value: List[Product]):
        self.__product_templates = value

    def __clearProductTemplates(self):
        self.__product_templates.clear()

    def makeNewProductTemplate(self, product: Product):
        """Вызывается для добавления нового шаблона
           Не добавляет шаблон, если уже существует шаблон
           с таким именем"""
        template = product.GetAsTemplate()
        isViable = True
        for templ in self.__product_templates:
            if templ.name == template.name:
                isViable = False
        
        if isViable:
            self.product_templates.append(template)

    def deleteTemplate(self, template: Product) -> bool:
        index = -1
        for i, prod in enumerate(self.product_templates):
            if prod == template:
                index = i
                break
        if index == -1:
            return False
        self.product_templates.pop(index)
        return True

    def __saveTemplates(self):
        """Сохраняет шаблоны
           Вызывается при закрытии приложения"""
        self.file_manager.saveTemplates(self.product_templates)

    def getOrderByID(self, ID: int):
        """Возвращает None, если Order не найден."""
        try:
            order = self.__orders[ID]
        except KeyError:
            order = self.__parseOrderByID(ID)

        if order is not None:    # Проверяется на случай, если заказ был изменён извне приложения
            previous_state = order.isDone
            if previous_state is not order.CheckIfDone():
                self.saveOrder(order)

        return order

    def __clearOrders(self):
        self.__orders.clear()

    def __mergeOrders(self, orders: List[Order]):
        self.__orders = self.__orders | orders

    def __saveNewOrderPreviews(self):
        """Эта функция 'обновляет' файл в превью
           вызывается при закрытии приложения"""
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

        self.file_manager.saveOrder(order)

    def deleteOrderByID(self, ID: int) -> Tuple[bool, bool, bool]:
        """Возвращает три була, если bool is True, то удаление успешно.
           Первый бул - удаление как файла
           Второй бул - удаление как Превью Заказа
           Третий бул - удаление заказа из оперативной памяти
           Сам вызывает сохранение нужных файлов"""
        success1 = success2 = success3 = True
        if not self.file_manager.deleteOrderByID(ID):
            success1 = False

        index = self.__getOrderPreviewIndexByID(ID)

        if index != -1:
            self.order_previews.pop(index)
            self.__saveNewOrderPreviews()
        else:
            success2 = False
        try:
            del self.__orders[ID]
        except KeyError:        # На случай, если мы ещё не загрузили в оперативу заказ
            success3 = False

        return (success1, success2, success3)

    def PreChangeOrderDir(self):
        """Вызывается перед изменением папки хранения заказов"""
        self.destroy()

    def PostChangeOrderDir(self):
        """Вызывается сразу после изменения папки хранения заказов"""
        self.order_previews = self.file_manager.parseOrderPreviews()
        self.product_templates = self.file_manager.parseTemplates()

    def saveOrder(self, order: Order):
        """Функция сохранения заказа в свой файл
           её необходимо вызывать при изменении существующего заказа"""
        self.file_manager.saveOrder(order)
        index = self.__getOrderPreviewIndexByID(order.id)
        self.order_previews[index] = order.createPreview()

    def saveOrderByID(self, ID: int):
        """то же, что и сверху"""
        order = self.__orders[ID]
        self.saveOrder(order)

    def AuthentificateMail(self) -> Tuple[int, str]:
        """Возвращает 0 при успешном входе; 1 при отсуствии данных о почте;
           2 при неудачном входе."""

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
        orders_dict = dict(list((order.id, order) for order in orders))

        self.__mergeOrders(orders_dict)

        message = self.mail_account.createMessage(TO=TO, message=msg_text,
                                                  filepaths=[filepath])

        os.remove(filepath)

        return message

    def __sendMail(self, message: MIMEMultipart):
        self.mail_account.sendMessage(message)

    def sendOtchetMail(self, TO: str, msg_text: str = "") -> Tuple[int, str]:
        """Функция, которая отправляет на указанную почту сообщение с прикреплённым
           html-файлом со всеми заказами.
           перед использованием необходимо вызвать функцию AuthentificateMail"""
        if self.mail_account.smtp is None:
            return (1, "Аккаунт почты не авторизован")

        message = self.__CreateOtchetMessage(TO=TO, msg_text=msg_text)
        self.__sendMail(message=message)

        return (0, "Успешно")
