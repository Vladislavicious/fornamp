import tkinter as tk
import customtkinter as ctk
from GUI.AddWindow import *

#добавить проверку что добавлен хотя бы 1 шаг и оповещение что шаги не были добавлены
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

        self.create_frame_order()



    def create_frame_order(self):
        
        self.frame_order = ctk.CTkFrame(master=self.root, border_width=3)
        self.frame_order.pack(anchor=tk.SW, fill=tk.BOTH, expand=tk.TRUE, padx=5, pady=5)
        self.scroll = ctk.CTkScrollableFrame(master = self.frame_order, height=600)
        self.scroll.pack(padx = 5, pady =5, fill=tk.X)

    def add_list_order(self):
        self.frame_order.destroy()
        self.create_frame_order()
        for item in self.list_order:
            self.frame_order_info = ctk.CTkFrame(self.scroll, border_width=2, fg_color="#b8bab9", height=120)
            self.frame_order_info.pack(fill=tk.X, padx = 10, pady=7)

            if(item.isDone == False):
                self.frame_order_info.configure(border_color = "#bf6b6b")
            elif(item.isDone == True and item.isVidan == False):
                self.frame_order_info.configure(border_color = "#e3a002")
            else:
                self.frame_order_info.configure(border_color = "#77bf6d")

            self.label_order = ctk.CTkLabel(self.frame_order_info, text = "Заказчик: " + item.zakazchik + "\nОписание заказа: " + item.commentary + "\nДата создания: " + str(item.date_of_creation)+ "\nДата выдачи: " + str(item.date_of_vidacha), font = ctk.CTkFont(family="Arial", size=12))
            self.label_order.pack(fill=tk.X, padx=10, pady = 10)
            self.label_order.bind('<Button-1>', lambda event, order = item: self.open_info(order))


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
        self.window_add = WindowAdd(self.root, self)




class WindowInfo(tk.Frame):
    def __init__(self, main_win, order):
        self.main_window = main_win
        self.cur_order = order
        self.cure_product = -1
        self.init_window_info()
        
        

    def init_window_info(self):
        self.frame_info_product = ctk.CTkFrame(self.main_window.root, border_width=3, width=410)     
        self.frame_info_product.pack(fill=tk.BOTH, padx=5, pady = 10, side=tk.LEFT)
        self.frame_info_product.pack_propagate(False)
        self.scroll_product = ctk.CTkScrollableFrame(master = self.frame_info_product, height=600)
        self.scroll_product.pack(padx = 3, pady =3, fill=tk.X)
        self.create_step_frame()
        self.show_product()

    def create_step_frame(self):
        self.frame_info_step = ctk.CTkFrame(self.main_window.root, border_width=3, width=410)
        self.frame_info_step.pack(fill=tk.BOTH, padx=5, pady = 10, side = tk.RIGHT)
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
        if(self.cure_product != s_index):
            self.frame_info_step.destroy()
            self.create_step_frame()   
            step = self.products[s_index].GetSteps()
            for item in step:
                self.frame_step_show = ctk.CTkFrame(self.scroll_step, border_width=2, fg_color= "#b8bab9", height=50, width=150)
                
                if(item.isDone == False):
                    self.frame_step_show.configure(border_color= "#b86161")
                else:
                    self.frame_step_show.configure(border_color= "#77bf6d")

                self.frame_step_show.pack(fill=tk.X, padx = 10, pady=7)
                self.frame_step_show.pack_propagate(False)
            
                self.label_step = ctk.CTkLabel(self.frame_step_show, text = item.name + "  ", font = ctk.CTkFont(family="Arial", size=12))

                self.label_step.pack(fill=tk.X, padx=10, pady = 10)
            self.cure_product = s_index


    def delete_window_info(self):
        self.frame_info_product.destroy()
        self.frame_info_step.destroy()
        self.main_window.create_frame_order()