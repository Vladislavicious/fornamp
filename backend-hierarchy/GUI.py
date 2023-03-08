import tkinter as tk
from tkinter import ttk


#пожалуйста не бейте это просто набросок)

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

        self.add_order()
        self.add_product()
        self.add_step()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=610)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=10)
        self.columnconfigure(4, weight=1)


        self.bind("<Configure>", self.resize)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

    def resize(self, event):
        region = self.canvas_product.bbox(tk.ALL)
        self.canvas_product.configure(scrollregion=region)

        region_step = self.canvas_step.bbox(tk.ALL)
        self.canvas_step.configure(scrollregion=region_step)



    def panel_add(self):

        self.frame_order_panel = ttk.Frame(self, borderwidth=5, relief=tk.SOLID, width=300, height=40)
        self.frame_product_panel = ttk.Frame(self, borderwidth=5, relief=tk.SOLID, width=400, height=40)
        self.frame_step_panel = ttk.Frame(self, borderwidth=5, relief=tk.SOLID, width=400, height=40)

        self.frame_order_panel.grid(row=0, column=0, sticky="ew")
        self.frame_product_panel.grid(row=0, column=1, columnspan=2, sticky="ew")
        self.frame_step_panel.grid(row=0, column=3, sticky="ew")

        button_add_order = ttk.Button( self.frame_order_panel, text="Добавить заказ",
                             command=self.add_new_order)
        button_add_order.pack(side=tk.RIGHT)

        label_title_order = ttk.Label(self.frame_order_panel, text="ЗАКАЗ")
        label_title_order.pack(anchor=tk.CENTER, pady=5)

        button_add_product = ttk.Button(self.frame_product_panel, text="Добавить продукт", command=self.product_field)
        button_add_product.pack(side=tk.RIGHT)

        label_title_product = ttk.Label(self.frame_product_panel, text="ПРОДУКТЫ")
        label_title_product.pack(side=tk.RIGHT, pady=5, padx=50)

        button_add_step = ttk.Button(self.frame_step_panel, text="Добавить шаг", command=self.step_field)
        button_add_step.pack(side=tk.RIGHT)

        label_title_step = ttk.Label(self.frame_step_panel, text="ШАГИ")
        label_title_step.pack(anchor=tk.CENTER, pady=5)



    def add_order(self):
        self.frame_order = ttk.Frame(self, borderwidth=5, relief=tk.SOLID, width=300, height=600)

        self.order_field()
        self.frame_order.grid(row=1, column=0)
        
        


    def add_product(self):
        self.count_product = 1

        scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas_product = tk.Canvas(self, yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.canvas_product.yview)

        self.frame_product = tk.Frame(self.canvas_product)

        self.canvas_product.create_window((0, 0), window=self.frame_product,
                                  anchor=tk.N)

        self.canvas_product.grid(row=1, column=1, sticky="nsw")
        scroll_y.grid(row=1, column=2, sticky="ns")



    def add_step(self):
        self.count_steps = 1

        scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas_step = tk.Canvas(self, yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.canvas_step.yview)

        self.frame_step = tk.Frame(self.canvas_step)

        self.canvas_step.create_window((0, 0), window=self.frame_step,
                                  anchor=tk.N)

        self.canvas_step.grid(row=1, column=3, sticky="nsw")
        scroll_y.grid(row=1, column=4, sticky="ns")



    def order_field(self):
        frame_order_field = ttk.Frame(self.frame_order, width=250, height=700)
        frame_order_field.pack(side=tk.TOP, padx=1, pady=1)
        frame_order_field.pack_propagate(False)

        label_name = ttk.Label(frame_order_field, text="Введите имя заказа")
        label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name_order = ttk.Entry(frame_order_field)
        self.entry_name_order.pack(fill=tk.X, pady=5)

        label_commentariy = ttk.Label(frame_order_field, text="Введите описание заказа")
        label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy_order = ttk.Entry(frame_order_field)
        self.entry_commentariy_order.pack(fill=tk.X, pady=5)

        button_close = ttk.Button(frame_order_field, text="Закрыть", command=self.close_window_add)
        button_close.pack(side=tk.BOTTOM, anchor=tk.E)

    def product_field(self):
        label_count_product = ttk.Label(self.frame_product, text="Продукт № " + str(self.count_product))
        label_count_product.pack(anchor=tk.CENTER, pady=5)
        self.count_product+=1

        frame_product_field = ttk.Frame(self.frame_product, borderwidth=5, relief=tk.SOLID, width=350, height=320)
        frame_product_field.pack(side=tk.TOP, padx=1, pady=1)
        frame_product_field.pack_propagate(False)

        label_name = ttk.Label(frame_product_field, text="Введите название продукта")
        label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name_product = ttk.Entry(frame_product_field)
        self.entry_name_product.pack(fill=tk.X, pady=5)

        label_selling_cost = ttk.Label(frame_product_field, text="Введите стоимость продажи")
        label_selling_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_selling_cost = ttk.Entry(frame_product_field)
        self.entry_selling_cost.pack(fill=tk.X, pady=5)

        label_production_cost = ttk.Label(frame_product_field, text="Введите себестоимость товара")
        label_production_cost .pack(anchor=tk.CENTER, pady=5)

        self.entry_production_cost = ttk.Entry(frame_product_field)
        self.entry_production_cost.pack(fill=tk.X, pady=5)

        label_commentariy = ttk.Label(frame_product_field, text="Введите описание заказа")
        label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy_product = ttk.Entry(frame_product_field)
        self.entry_commentariy_product.pack(fill=tk.X, pady=5)

        label_quantity = ttk.Label(frame_product_field, text="Введите количество товаров")
        label_quantity.pack(anchor=tk.CENTER, pady=5)

        self.entry_quantity = ttk.Entry(frame_product_field)
        self.entry_quantity.pack(fill=tk.X, pady=5)



    def step_field(self):

        label_count_step = ttk.Label(self.frame_step, text="Шаг № " + str(self.count_steps))
        label_count_step.pack(anchor=tk.CENTER, pady=5)
        self.count_steps+=1

        frame_step_field = ttk.Frame(self.frame_step, borderwidth=5, relief=tk.SOLID, width=350, height=150)
        frame_step_field.pack(side=tk.TOP, padx=1, pady=1)
        frame_step_field.pack_propagate(False)

        label_name = ttk.Label(frame_step_field, text="Введите название шага")
        label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name_product = ttk.Entry(frame_step_field)
        self.entry_name_product.pack(fill=tk.X, pady=5)

        label_complexity_cost = ttk.Label(frame_step_field, text="Введите сложность шага")
        label_complexity_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_complexity_cost = ttk.Entry(frame_step_field)
        self.entry_complexity_cost.pack(fill=tk.X, pady=5)
        


    def close_window_add(self):
        self.destroy()

    def add_new_order(self):
        pass
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Main_window(root)
    app.pack()
    root.title("Название программы)")
    root.geometry("1000x600+250+100")
    root.resizable(False, False)
    root.mainloop()
