from BaH.step import Step
from Caps.validator import Validator
from new_GUI.textField import TextField
from tkabs.button import Button
from tkabs.frame import Frame
from UIadjusters.fontFabric import FontFabric
from uiabs.container import Container
from uiabs.editable import Editable


class addStepField(Frame, Editable):
    def __init__(self, parental_widget: Container, master: any,
                 step: Step = None):

        Frame.__init__(self, parental_widget=parental_widget, master=master)
        Editable.__init__(self, parental_widget)

        self.step = step
        self.ff = FontFabric.get_instance()
        self.font = self.ff.get_base_font()

        if self.step is not None:
            self.name_text = step.name
            self.complexity = str(step.complexity)
        else:
            self.name_text = ""
            self.complexity = ""

        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():

            self.item.grid_columnconfigure(0, weight=1)

            self.delete_button = Button(parental_widget=self, master=self.item, text="удалить",
                                        command=self.__self_delete, font=self.font, width=40,
                                        fg_color="#AA0A00", hover_color="#AA0AE0")
            self.delete_button.item.grid(row=0, column=0, padx=3, pady=3, sticky="nw")
            self.add_widget(self.delete_button)

            self.name_field = TextField(parental_widget=self, master=self.item,
                                        validation_method=Validator.validate_name, title="Название шага",
                                        placeholder_text="Введите название", initial_text=self.name_text)
            self.name_field.item.grid(row=1, column=0, padx=3, sticky="nsew")
            self.add_widget(self.name_field)

            self.complexity_field = TextField(parental_widget=self, master=self.item,
                                              validation_method=Validator.validate_complexity,
                                              title="Сложность шага", initial_text=self.complexity,
                                              placeholder_text="Сложность от 1 до 5")
            self.complexity_field.item.grid(row=2, column=0, padx=3, sticky="nsew")
            self.add_widget(self.complexity_field)

            return True
        return False

    def __self_delete(self):
        self.hide()
        self.set_as_edited()
        self.parental_widget.delete_widget(self)

    def edit(self):
        for widget in self.get_class_instances(Editable):
            widget.edit()
        Editable.edit(self)

    def confirm(self) -> bool:
        is_confirmed = True
        for widget in self.get_class_instances(Editable):
            widget.confirm()
            if widget.is_confirmed is False:
                is_confirmed = False

        if is_confirmed:
            Editable.confirm(self)
            self.set_as_edited()
            return True
        return False

    def save(self):
        print("Сохраняю шаг")
        for widget in self.get_class_instances(Editable):
            widget.save()
        if Editable.save(self):
            self.__assemble_step()
            return True
        return False

    def __assemble_step(self):
        name = self.name_field.get()
        complexity = int(self.complexity_field.get())
        self.step = Step(name, complexity=complexity)
