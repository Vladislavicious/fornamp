from datetime import date
import tkinter as tk
import customtkinter as ctk
import BaH.order as bh_order
from GUI.ProductField import *
from GUI.StepField import *




class WindowAdd(ctk.CTkToplevel):
    def __init__(self, root, app):
        super().__init__(root)

        self.main_window = app
        self.list_frame_product = []
        self.list_product = []
        
        self.current_product = 0

        self.init_window_add()

    def init_window_add(self) -> None:
        self.geometry("1000x600+250+100")
        self.resizable(False, False)  

        self.font_ = ctk.CTkFont(family="Arial", size=16)
        self.fontmini = ctk.CTkFont(family="Arial", size=12)

        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window()) 

        
        self.panel_add()
        self.add_area_order()
        self.add_area_product()
        self.add_area_step()
        
        
        self.main_window.withdraw()



    def panel_add(self):    #панель добавления шагов, продуктов, заказа
        self.frame_common_panel = self.frame_order_panel = ctk.CTkFrame(self, border_width=0, width=1000, corner_radius=0, height=40)
        self.frame_common_panel.pack(anchor=tk.W, side=tk.TOP)
        self.frame_common_panel.pack_propagate(False)

        self.frame_order_panel = ctk.CTkFrame(self.frame_common_panel, border_width=1, width=250, corner_radius=0, height=40)
        self.frame_product_panel = ctk.CTkFrame(self.frame_common_panel, border_width=1, width=375, corner_radius=0, height=40)
        self.frame_step_panel = ctk.CTkFrame(self.frame_common_panel, border_width=1, width=375, corner_radius=0, height=40)

        self.frame_order_panel.pack(side=tk.LEFT)
        self.frame_order_panel.pack_propagate(False)
        

        
        self.frame_product_panel.pack(side = tk.LEFT)
        self.frame_product_panel.pack_propagate(False)
        
        
        self.frame_step_panel.pack(side = tk.LEFT)
        self.frame_step_panel.pack_propagate(False)
        


        self.button_add_order = ctk.CTkButton(self.frame_order_panel, text="Добавить заказ", 
                                              command=self.add_new_order, state = "disabled")#, width=40, height=10)
        self.button_add_order.pack(side=tk.TOP, pady=7)

        button_add_product = ctk.CTkButton(self.frame_product_panel, text="Добавить товар",
                                           command=self.add_product_field)#, width=40, height=10)
        button_add_product.pack(side=tk.TOP, pady=7)

        self.button_add_step = ctk.CTkButton(self.frame_step_panel, text="Добавить шаг", 
                                             command=self.add_step_field)#, width=40, height=10)
        self.button_add_step.pack(side=tk.TOP, pady=7)

    def add_area_order(self):   #создание области в которой создается заказ
        self.frame_order = ctk.CTkFrame(self, border_width=1, width=250, height=560, corner_radius=0)

        self.add_order_field()
        self.frame_order.pack(side = tk.LEFT)
        self.frame_order.pack_propagate(False)

    def add_area_product(self):     #создание области в которой создается продукт
        self.number_product = 1

        self.frame_product = ctk.CTkFrame(master=self, border_width=0, width=375, height=560)
        self.frame_product.pack(side = tk.LEFT)
        self.frame_product.pack_propagate(False)
        self.scroll_product = ctk.CTkScrollableFrame(master = self.frame_product, height=560)
        self.scroll_product.pack(padx = 5, pady =5, fill=tk.X)

    def add_area_step(self):    #создание области в которой создается шаг
        self.number_step = 1

        self.frame_step = ctk.CTkFrame(master=self, border_width=0, width=375, height=560)
        self.frame_step.pack(side = tk.LEFT)
        self.frame_step.pack_propagate(False)
        self.scroll_step = ctk.CTkScrollableFrame(master = self.frame_step, height=560)
        self.scroll_step.pack(padx = 5, pady =5, fill=tk.X)

    def add_order_field(self):  #поля ввода для создания заказа и конпка выхода в главное меню
        frame_order_field = ctk.CTkFrame(self.frame_order, width=250, height=560, corner_radius=0)
        frame_order_field.pack(side=tk.TOP, padx=1, pady=1)
        frame_order_field.pack_propagate(False)

        self.label_date = ctk.CTkLabel(frame_order_field, text="Введите дату выдачи", font=self.font_)
        self.label_date.pack(anchor=tk.CENTER, pady=5)

        self.entry_data_order = ctk.CTkEntry(frame_order_field, placeholder_text="ГГГГ-ММ-ДД")
        self.entry_data_order.pack(fill=tk.X, pady=5)
        self.entry_data_order.bind('<KeyRelease>', self.edit_data)

        self.label_commentariy = ctk.CTkLabel(frame_order_field, text="Введите описание заказа", font=self.font_)
        self.label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy_order = ctk.CTkEntry(frame_order_field)
        self.entry_commentariy_order.pack(fill=tk.X, pady=5)

        self.label_error = ctk.CTkLabel(frame_order_field, text="", font=self.font_, text_color = "#e64646")
        self.label_error.pack(anchor=tk.CENTER, pady=5)

        button_close = ctk.CTkButton(frame_order_field, text="Закрыть", command=self.close_window, width=40, height=10)
        button_close.pack(side=tk.BOTTOM, anchor=tk.E)

    def add_step_field(self):   #добавление новго шага
        if (self.number_product == 1):
            return
        steps = Step_field(self.main_window)

        self.list_frame_product[self.current_product].list_frame_step.append(steps)

        steps.index =  self.list_frame_product[self.current_product].list_frame_step.index(steps)

    def add_product_field(self): #добавление новго продукта и добавление шага в список
        self.product_field = Product_field(self.number_product, self.main_window)
        self.number_product += 1
        
        self.list_frame_product.append(self.product_field)
        self.product_field.reload(tk.Event)
        self.add_step_field()

    def close_window(self):
        self.main_window.add_list_order()
        self.main_window.deiconify()
        self.destroy()

    def edit_data_vidachi_field(self): #редактирование поля ввода даты, если она введена неверно
        self.entry_data_order.delete(first_index=0, last_index = len(self.entry_data_order.get()))
        self.entry_data_order.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "ГГГГ-ММ-ДД", placeholder_text_color="#979da2")
        self.label_date.focus()

    def check_order_field(self):
        check = True

        if(self.entry_commentariy_order.get() == ""):
            self.entry_commentariy_order.configure(fg_color="#faebeb", border_color= "#e64646", placeholder_text = "Заполните это поле", placeholder_text_color="#979da2")
            self.label_commentariy.focus()
            check = False
        elif(len(self.entry_commentariy_order.get()) > 60):
            self.entry_commentariy_order.configure(fg_color="#faebeb", border_color= "#e64646")
            self.label_error.configure(text = "Введите не больше 60 символов")
            check = False
        else:
            self.entry_commentariy_order.configure(fg_color="#f9f9fa", border_color= "#61bf0d", placeholder_text = "")
        
        is_valid_date = lambda d: date.fromisoformat(d) >= date.today()
        try:
            if(is_valid_date(self.entry_data_order.get()[:10])):
                self.dat_of_vidacha = date.fromisoformat(self.entry_data_order.get()[:10])
                self.entry_data_order.configure(fg_color="#f9f9fa", border_color= "#61bf0d", placeholder_text = "")
            else:
                self.edit_data_vidachi_field()
                check = False
        except:
            self.edit_data_vidachi_field()
            check = False

        return check
        

    def edit_data(self, event):
        length = len(event.widget.get())
        if( length > 10):
           self.entry_data_order.delete(10, length)
            
    def add_new_order(self):
        if(self.check_order_field() == True):
            dat = bh_order.date.today()
            order = bh_order.Order(1, self.entry_commentariy_order.get(), dat, self.dat_of_vidacha, self.list_product, self.entry_commentariy_order.get()) #это затычка надо поменять принимаемые данные

            self.main_window.app.addNewOrder(order)
            self.main_window.app.saveNewOrderPreviews()
            self.main_window.app.saveOrder(order)
            self.close_window()
