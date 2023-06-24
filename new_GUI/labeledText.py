
from UIadjusters.fontFabric import FontFabric
from tkabs.frame import Frame
from tkabs.label import Label
from uiabs.container_tk import Container_tk


class labeledText(Frame):
    def __init__(self, parental_widget: Container_tk, master: any, title: str,
                 initial_text: str = "", width: int = 250, **kwargs):

        super().__init__(parental_widget, master, width=width, **kwargs)

        self.initial_text = initial_text
        self.title_text = title

        self.ff = FontFabric.get_instance()
        self.font = self.ff.get_base_font()
        self.initialize()

    def change_title(self, title: str):
        self.title_text = title
        self.title_label.item.configure(text=title)

    def change_text(self, text: str):
        self.initial_text = text
        self.text_label.item.configure(text=text)

    def get(self) -> str:
        return self.initial_text

    def initialize(self) -> bool:
        if super().initialize():
            self.item.grid_columnconfigure(0, weight=1)
            self.item.grid_rowconfigure(0, weight=1)
            self.item.grid_rowconfigure(1, weight=3)
            self.item.grid_propagate(True)

            self.title_label = Label(parental_widget=self, master=self.item,
                                     text=self.title_text,
                                     font=self.ff.get_changed_font(weight='bold'))
            self.title_label.item.grid(row=0, column=0, sticky="nsew")
            self.add_widget(self.title_label)

            self.text_label = Label(parental_widget=self, master=self.item,
                                    text=self.initial_text, font=self.font)
            self.text_label.item.grid(row=1, column=0, sticky="nsew")
            self.add_widget(self.text_label)

            return True
        return False

    def draw(self):
        pass

    def erase(self):
        pass
