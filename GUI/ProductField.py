import tkinter as tk
import customtkinter as ctk
import BaH.product as bh_product
from GUI.StepField import *


class Product_field():  #класс продукта
    def __init__(self, count: int, app) -> None:
        self.main_window = app
        self.window_add = self.main_window.window_add
        self.list_frame_step: Step_field = []
        self.list_step = []

        self.product: bh_product
        self.count = count
        self.is_saved = 0
        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.label_count: ctk.CTkLabel
        self.frame_product_field: ctk.CTkFrame
        self.label_name: ctk.CTkLabel
        self.entry_name: ctk.CTkEntry
        self.label_selling_cost: ctk.CTkLabel
        self.entry_selling_cost: ctk.CTkEntry
        self.label_production_cost: ctk.CTkLabel
        self.entry_production_cost: ctk.CTkEntry
        self.label_commentariy: ctk.CTkLabel
        self.entry_commentariy: ctk.CTkEntry
        self.label_quantity: ctk.CTkLabel
        self.entry_quantity: ctk.CTkEntry

        self.button_aply: ctk.CTkButton
        self.button_delete: ctk.CTkButton

        self.add_product()

    def add_product(self):  #создание поля нового пустого продукта
        self.window_add.button_add_order.configure(state = "disabled")
        self.window_add.button_add_step.configure(state = "normal")

        self.label_count = ctk.CTkLabel(self.window_add.scroll_product, text="Товар № " + str(self.count),
                                        font=self.font_)
        self.label_count.pack(anchor=tk.CENTER, pady=5)

        self.frame_product_field = ctk.CTkFrame(self.window_add.scroll_product, border_width=2, width=350, height=415)
        self.frame_product_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_product_field.pack_propagate(False)
        self.frame_product_field.bind('<Button-1>', self.reload)
        

        self.label_name = ctk.CTkLabel(self.frame_product_field, text="Введите название товара", font=self.fontmini)
        self.label_name.pack(anchor=tk.CENTER, pady=5)
        self.label_name.bind('<Button-1>', self.reload)

        self.entry_name = ctk.CTkEntry(self.frame_product_field)
        self.entry_name.pack(fill=tk.X, pady=5, padx=5)
        self.entry_name.bind('<Button-1>', self.reload)

        self.label_selling_cost = ctk.CTkLabel(self.frame_product_field, text="Введите стоимость продажи",
                                               font=self.fontmini)
        self.label_selling_cost.pack(anchor=tk.CENTER, pady=5)
        self.label_selling_cost.bind('<Button-1>', self.reload)

        self.entry_selling_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_selling_cost.pack(fill=tk.X, pady=5, padx=5)
        self.entry_selling_cost.bind('<Button-1>', self.reload)

        self.label_production_cost = ctk.CTkLabel(self.frame_product_field, text="Введите себестоимость товара",
                                                  font=self.fontmini)
        self.label_production_cost.pack(anchor=tk.CENTER, pady=5)
        self.label_production_cost.bind('<Button-1>', self.reload)

        self.entry_production_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_production_cost.pack(fill=tk.X, pady=5, padx=5)
        self.entry_production_cost.bind('<Button-1>', self.reload)

        self.label_quantity = ctk.CTkLabel(self.frame_product_field, text="Введите количество товаров",
                                           font=self.fontmini)
        self.label_quantity.pack(anchor=tk.CENTER, pady=5)
        self.label_quantity.bind('<Button-1>', self.reload)

        self.entry_quantity = ctk.CTkEntry(self.frame_product_field)
        self.entry_quantity.pack(fill=tk.X, pady=5, padx=5)
        self.entry_quantity.bind('<Button-1>', self.reload)

        self.label_commentariy = ctk.CTkLabel(self.frame_product_field, text="Введите описание ",
                                              font=self.fontmini)
        self.label_commentariy.pack(anchor=tk.CENTER, pady=5)
        self.label_commentariy.bind('<Button-1>', self.reload)

        self.entry_commentariy = ctk.CTkEntry(self.frame_product_field)
        self.entry_commentariy.pack(fill=tk.X, pady=5, padx=5)
        self.entry_commentariy.bind('<Button-1>', self.reload)

        self.button_aply = ctk.CTkButton(self.frame_product_field, text="Применить", command = self.aply)
        self.button_aply.pack(side = tk.LEFT, padx = 10)

        self.button_delete = ctk.CTkButton(self.frame_product_field, text="Удалить", command = self.delete_product, fg_color = "#d9071c", hover_color= "#ad0314")
        self.button_delete.pack(side = tk.RIGHT, padx = 10)


    def aply(self):     #кнопка подтверждения продукта и добавление его в список
        if(self.chek_field()==True):
            self.product = bh_product.Product(self.entry_name.get(),
                                        int(self.entry_selling_cost.get()),
                                        self.list_step,
                                        int(self.entry_quantity.get()),
                                        int(self.entry_production_cost.get()),
                                        self.entry_commentariy.get())
            self.window_add.list_product.append(self.product)
            self.button_aply.configure(fg_color = "#2dba52", hover_color = "#189e3b", text = "Редактировать", command = self.edit)
            self.edit_state_step_button("disabled")
            self.is_saved = 1
            self.check_button_add_order()
                


            


    def edit(self):
        self.edit_state_step_button("normal")
        self.button_aply.configure(fg_color = "#3b8ed0", hover_color = "#36719f", text = "Применить", command=self.apply_edit)
        self.is_saved = 0
        self.window_add.button_add_order.configure(state = "disabled")

    def apply_edit(self):
        if(self.chek_field()==True):
            product = self.window_add.list_product[self.count-1]
            product.name = self.entry_name.get()
            product.selling_cost = int(self.entry_selling_cost.get())
            product.production_cost = int(self.entry_production_cost.get())
            product.quantity = int(self.entry_quantity.get())
            product.commentary = self.entry_commentariy.get()

            self.is_saved = 1

            self.edit_state_step_button("disabled")
            self.button_aply.configure(fg_color = "#2dba52", hover_color = "#189e3b", text = "Редактировать", command = self.edit)
            self.check_button_add_order()
        


    def delete_product(self):
        if(self.is_saved==1):
            self.window_add.list_product.pop(self.count - 1)
        ln = len(self.window_add.list_frame_product)
        if(ln != self.count):
            for i in range(self.count , ln):
                self.window_add.list_frame_product[i].count = self.window_add.list_frame_product[i].count - 1
                self.window_add.list_frame_product[i].label_count.configure(text = "Продукт №" + str(self.window_add.list_frame_product[i].count))

               

        self.label_count.destroy()
        self.frame_product_field.destroy()
        self.window_add.number_product -= 1
        del self.window_add.list_frame_product[self.count-1]
        self.window_add.frame_step.destroy()
        self.window_add.add_area_step()
        if(len(self.window_add.list_frame_product)>=1):
            self.window_add.current_product = 1
            self.window_add.list_frame_product[0].reload(tk.Event)
        self.check_button_add_order()
            
        

    def check_button_add_order(self):
        for item in self.window_add.list_frame_product:
            if(item.is_saved == 0):
                self.window_add.button_add_order.configure(state = "disabled")
                break
            else:
                self.window_add.button_add_order.configure(state = "normal")
        


    def edit_state_step_button(self, state_aply: str):
        for item in self.window_add.list_frame_product[self.count-1].list_frame_step:
            item.button_aply.configure(state = state_aply)
            item.button_delete.configure(state = state_aply)
        self.entry_name.configure(state = state_aply)
        self.entry_selling_cost.configure(state = state_aply)
        self.entry_production_cost.configure(state = state_aply)
        self.entry_commentariy.configure(state = state_aply)
        self.entry_quantity.configure(state = state_aply)

        self.window_add.button_add_step.configure(state = state_aply)



    def chek_field(self):   #проверка на введеные поля
        check = True
        if(self.entry_name.get() == ""):
            self.entry_name.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Заполните все поля", placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        elif(len(self.entry_name.get()) > 60):
            self.entry_name.delete(first_index=0, last_index= len(self.entry_name.get()))
            self.entry_name.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Длина названия должна быть не более 35 символов", placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        else:
            self.entry_name.configure(fg_color="#f9f9fa", border_color= "#61bf0d", placeholder_text = "")


        if(not(self.entry_selling_cost.get().isdigit())):
            self.entry_selling_cost.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Заполните все поля", placeholder_text_color="#979da2")
            self.label_name.focus()
            check =  False
        else:
            self.entry_selling_cost.configure(fg_color="#f9f9fa", border_color= "#61bf0d", placeholder_text = "")

        if(not(self.entry_production_cost.get().isdigit())):
            self.entry_production_cost.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Заполните все поля", placeholder_text_color="#979da2")
            self.label_name.focus()
            check =  False
        else:
            self.entry_production_cost.configure(fg_color="#f9f9fa", border_color= "#61bf0d", placeholder_text = "")


        if(not(self.entry_quantity.get().isdigit())):
            self.entry_quantity.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Заполните все поля", placeholder_text_color="#979da2")
            self.label_name.focus()
            check =  False
        else:
            self.entry_quantity.configure(fg_color="#f9f9fa", border_color= "#61bf0d", placeholder_text = "")

        if(len(self.entry_commentariy.get()) > 60):
            self.entry_commentariy.delete(first_index=0, last_index= len(self.entry_commentariy.get()))
            self.entry_commentariy.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Длина названия должна быть не более 60 символов", placeholder_text_color="#979da2")
            self.label_name.focus()
            check = False
        else:
            self.entry_commentariy.configure(fg_color="#f9f9fa", border_color= "#61bf0d", placeholder_text = "")

        if(len(self.window_add.list_frame_product[self.count-1].list_frame_step) == 0):
            check = False
        else:
            for item in self.window_add.list_frame_product[self.count-1].list_frame_step:
                if(item.is_saved == 0):
                    item.frame_step_field.configure(border_color = "#e64646")
                    check = False
                else:
                    item.frame_step_field.configure(border_color = "#979da2")
                
        return check

    def reload(self, event):    #отображение шагов связанных с этим продуктом
        if(self.window_add.current_product != self.count - 1):
            self.window_add.frame_step.destroy()
            self.window_add.add_area_step()
            self.window_add.current_product = self.count - 1
            for element in self.list_frame_step:#self.window_add.list_frame_product[self.count - 1].list_frame_step:
                element.add_step()

        if(self.is_saved == 1):
            self.window_add.button_add_step.configure(state = "disabled")
        else:
            self.window_add.button_add_step.configure(state = "normal")

