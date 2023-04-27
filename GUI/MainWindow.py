import tkinter as tk
import customtkinter as ctk
from GUI.AddWindow import *

#добавить проверку ввода для заказа
#добавить проверку что добавлен хотя бы 1 шаг и оповещение что шаги не были добавлены
#сделать сохранение продукта при нажатии кнопки добавить новый продукт  ??? необязательно
#подправить конструкторы продуктов и шагов
#испрвить баг в котором при создании заказа с несколькими продуктами показывает у продуктов одни и те же шаги если после создание этого заказа сначала открыть другой заказ  (при переходе в show_info не меняется индекс)

class MainWindow(tk.Frame):
    def __init__(self, root):
        self.root = root

        super().__init__(self.root)

        self.list_order = []
        self.init_main_window()

    def init_main_window(self):

        

        frame_title = ctk.CTkFrame(master=self.root, height=50, border_width=3, fg_color="#FFFFFF")
        self.frame_tools = ctk.CTkFrame(master=self.root, width=150, border_width=3)
        
        

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

        self.create_canvas_order()


    def create_canvas_order(self):
        
        self.frame_order = ctk.CTkFrame(master=self.root, border_width=3)
        self.frame_order.pack(anchor=tk.SW, fill=tk.BOTH, expand=tk.TRUE, padx=5, pady=5)
        #scrol = ctk.CTkScrollableFrame(self.frame_order, label_anchor=ctk.E, height=500)
        #scrol.pack(padx = 10, pady = 10, fill=tk.X)

    def add_list_order(self):
        self.frame_order.destroy()
        self.create_canvas_order()
        for item in self.list_order:
            self.frame_order_info = ctk.CTkFrame(self.frame_order, border_width=3, fg_color="#6F7A71", height=50)
            self.frame_order_info.pack(fill=tk.X, padx = 10, pady=7)
            self.label_order = ctk.CTkLabel(self.frame_order_info, text = item.zakazchik + "  " + str(item.date_of_creation)+ "  " + str(item.date_of_vidacha), font = ctk.CTkFont(family="Arial", size=12))
            self.label_order.pack(fill=tk.X, padx=10, pady = 10)
            self.label_order.bind('<Button-1>', lambda event, order = item: self.open_info(order))


    def open_info(self, order):
        self.button_add_order.configure(state = "disabled")
        self.frame_order.destroy()
        self.create_canvas_order()
        self.button_close_info = ctk.CTkButton(self.frame_tools, text="Вернуться к заказам", command=self.close_info)
        self.button_close_info.pack(anchor=tk.N, pady=6)
        self.window_info = WindowInfo(self, order)


    def close_info(self):
        del self.window_info
        self.add_list_order()
        self.button_add_order.configure(state = "normal")
        self.button_close_info.destroy()


    def open_window(self):
        self.window_add = WindowAdd(self.root, self)




class WindowInfo(tk.Frame):
    def __init__(self, main_win, order):
        self.main_window = main_win
        self.cur_order = order
        self.init_window_info()
        
        

    def init_window_info(self):
        self.frame_info_product = ctk.CTkFrame(self.main_window.frame_order, border_width=3, width=400)
        
        self.frame_info_product.pack(fill=tk.Y, padx=5, pady = 10, side=tk.LEFT, expand=True)
        self.create_step_frame()
        self.show_product()

    def create_step_frame(self):
        self.frame_info_step = ctk.CTkFrame(self.main_window.frame_order, border_width=3, width=400)
        self.frame_info_step.pack(fill=tk.Y, padx=5, pady = 10, side = tk.RIGHT, expand=True)


    def show_product(self):

        self.product = self.cur_order.GetProducts()
        for item in self.product:
            self.frame_product_show = ctk.CTkFrame(self.frame_info_product, border_width=3, fg_color="#6F7A71", height=50, width=400)
            self.frame_product_show.pack(fill=tk.X, padx = 10, pady=7)
            self.frame_product_show.pack_propagate(False)
            self.label_product = ctk.CTkLabel(self.frame_product_show, text = item.name + "  " + str(item.selling_cost - item.production_cost), font = ctk.CTkFont(family="Arial", size=12))
            self.label_product.pack(fill=tk.X, padx=10, pady = 10)
            self.label_product.bind('<Button-1>', lambda event, step_index = self.product.index(item): self.open_step_info(step_index))


    def open_step_info(self, s_index):  
        self.frame_info_step.destroy()
        self.create_step_frame()   
        step = self.product[s_index].GetSteps()
        for item in step:
            self.frame_step_show = ctk.CTkFrame(self.frame_info_step, border_width=3, fg_color="#6F7A71", height=50, width=400)
            self.frame_step_show.pack(fill=tk.X, padx = 10, pady=7)
            self.frame_step_show.pack_propagate(False)
            
            self.label_step = ctk.CTkLabel(self.frame_step_show, text = item.name + "  ", font = ctk.CTkFont(family="Arial", size=12))
            self.label_step.pack(fill=tk.X, padx=10, pady = 10)