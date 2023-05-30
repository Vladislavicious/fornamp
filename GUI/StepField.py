import tkinter as tk
import customtkinter as ctk

from BaH.product import Product
from BaH.step import Step


class StepField():     # класс отображения шага в приложении
    def __init__(self, app, master, add_window, parental_product: Product,
                 step: Step = None, personal_number: int = 1) -> None:

        self.main_window = app
        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        ###
        self.add_window = add_window
        self.parental_product = parental_product
        self.step = step
        self.personal_number = personal_number      # Какой это шаг в колонке
        self.master = master      # Колонка в которую закрепляемся, по сути window_add.scroll_step
        ###

        self.name_text = ""
        self.complexity_text = ""
        if self.step is not None:
            self.name_text = self.step.name
            self.complexity_text = str(self.step.complexity)

        self.color_button = "#3b8ed0"
        self.text_button = "Применить"
        self.state_entry = "normal"
        self.is_saved: bool = False  # 0- не сохранено 1 - сохранено 2 - редактируется

        self.label_count: ctk.CTkLabel
        self.frame_step_field: ctk.CTkFrame
        self.label_name: ctk.CTkLabel
        self.entry_name: ctk.CTkEntry
        self.label_complexity: ctk.CTkLabel
        self.entry_complexity: ctk.CTkEntry
        self.label_commentariy: ctk.CTkLabel
        self.entry_commentariy: ctk.CTkEntry

        self.button_aply: ctk.CTkButton
        self.button_delete: ctk.CTkButton

        self.add_step()

    def add_step(self):     # создание поля нового пустого шага
        self.label_count = ctk.CTkLabel(self.master, text="Шаг № " + str(self.personal_number),
                                        font=self.font_)
        self.label_count.pack(anchor=tk.CENTER, pady=5)

        self.frame_step_field = ctk.CTkFrame(self.master, border_width=2, width=350, height=190)
        self.frame_step_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_step_field.pack_propagate(False)

        self.label_name = ctk.CTkLabel(self.frame_step_field, text="Введите название шага", font=self.fontmini)
        self.label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name = ctk.CTkEntry(self.frame_step_field)
        self.entry_name.insert(0, self.name_text)
        self.entry_name.pack(fill=tk.X, pady=5, padx=5)
        self.entry_name.configure(state=self.state_entry)

        self.label_complexity = ctk.CTkLabel(self.frame_step_field, text="Введите сложность шага (от 1 до 5)",
                                             font=self.fontmini)
        self.label_complexity.pack(anchor=tk.CENTER, pady=5)

        self.entry_complexity = ctk.CTkEntry(self.frame_step_field)
        self.entry_complexity.insert(0, self.complexity_text)
        self.entry_complexity.pack(fill=tk.X, pady=5, padx=5)
        self.entry_complexity.configure(state=self.state_entry)

        if self.is_saved is False:
            self.button_aply = ctk.CTkButton(self.frame_step_field, text=self.text_button,
                                             fg_color=self.color_button, command=self.apply)
        else:
            self.button_aply = ctk.CTkButton(self.frame_step_field, text=self.text_button,
                                             fg_color=self.color_button, hover_color="#189e3b", command=self.edit)
        self.button_aply.pack(side=tk.LEFT, padx=10)

        self.button_delete = ctk.CTkButton(self.frame_step_field, text="Удалить", command=self.destroy,
                                           fg_color="#d9071c", hover_color="#ad0314")

        self.button_delete.pack(side=tk.RIGHT, padx=10)

    def apply(self):     # кнопка подтверждения шага и добавление его в список
        if self.check_field() is True:
            self.step = Step(name=self.name_text, quantity=self.parental_product.quantity,
                             complexity=int(self.complexity_text))

            self.is_saved = True
            self.color_button = "#2dba52"
            self.text_button = "Редактировать"
            self.button_aply.configure(fg_color=self.color_button, hover_color="#189e3b",
                                       text=self.text_button, command=self.edit)

            self.state_entry = "disabled"
            self.entry_name.configure(state=self.state_entry)
            self.entry_complexity.configure(state=self.state_entry)

    def edit(self):
        self.button_aply.configure(fg_color="#3b8ed0", hover_color="#36719f",
                                   text="Применить", command=self.apply_edit)
        self.entry_name.configure(state="normal")
        self.entry_complexity.configure(state="normal")
        self.is_saved = False

    def apply_edit(self):
        if self.check_field() is True:
            complexity = int(self.complexity_text)
            self.step.complexity = complexity

            self.step.name = self.name_text

            self.entry_name.configure(state="disabled")
            self.entry_complexity.configure(state="disabled")
            self.button_aply.configure(fg_color="#2dba52", hover_color="#189e3b",
                                       text="Редактировать", command=self.edit)
            self.is_saved = True

    def destroy(self):
        self.label_count.destroy()
        self.frame_step_field.destroy()

    def check_field(self):   # проверка на введеные поля
        check = True
        if self.entry_name.get() == "":
            self.entry_name.configure(fg_color="#faebeb", border_color="#e64646",
                                      placeholder_text="Заполните все поля", placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        elif len(self.entry_name.get()) > 25:
            self.entry_name.delete(first_index=0, last_index=len(self.entry_name.get()))
            self.entry_name.configure(fg_color="#faebeb", border_color="#e64646",
                                      placeholder_text="Длина названия должна быть не более 25 символов",
                                      placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        else:
            self.name_text = self.entry_name.get()
            self.entry_name.configure(fg_color="#f9f9fa", border_color="#61bf0d", placeholder_text="")

        if not self.entry_complexity.get().isdigit():
            self.entry_complexity.configure(fg_color="#faebeb", border_color="#e64646",
                                            placeholder_text="Допустимо вводить только цифры",
                                            placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        else:
            if int(self.entry_complexity.get()) > 5 or int(self.entry_complexity.get()) < 1:
                self.entry_complexity.configure(fg_color="#faebeb", border_color="#e64646",
                                                placeholder_text="Введите значение от 1 до 5",
                                                placeholder_text_color="#979da2")
                self.label_name.focus()
                check = False
            else:
                self.complexity_text = self.entry_complexity.get()
                self.entry_complexity.configure(fg_color="#f9f9fa", border_color="#61bf0d", placeholder_text="")
        return check
