from BaH.order import OrderPreview
from tkabs.frame import Frame
from tkabs.label import Label
from tkabs.fontFabric import FontFabric
from uiabs.container import Container


class OrderPreviewField(Frame):
    def __init__(self, parental_widget: Container, master: any,
                 order_preview: OrderPreview):
        border_width = 2
        border_color = "#B22222"
        super().__init__(parental_widget, master, border_width=border_width,
                         border_color=border_color)
        self.order_preview = order_preview
        self.base_font = FontFabric.get_base_font()

        self.initialize()

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
