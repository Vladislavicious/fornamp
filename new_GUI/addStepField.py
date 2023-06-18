from typing import Tuple
from BaH.step import Step
from Caps.validator import Validator
from new_GUI.textField import TextField
from tkabs.frame import Frame
from UIadjusters.fontFabric import FontFabric
from uiabs.container import Container
from uiabs.editable import Editable


class addStepField(Frame, Editable):
    def __init__(self, parental_widget: Container, master: any,
                 step: Step = None, border_width: int | str | None = 2,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = None):

        Frame.__init__(self, parental_widget=parental_widget, master=master,
                       border_width=border_width, bg_color=bg_color,
                       fg_color=fg_color, border_color=border_color)
        Editable.__init__(self, parental_widget)

        self.step = step
        self.base_font = FontFabric.get_base_font()

        if self.step is not None:
            self.name_text = step.name
            self.complexity = str(step.complexity)
        else:
            self.name_text = ""
            self.complexity = ""

        self.initialize()

    def initialize(self) -> bool:
        if super().initialize():

            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_rowconfigure(0, weight=1)

            self.name_field = TextField(parental_widget=self, master=self.frame,
                                        validation_method=Validator.validate_name, title="Название шага",
                                        placeholder_text="Введите название", initial_text=self.name_text)
            self.name_field.frame.grid(row=0, column=0, padx=3, sticky="nsew")
            self.add_widget(self.name_field)

            self.complexity_field = TextField(parental_widget=self, master=self.frame,
                                              validation_method=Validator.validate_complexity,
                                              title="Сложность шага", initial_text=self.complexity,
                                              placeholder_text="Сложность от 1 до 5")
            self.complexity_field.frame.grid(row=1, column=0, padx=3, sticky="nsew")
            self.add_widget(self.complexity_field)

            return True
        return False

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
