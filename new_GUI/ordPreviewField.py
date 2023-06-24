from BaH.order import OrderPreview
from UIadjusters.colorFabric import ColorFabric
from tkabs.frame import Frame
from tkabs.label import Label
from UIadjusters.fontFabric import FontFabric
from uiabs.Container_tk import Container_tk


class OrderPreviewField(Frame):
    def __init__(self, parental_widget: Container_tk, master: any,
                 order_preview: OrderPreview):

        self.cf = ColorFabric()
        border_color = self.cf.undone
        border_width = self.cf.lines_width

        super().__init__(parental_widget, master, border_width=border_width,
                         border_color=border_color)
        self.order_preview = order_preview
        self.ff = FontFabric.get_instance()
        self.font = self.ff.get_base_font()

        self.initialize()

    @property
    def customer(self) -> str:
        return self.customer_label.contained_text

    def change_customer(self, customer: str):
        self.customer_label.change_text("Заказчик: " + customer)

    @property
    def date_of_vidacha(self) -> str:
        return self.date_of_vidacha_label.contained_text

    def change_date_ov(self, date: str):
        self.date_of_vidacha_label.change_text("Дата выдачи: " + date)

    def __configure_colors(self):
        if self.order_preview.isDone:
            if self.order_preview.isVidan:
                self.item.configure(border_color=self.cf.vidan)
            else:
                self.item.configure(border_color=self.cf.done)
        else:
            self.item.configure(border_color=self.cf.undone)

    def change_order_preview(self, order_preview: OrderPreview):
        self.order_preview = order_preview

        customer = order_preview.zakazchik
        date = order_preview.date_of_vidacha.strftime("%d/%m/%Y")
        self.change_customer(customer)
        self.change_date_ov(date)
        self.__configure_colors()

    def initialize(self) -> bool:
        if super().initialize():
            self.__configure_colors()
            self.item.rowconfigure(0, weight=1)
            self.item.rowconfigure(1, weight=1)
            self.item.rowconfigure(2, weight=1)

            self.item.columnconfigure(0, weight=1)

            self.item.configure(cursor="hand2")

            id = "id: " + str(self.order_preview.id)
            self.id_label = Label(self, self.item, text=id, font=self.font)
            self.id_label.item.grid(column=0, row=0, padx=5, pady=2, sticky="nw")
            self.add_widget(self.id_label)

            customer = "Заказчик: " + self.order_preview.zakazchik
            self.customer_label = Label(self, self.item, text=customer, font=self.font)
            self.customer_label.item.grid(column=0, row=1, padx=5, pady=2, sticky="w")
            self.add_widget(self.customer_label)

            date_of_vidacha = "Дата выдачи: " + \
                              self.order_preview.date_of_vidacha.strftime("%d.%m.%Y")
            self.date_of_vidacha_label = Label(self, self.item, text=date_of_vidacha, font=self.font)
            self.date_of_vidacha_label.item.grid(column=0, padx=5, pady=2, row=2, sticky="sw")
            self.add_widget(self.date_of_vidacha_label)

            return True
        return False
