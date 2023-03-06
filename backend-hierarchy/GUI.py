import tkinter as tk
from tkinter import ttk
from order import Order
from order import listFromJSON
from datetime import date, datetime


#overrideredirect(flag=None) если флаг не будет равен 0 то окно нельзя будет двигать и закрывать обычным способом

class Main_window(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.init_main()

    def init_main(self):

        frame_title = ttk.Frame(borderwidth=5, relief=tk.SOLID, height=50)
        frame_tools = ttk.Frame(borderwidth=5, relief=tk.SOLID, width=150)
        frame_order = ttk.Frame(borderwidth=5, relief=tk.SOLID)
        

        button_profile = ttk.Button(frame_title, text="Профиль")
        button_profile.pack(side = tk.RIGHT)
       
        name_label = ttk.Label(frame_title, text="НАЗВАНИЕ ПРОГРАММЫ", font =  36, padding=[15,0])
        name_label.pack(anchor = tk.N)

        button_add_order = ttk.Button(frame_tools, text = "Добавить", command=self.open_window)
        button_add_order.pack(anchor = tk.N)
 

        frame_tools.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        frame_title.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        frame_title.pack_propagate(False)
        frame_tools.pack_propagate(False)
        frame_order.pack(anchor=tk.SW, fill=tk.BOTH, expand=tk.TRUE, padx=5, pady=5)


    def open_window(self):
        Window_add()

class Window_add(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.main_window = app
        self.init_window_add()

    def init_window_add(self):
        self.geometry("1000x650+258+100")
        self.resizable(False,False)
        self.overrideredirect(True)

        self.panel_add()

        self.frame_order = ttk.Frame(self, borderwidth=5, relief=tk.SOLID, width=200)
        self.frame_product = ttk.Frame(self, borderwidth=5, relief=tk.SOLID, width=400)
        self.frame_step = ttk.Frame(self, borderwidth=5, relief=tk.SOLID, width=400)

        self.frame_order.pack(side=tk.LEFT, fill=tk.Y, padx=1, pady=1)
        self.frame_product.pack(side=tk.LEFT, fill=tk.Y, padx=1, pady=1)
        self.frame_step.pack(side=tk.LEFT, fill=tk.Y, padx=1, pady=1)
        self.frame_order.pack_propagate(False)
        self.frame_product.pack_propagate(False)
        self.frame_step.pack_propagate(False)


        button_close_order = ttk.Button(self.frame_step, text="Закрыть", command=self.destroy)
        button_close_order.pack(side=tk.RIGHT, anchor=tk.S)

        button_add_order = ttk.Button(self.frame_step, text="Добавить заказ", command=self.add)
        button_add_order.pack(side=tk.RIGHT, anchor=tk.S)

        self.order_field()
        self.product_field()

    def panel_add(self):

        frame_panel = ttk.Frame(self, width=1000, height=40)
        frame_panel.pack(side=tk.TOP)
        frame_panel.pack_propagate(False)

        self.frame_order_panel = ttk.Frame(frame_panel, borderwidth=5, relief=tk.SOLID, width=200, height=40)
        self.frame_product_panel = ttk.Frame(frame_panel, borderwidth=5, relief=tk.SOLID, width=400, height=40)
        self.frame_step_panel = ttk.Frame(frame_panel, borderwidth=5, relief=tk.SOLID, width=400, height=40)

        self.frame_order_panel.pack(side=tk.LEFT, padx=1, pady=1)
        self.frame_product_panel.pack(side=tk.LEFT, padx=1, pady=1)
        self.frame_step_panel.pack(side=tk.LEFT, padx=1, pady=1)
        self.frame_order_panel.pack_propagate(False)
        self.frame_product_panel.pack_propagate(False)
        self.frame_step_panel.pack_propagate(False)

        label_title_order = ttk.Label(self.frame_order_panel, text="ЗАКАЗ")
        label_title_order.pack(anchor=tk.CENTER, pady=5)

        button_add_product = ttk.Button(self.frame_product_panel, text="Добавить продукт", command=self.product_field)
        button_add_product.pack(side=tk.RIGHT)

        label_title_product = ttk.Label(self.frame_product_panel, text="ПРОДУКТЫ")
        label_title_product.pack(side=tk.RIGHT, pady=5, padx=50)

        label_title_step = ttk.Label(self.frame_step_panel, text="ШАГИ")
        label_title_step.pack(anchor=tk.CENTER, pady=5)



    def order_field(self):
        label_name = ttk.Label(self.frame_order, text="Введите имя заказа")
        label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name_order = ttk.Entry(self.frame_order)
        self.entry_name_order.pack(fill=tk.X, pady=5)

        label_commentariy = ttk.Label(self.frame_order, text="Введите описание заказа")
        label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy_order = ttk.Entry(self.frame_order)
        self.entry_commentariy_order.pack(fill=tk.X, pady=5)

    def product_field(self):
        frame_step_field = ttk.Frame(self.frame_product, borderwidth=5, relief=tk.SOLID, width=390, height=320)
        frame_step_field.pack(side=tk.TOP, padx=1, pady=1)
        frame_step_field.pack_propagate(False)

        label_name = ttk.Label(frame_step_field, text="Введите имя заказа")
        label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name_product = ttk.Entry(frame_step_field)
        self.entry_name_product.pack(fill=tk.X, pady=5)

        label_selling_cost = ttk.Label(frame_step_field, text="Введите стоимость продажи")
        label_selling_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_selling_cost = ttk.Entry(frame_step_field)
        self.entry_selling_cost.pack(fill=tk.X, pady=5)

        label_production_cost = ttk.Label(frame_step_field, text="Введите себестоимость товара")
        label_production_cost .pack(anchor=tk.CENTER, pady=5)

        self.entry_production_cost = ttk.Entry(frame_step_field)
        self.entry_production_cost.pack(fill=tk.X, pady=5)

        label_commentariy = ttk.Label(frame_step_field, text="Введите описание заказа")
        label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy_product = ttk.Entry(frame_step_field)
        self.entry_commentariy_product.pack(fill=tk.X, pady=5)

        label_quantity = ttk.Label(frame_step_field, text="Введите количество товаров")
        label_quantity.pack(anchor=tk.CENTER, pady=5)

        self.entry_quantity = ttk.Entry(frame_step_field)
        self.entry_quantity.pack(fill=tk.X, pady=5)



    def add(self):
        #order = Order(100,self.entry_zakzchik.get(), datetime.now(),datetime.now(), self.main_window.list_product, self.entry_commentariy)
        #label_order = ttk.Label(self.frame_order, text=self.entry_name.get())
        #label_order.pack(fill=tk.X, anchor=tk.S)

        self.destroy()
        


        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Main_window(root)
    app.pack()
    root.title("Название программы)")
    root.geometry("1000x600+250+100")
    root.resizable(False, False)
    root.mainloop()
