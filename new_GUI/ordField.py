"""
Класс, наследуемый от Frame, получающий на вход OrderPreview
При нажатии на любую часть фрейма, вызывается функция order_field_press(self, order_id: int),
эта функция, в свою очередь, вызывает функцию открытия open_order(order: Order) этого заказа в MainWindow,
которая открывает окно с заказом, а себя hide.
"""
from customtkinter import CTkFont
from BaH.order import OrderPreview
from tkabs.frame import Frame
from tkabs.label import Label
from uiabs.container import Container


def shorter(string: str, length: int = 60) -> str:
    string_len = len(string)

    new_string = "\n".join(list([string[i:i + length] for i in range(0, string_len, length)]))
    return new_string


class OrderField(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 order_preview: OrderPreview):
        border_width = 2
        border_color = "#B22222"
        super().__init__(parental_widget, master, border_width=border_width,
                         border_color=border_color)
        self.order_preview = order_preview
        self.base_font = CTkFont(family="Century gothic", size=16)

        self.initialize()

    def __configure_string_length(self, string: str):

        string_length = len(string)
        if string_length > 60:
            new_string_length = 60
            return shorter(string, new_string_length)
        return string

    def initialize(self) -> bool:
        if super().initialize():
            if self.order_preview.isDone:
                if self.order_preview.isVidan:
                    self.frame.configure(border_color="#7FFF00")
                else:
                    self.frame.configure(border_color="#FFA500")

            self.frame.rowconfigure(0, weight=1)
            self.frame.rowconfigure(1, weight=1)
            self.frame.rowconfigure(2, weight=1)

            self.frame.columnconfigure(0, weight=1)

            id = "id: " + str(self.order_preview.id)
            self.id_label = Label(self, self.frame, text=id, font=self.base_font)
            self.id_label.label.grid(column=0, row=0, padx=5, pady=2, sticky="nw")
            self.add_widget(self.id_label)

            customer = "Заказчик: " + self.order_preview.zakazchik
            self.customer_label = Label(self, self.frame, text=customer, font=self.base_font)
            self.customer_label.label.grid(column=0, row=1, padx=5, pady=2, sticky="w")
            self.add_widget(self.customer_label)

            date_of_vidacha = "Дата выдачи: " + \
                              self.order_preview.date_of_vidacha.strftime("%d.%m.%Y")
            self.date_of_vidacha = Label(self, self.frame, text=date_of_vidacha, font=self.base_font)
            self.date_of_vidacha.label.grid(column=0, padx=5, pady=2, row=2, sticky="sw")
            self.add_widget(self.date_of_vidacha)

            return True
        return False
