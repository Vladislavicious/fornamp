from typing import Tuple
from ioconnection.App import App
from BaH.step import Step
from new_GUI.runner import Runner
from new_GUI.textField import TextField
from tkabs.frame import Frame
from UIadjusters.fontFabric import FontFabric
from uiabs.container import Container
from uiabs.editable import Editable


def is_valid_string(s):
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя.,:/" ')
    return all(c in allowed_chars for c in s)


def validate_name(string: str = "") -> Tuple[bool, str]:
    """Проверяет строку на соответствие параметрам"""
    length = len(string)
    if length < 2:
        return False, "Название слишком короткое"
    if length > 32:
        return False, "Название слишком длинное"
    if not is_valid_string(string.lower()):
        return False, "Содержит неподобающие символы"
    return True, ""


class stepField(Frame, Editable):
    def __init__(self, parental_widget: Container, master: any, step: Step,
                 border_width: int | str | None = 2,
                 bg_color: str | Tuple[str, str] = "transparent",
                 fg_color: str | Tuple[str, str] | None = None,
                 border_color: str | Tuple[str, str] | None = "#B22222"):

        Frame.__init__(self, parental_widget=parental_widget, master=master,
                       border_width=border_width, bg_color=bg_color,
                       fg_color=fg_color, border_color=border_color)
        Editable.__init__(self, parental_widget)

        self.step = step
        self.base_font = FontFabric.get_base_font()

        if self.step is not None:
            self.name_text = step.name
            self.quantity = step.quantity
            self.number_of_made = step.number_of_made
        else:
            self.name_text = ""
            self.quantity = 0
            self.number_of_made = 0

        self.runner = None

    def initialize(self) -> bool:
        if super().initialize():

            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_rowconfigure(0, weight=1)

            self.name_field = TextField(parental_widget=self, master=self.frame,
                                        validation_method=validate_name, title="Название шага",
                                        placeholder_text="Введите название", initial_text=self.name_text)
            self.name_field.frame.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
            self.add_widget(self.name_field)

            from_value = 0
            to_value = self.quantity - self.number_of_made
            if to_value > 0:
                self.runner = Runner(parental_widget=self, master=self.frame, runner_title="Выполнить:",
                                     from_value=from_value, to_value=to_value, steps_count=to_value)
                self.runner.frame.grid(row=1, column=0, padx=5, pady=3, sticky="nsew")
                self.add_widget(self.runner)

            if self.step.isDone:
                self.__configure_as_done()

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

    def __configure_as_done(self):
        self.frame.configure(border_color="#7FFF00")
        if self.runner is not None:
            self.runner.hide()

    def __assemble_step(self):
        if self.step.isDone:
            return

        max_contr_value = int(self.runner.to_value)

        contribution = int(self.runner.from_value)

        if contribution > max_contr_value:
            self.runner.from_value = self.runner.to_value
            contribution = max_contr_value

        self.number_of_made += contribution

        app_reference = App()

        username = app_reference.current_user.login

        self.step.Contribute(username, contribution)

        if self.step.isDone:
            self.__configure_as_done()
