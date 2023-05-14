﻿import tkinter as tk
import customtkinter as ctk
from GUI.AddWindow import *
from GUI.ProfileWindow import *
from BaH.Contribution import *


#подправить конструкторы продуктов и шагов
#испрвить баг в котором при создании заказа с несколькими продуктами показывает у продуктов одни и те же шаги если после создание этого заказа сначала открыть другой заказ  (при переходе в show_info не меняется индекс)

class MainWindow(ctk.CTkToplevel):
    def __init__(self, root):
        self.root = root

        super().__init__(root)
        self.list_order = []
        self.init_main_window()

    def init_main_window(self):

        self.title("Task manager")
        self.geometry("1000x600+250+100")
        self.resizable(False, False)

        frame_title = ctk.CTkFrame(master=self, height=50, border_width=3, fg_color="#FFFFFF")
        self.frame_tools = ctk.CTkFrame(master=self, width=150, border_width=3)
        
        

        button_profile = ctk.CTkButton(frame_title, text="Профиль")
        button_profile.pack(side=tk.RIGHT, padx=10)

        name_label = ctk.CTkLabel(frame_title, text="TASK MANAGER", fg_color="transparent",
                                  font=ctk.CTkFont(family="Arial", size=24))
        name_label.place(relx=0.37, rely=0.2)

        self.button_add_order = ctk.CTkButton(self.frame_tools, text="Добавить", command=self.open_window)
        self.button_add_order.pack(anchor=tk.N, pady=6)

        self.frame_tools.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        frame_title.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        frame_title.pack_propagate(False)
        self.frame_tools.pack_propagate(False)

        self.create_frame_order()

        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window()) 
        self.root.withdraw()



    def create_frame_order(self):
        
        self.frame_order = ctk.CTkFrame(master=self, border_width=3)
        self.frame_order.pack(anchor=tk.SW, fill=tk.BOTH, expand=tk.TRUE, padx=5, pady=5)
        self.scroll = ctk.CTkScrollableFrame(master = self.frame_order, height=600)
        self.scroll.pack(padx = 5, pady =5, fill=tk.X)

    def add_list_order(self):
        self.frame_order.destroy()
        self.create_frame_order()
        for item_order in self.list_order:
            self.frame_order_info = ctk.CTkFrame(self.scroll, border_width=2, fg_color="#b8bab9", height=120)
            self.frame_order_info.pack(fill=tk.X, padx = 10, pady=7)

            if(item_order.isDone == False):
                self.frame_order_info.configure(border_color = "#bf6b6b")
            elif(item_order.isDone == True and item_order.isVidan == False):
                self.frame_order_info.configure(border_color = "#e3a002")
            else:
                self.frame_order_info.configure(border_color = "#77bf6d")

            self.label_order = ctk.CTkLabel(self.frame_order_info, text = "Заказчик: " + item_order.zakazchik + "\nОписание заказа: " + item_order.commentary + "\nДата создания: " + str(item_order.date_of_creation)+ "\nДата выдачи: " + str(item_order.date_of_vidacha), font = ctk.CTkFont(family="Arial", size=12))
            self.label_order.pack(fill=tk.X, padx=10, pady = 10)
            self.label_order.bind('<Button-1>', lambda event, order = item_order: self.open_info(order))


    def open_info(self, order):
        self.button_add_order.configure(state = "disabled")
        self.frame_order.destroy()
        self.button_close_info = ctk.CTkButton(self.frame_tools, text="Вернуться к заказам", command=self.close_info)
        self.button_close_info.pack(anchor=tk.N, pady=6)
        self.window_info = WindowInfo(self, order)


    def close_info(self):
        self.window_info.delete_window_info()
        del self.window_info
        self.add_list_order()
        self.button_add_order.configure(state = "normal")
        self.button_close_info.destroy()


    def open_window(self):
        self.window_add = WindowAdd(self, self)

    def close_window(self):
        self.destroy()
        self.root.destroy()




class WindowInfo(tk.Frame):
    def __init__(self, main_win, order):
        self.main_window = main_win
        self.cur_order = order
        self.cure_product = -1
        self.username = "Igor"
        self.init_window_info()
        
        

    def init_window_info(self):
        self.frame_info_product = ctk.CTkFrame(self.main_window, border_width=3, width=410)     
        self.frame_info_product.pack(fill=tk.BOTH, padx=5, pady = 5, side=tk.LEFT)
        self.frame_info_product.pack_propagate(False)
        self.scroll_product = ctk.CTkScrollableFrame(master = self.frame_info_product, height=600)
        self.scroll_product.pack(padx = 3, pady =3, fill=tk.X)
        self.create_step_frame()
        self.show_product()

    def create_step_frame(self):
        self.frame_info_step = ctk.CTkFrame(self.main_window, border_width=3, width=410)
        self.frame_info_step.pack(fill=tk.BOTH, padx=5, pady = 5, side = tk.RIGHT)
        self.frame_info_step.pack_propagate(False)
        self.scroll_step = ctk.CTkScrollableFrame(master = self.frame_info_step, height=600)
        self.scroll_step.pack(padx = 3, pady =3, fill=tk.X)


    def show_product(self):

        self.products = self.cur_order.GetProducts()
        for item in self.products:
            self.frame_product_show = ctk.CTkFrame(self.scroll_product, border_width=2, fg_color= "#b8bab9", height=90, width=150)
            self.frame_product_show.pack(fill=tk.X, padx = 10, pady=7)
            self.frame_product_show.pack_propagate(False)
            self.label_product = ctk.CTkLabel(self.frame_product_show,
                                             text =  "Название продукта: " + item.name[:item.name.find(" ", 15)+1] + "\n" + item.name[item.name.find(" ", 15)+1:] + '\nОписание продукта: ' + item.commentary[:item.commentary.find(" ", 15)+1] + "\n" + item.commentary[item.commentary.find(" ", 15)+1:] + "\nПрибыль с реализации: " + str(item.selling_cost*item.quantity - item.production_cost*item.quantity) + " ₽",
                                            font = ctk.CTkFont(family="Arial", size=12))
            self.label_product.pack(fill=tk.X, padx=10, pady = 10)
            self.label_product.bind('<Button-1>', lambda event, product_index = self.products.index(item): self.open_step_info(product_index))
            if(item.isDone == False):
                self.frame_product_show.configure(border_color= "#bf6b6b")
            else:
                self.frame_product_show.configure(border_color= "#77bf6d")


    def open_step_info(self, s_index):
        self.prod_index = s_index
        if(self.cure_product != self.prod_index):
            self.frame_info_step.destroy()
            self.create_step_frame()   
            self.step = self.products[self.prod_index].GetSteps()
            for item_step in self.step:
                step_info = StepInfo(self, item_step)

            self.cure_product = self.prod_index



    def delete_window_info(self):
        self.frame_info_product.destroy()
        self.frame_info_step.destroy()
        self.main_window.create_frame_order()


class StepInfo(tk.Frame):
    def __init__(self, info_window, item_step):
        self.info_window = info_window
        self.item_step = item_step
        self.init_stepInfo()

    def init_stepInfo(self):

        self.frame_step_show = ctk.CTkFrame(self.info_window.scroll_step, border_width=2, fg_color= "#b8bab9", height=60, width=150)
                
        if(self.item_step.isDone == False):
            self.frame_step_show.configure(border_color= "#b86161")
        else:
            self.frame_step_show.configure(border_color= "#77bf6d")

        self.frame_step_show.pack(fill=tk.X, padx = 10, pady=7)
        self.frame_step_show.pack_propagate(False)
            
        if(self.item_step.isDone == False):
            self.label_step = ctk.CTkLabel(self.frame_step_show, text = "Описание шага: " + self.item_step.name[:self.item_step.name.find(" ", 12)+1] + "\n" + self.item_step.name[self.item_step.name.find(" ", 12)+1:] + "\nВыполнено шагов: " + str(self.item_step.number_of_made) + "/" + str(self.item_step.quantity), font = ctk.CTkFont(family="Arial", size=12), justify = tk.LEFT)
            self.label_step.pack(side = tk.LEFT, padx=5, pady = 10)
        else:
            self.label_step = ctk.CTkLabel(self.frame_step_show, text = "Описание шага:\n" + self.item_step.name, font = ctk.CTkFont(family="Arial", size=12), justify = tk.CENTER)
            self.label_step.pack(side = tk.TOP, padx=5, pady = 15)

        if(self.item_step.isDone == False):
            self.button_redy = ctk.CTkButton(self.frame_step_show, text = "Выполнено", command = lambda: self.change_status(self.item_step, self.frame_step_show, self.button_redy))
            self.button_redy.pack(side = tk.RIGHT, padx = 5)

    def change_status(self, item_step, frame, button):
        k = 0
        for item in item_step.GetContr():
            if(item.contributor == self.info_window.username):
                item.number_of_made += 1
                self.label_step.configure(text = "Описание шага: " + item_step.name[:item_step.name.find(" ", 12)+1] + "\n" + item_step.name[item_step.name.find(" ", 12)+1:] + "\nВыполнено шагов: " + str(item_step.number_of_made) + "/" + str(item_step.quantity))
                item_step.isDone = True
                self.info_window.products[self.info_window.prod_index].CheckIfDone()
                k = 1

        if(k == 0):
            contribution = Contribution(self.info_window.username)
            item_step.AddContr(contribution)
            self.label_step.configure(text = "Описание шага: " + item_step.name[:item_step.name.find(" ", 12)+1] + "\n" + item_step.name[item_step.name.find(" ", 12)+1:] + "\nВыполнено шагов: " + str(item_step.number_of_made) + "/" + str(item_step.quantity))
            self.info_window.products[self.info_window.prod_index].CheckIfDone()

        if(item_step.isDone == True):
            frame.configure(border_color= "#77bf6d")
            self.label_step.configure(text = "Описание шага:\n" + self.item_step.name, justify = tk.CENTER)
            self.label_step.pack(side = tk.TOP, padx=5, pady = 15)
            button.destroy()
            self.info_window.step.append(self.info_window.step.pop( self.info_window.step.index(self.item_step)))

        if(self.info_window.products[self.info_window.prod_index].isDone == True):
            self.info_window.frame_product_show.configure(border_color= "#77bf6d")
            self.info_window.cur_order.CheckIfDone()