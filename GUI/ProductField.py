import tkinter as tk
import customtkinter as ctk
import BaH.product as bh_product




class Product_field():  #класс продукта
    def __init__(self, count: int, app) -> None:
        self.main_window = app
        self.window_add = self.main_window.window_add
        self.list_frame_step: Step_field = []
        self.list_step = []

        self.prod: bh_product
        self.count = count
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

        self.add_product()

    def add_product(self):  #создание поля нового пустого продукта
        self.label_count = ctk.CTkLabel(self.window_add.frame_product, text="Товар № " + str(self.count),
                                        font=self.font_)
        self.label_count.pack(anchor=tk.CENTER, pady=5)

        self.frame_product_field = ctk.CTkFrame(self.window_add.frame_product, border_width=2, width=350, height=415)
        self.frame_product_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_product_field.pack_propagate(False)
        self.frame_product_field.bind('<Button-1>', self.reload)
        

        self.label_name = ctk.CTkLabel(self.frame_product_field, text="Введите название товара", font=self.fontmini)
        self.label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name = ctk.CTkEntry(self.frame_product_field)
        self.entry_name.pack(fill=tk.X, pady=5, padx=5)

        self.label_selling_cost = ctk.CTkLabel(self.frame_product_field, text="Введите стоимость продажи",
                                               font=self.fontmini)
        self.label_selling_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_selling_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_selling_cost.pack(fill=tk.X, pady=5, padx=5)

        self.label_production_cost = ctk.CTkLabel(self.frame_product_field, text="Введите себестоимость товара",
                                                  font=self.fontmini)
        self.label_production_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_production_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_production_cost.pack(fill=tk.X, pady=5, padx=5)

        self.label_quantity = ctk.CTkLabel(self.frame_product_field, text="Введите количество товаров",
                                           font=self.fontmini)
        self.label_quantity.pack(anchor=tk.CENTER, pady=5)

        self.entry_quantity = ctk.CTkEntry(self.frame_product_field)
        self.entry_quantity.pack(fill=tk.X, pady=5, padx=5)

        self.label_commentariy = ctk.CTkLabel(self.frame_product_field, text="Введите описание ",
                                              font=self.fontmini)
        self.label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy = ctk.CTkEntry(self.frame_product_field)
        self.entry_commentariy.pack(fill=tk.X, pady=5, padx=5)

        self.button_aply = ctk.CTkButton(self.frame_product_field, text="Применить", command = self.aply)
        self.button_aply.pack(anchor=tk.CENTER)


    def aply(self):     #кнопка подтверждения продукта и добавление его в список
        if(self.chek_field()==True):
            self.prod = bh_product.Product(self.entry_name.get(),
                                        int(self.entry_selling_cost.get()),
                                        self.list_step,
                                        int(self.entry_quantity.get()),
                                        int(self.entry_production_cost.get()))
            self.main_window.window_add.list_product.append(self.prod)
            self.button_aply.configure(fg_color = "#2dba52", hover_color = "#189e3b", text = "Редактировать")

    def chek_field(self):   #проверка на введеные поля
        if(self.entry_name.get() != "" and self.entry_commentariy.get() != "" and self.entry_selling_cost.get() != "" and self.entry_production_cost.get() != "" and self.entry_quantity.get() != ""):
            return True #наверное сюда надо добавить проверку на корректность введеных полей

    def reload(self, event):    #отображение шагов связанных с этим продуктом
        if(self.window_add.current_step != self.count - 1):
            self.window_add.canvas_step.delete(tk.ALL)
            self.window_add.add_area_step()
            self.window_add.current_step = self.count - 1
            for element in self.window_add.list_frame_product[self.count - 1]:
                element.add_step()
