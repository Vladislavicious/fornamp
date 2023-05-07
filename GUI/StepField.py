import tkinter as tk
import customtkinter as ctk
import BaH.step as bh_step


class Step_field():     #класс шага
    def __init__(self, app) -> None:
        self.main_window = app
        self.window_add = self.main_window.window_add
        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.index: int

        self.text = ""
        self.complex = ""

        self.color_button = "#3b8ed0"
        self.text_button = "Применить"
        self.state_entry = "normal"
        self.is_saved = 0

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

    def add_step(self):     #создание поля нового пустого шага
        self.label_count = ctk.CTkLabel(self.window_add.scroll_step, text="Шаг № " + str(self.window_add.number_step),
                                        font=self.font_)
        self.label_count.pack(anchor=tk.CENTER, pady=5)
        self.window_add.number_step += 1

        self.frame_step_field = ctk.CTkFrame(self.window_add.scroll_step, border_width=2, width=350, height=190)
        self.frame_step_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_step_field.pack_propagate(False)

        self.label_name = ctk.CTkLabel(self.frame_step_field, text="Введите название шага", font=self.fontmini)
        self.label_name.pack(anchor=tk.CENTER, pady=5)


        self.entry_name = ctk.CTkEntry(self.frame_step_field)
        self.entry_name.insert(0, self.text)
        self.entry_name.pack(fill=tk.X, pady=5, padx=5)
        self.entry_name.configure(state =  self.state_entry)

        self.label_complexity = ctk.CTkLabel(self.frame_step_field, text="Введите сложность шага (от 1 до 5)",
                                                  font=self.fontmini)
        self.label_complexity.pack(anchor=tk.CENTER, pady=5)

        self.entry_complexity = ctk.CTkEntry(self.frame_step_field)
        self.entry_complexity.insert(0, self.complex)
        self.entry_complexity.pack(fill=tk.X, pady=5, padx=5)
        self.entry_complexity.configure(state =  self.state_entry)

        if(self.is_saved == 0):
            self.button_aply = ctk.CTkButton(self.frame_step_field, text= self.text_button, fg_color = self.color_button, command = self.aply)
        else:
            self.button_aply = ctk.CTkButton(self.frame_step_field, text= self.text_button, fg_color = self.color_button, hover_color = "#189e3b", state = self.state_entry, command = self.edit)
        self.button_aply.pack(side = tk.LEFT, padx = 10)

        if(self.is_saved == 0):
            self.button_delete = ctk.CTkButton(self.frame_step_field, text="Удалить", command = self.delete_step, fg_color = "#d9071c", hover_color= "#ad0314")
        else:
            self.button_delete = ctk.CTkButton(self.frame_step_field, text="Удалить", command = self.delete_step, fg_color = "#d9071c", hover_color= "#ad0314", state = "disabled")
        self.button_delete.pack(side = tk.RIGHT, padx = 10)




    def aply(self):     #кнопка подтверждения шага и добавление его в список
        if(self.chek_field()==True):
            contributions: list = []
            self.step = bh_step.Step(self.entry_name.get(),
                                     contributions,
                                     self.window_add.number_step,
                                     False,
                                     int(self.entry_complexity.get()),
                                     1)# ЭТО КОСТЫЛЬ НАДО ПЕРЕДЕЛАТЬ  
            self.window_add.list_frame_product[self.window_add.current_product].list_step.append(self.step)
            #self.window_add.product_field.list_step.append(self.step)   
            self.is_saved = 1
            self.color_button = "#2dba52"
            self.text_button = "Редактировать"
            self.button_aply.configure(fg_color = self.color_button, hover_color = "#189e3b", text = self.text_button, command = self.edit)
            self.text = self.entry_name.get()
            self.complex = self.entry_complexity.get()
            self.state_entry = "disabled"
            self.entry_name.configure(state =  "disabled")
            self.entry_complexity.configure(state =  "disabled")
            self.index =  self.window_add.list_frame_product[self.window_add.current_product].list_step.index(self.step)
            
            


    def edit(self):
        self.button_aply.configure(fg_color = "#3b8ed0", hover_color = "#36719f", text = "Применить", command=self.apply_edit)
        self.entry_name.configure(state = "normal")
        self.entry_complexity.configure(state = "normal")
        self.is_saved = 0
        


    def apply_edit(self):
        if(self.chek_field()==True):
            #self.window_add.product_field.list_step[self.index].complexity = int(self.entry_complexity.get())
            self.step.complexity = int(self.entry_complexity.get())
            self.complex = int(self.entry_complexity.get())
            self.step.name = self.entry_name.get()
            self.text = self.entry_name.get()
            self.entry_name.configure(state = "disabled")
            self.entry_complexity.configure(state = "disabled")
            self.button_aply.configure(fg_color = "#2dba52", hover_color = "#189e3b", text = "Редактировать", command = self.edit)
            self.is_saved = 1



    def delete_step(self):
        if(self.is_saved == 1):
            self.window_add.list_frame_product[self.window_add.current_product].list_step.pop(self.index)
        ln = len(self.window_add.list_frame_product[self.window_add.current_product].list_frame_step) - 1
        if(ln != self.index):
            for i in range(self.index + 1 , ln+1):
                self.window_add.list_frame_product[self.window_add.current_product].list_frame_step[i].index = self.window_add.list_frame_product[self.window_add.current_product].list_frame_step[i].index - 1
                self.window_add.list_frame_product[self.window_add.current_product].list_frame_step[i].label_count.configure(text = "Шаг №" + str(self.window_add.list_frame_product[self.window_add.current_product].list_frame_step[i].index + 1))

        self.label_count.destroy()
        self.frame_step_field.destroy()
        self.window_add.number_step -= 1
        del self.window_add.list_frame_product[self.window_add.current_product].list_frame_step[self.index]
        



    def chek_field(self):   #проверка на введеные поля
        check = True
        if(self.entry_name.get() == ""):
            self.entry_name.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Заполните все поля", placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        elif(len(self.entry_name.get()) > 35):
            self.entry_name.delete(first_index=0, last_index= len(self.entry_name.get()))
            self.entry_name.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Длина названия должна быть не более 35 символов", placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        else:
            self.entry_name.configure(fg_color="#f9f9fa", border_color= "#61bf0d", placeholder_text = "")
        if(not(self.entry_complexity.get().isdigit())):
            self.entry_complexity.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Заполните все поля", placeholder_text_color="#979da2")
            self.label_name.focus()
            check =  False
        else:
            self.entry_complexity.configure(fg_color="#f9f9fa", border_color= "#61bf0d", placeholder_text = "")
        return check

