from new_GUI.labeledText import labeledText
from new_GUI.textField import TextField
from tkabs.label import Label
from tkabs.slider import Slider
from UIadjusters.fontFabric import FontFabric
from tkabs.frame import Frame
from uiabs.container_tk import Container_tk
from uiabs.editable import Editable
from Caps.validator import Validator


class Runner(Frame, Editable):
    def __init__(self, parental_widget: Container_tk, master: any, runner_title: str,
                 from_value: int = 0, to_value: int = 1, steps_count: int = 0,
                 width: int = 100, height: int = 100,
                 border_width: int | None = None,
                 bg_color: str | None = None,
                 fg_color: str | None = None,
                 border_color: str | None = None):

        Frame.__init__(self, parental_widget=parental_widget, master=master,
                       width=width, height=height,
                       border_width=border_width, bg_color=bg_color,
                       fg_color=fg_color, border_color=border_color)
        Editable.__init__(self, parental_unit=parental_widget)
        if from_value < 0:
            from_value = 0
        if to_value < 1:
            to_value = 1
        if to_value == from_value:
            to_value += 1
        if to_value < from_value:
            (to_value, from_value) = (to_value, from_value)
            print("Очень плохие данные в слайдере")
        if steps_count <= 0:
            steps_count = to_value + 1

        self.ff = FontFabric.get_instance()
        self.font = self.ff.get_base_font()
        self.steps_count = steps_count
        self.from_value_text = str(from_value)
        self.to_value_text = str(to_value)
        self.runner_title_text = runner_title

        self.initialize()

    @property
    def slider_value(self):
        return self.slider.slider_value

    @property
    def from_value(self) -> str:
        return self.from_field.get()

    @from_value.setter
    def from_value(self, text: str):
        self.from_field.change_text(text)

    @property
    def to_value(self) -> str:
        return self.to_field.get()

    def initialize(self) -> bool:
        if super().initialize():
            self.item.grid_rowconfigure(1, weight=1)
            self.item.grid_columnconfigure(1, weight=1)
            self.item.grid_propagate(False)

            self.runner_title = Label(parental_widget=self, master=self.item,
                                      text=self.runner_title_text, font=self.ff.get_bold_font())
            self.runner_title.item.grid(row=0, columnspan=3, padx=2)
            self.add_widget(self.runner_title)

            self.from_field = TextField(parental_widget=self, master=self.item,
                                        title="От", width=30,
                                        validation_method=lambda value:
                                        Validator.validate_number(string=value, name="От", min_number=0),
                                        initial_text=self.from_value_text,
                                        enter_pressed_function=self.confirm)
            self.from_field.item.grid(row=1, column=0, padx=2)
            self.add_widget(self.from_field)

            from_int = int(self.from_value_text)
            to_int = int(self.to_value_text)
            self.slider = Slider(parental_widget=self, master=self.item,
                                 from_=0, to=to_int, height=25, width=550,
                                 number_of_steps=self.steps_count, state="normal",
                                 command=self.__slider_change)
            self.slider.item.set(from_int)
            self.slider.item.grid(row=1, column=1, sticky="ew")
            self.add_widget(self.slider)

            self.to_field = labeledText(parental_widget=self, master=self.item,
                                        title="До", initial_text=self.to_value_text)
            self.to_field.item.grid(row=1, column=2, padx=2)
            self.add_widget(self.to_field)

            return True
        return False

    def __slider_change(self, value):
        self.from_field.change_text(str(int(value)))
        self.from_field.edit()
        self.from_field.text_entry.item.focus()

    def edit(self):
        for field in self.get_class_instances(Editable):
            field.edit()
        Editable.edit(self)

    def confirm(self):
        if self.from_field.confirm():
            from_field_value = int(self.from_field.get())
            self.slider.set_value(from_field_value)
            self.set_as_edited()
            self.slider.confirm()
            Editable.confirm(self)

    def draw(self):
        self.from_field.show()
