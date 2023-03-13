import tkinter as tk
from tkinter import ttk



class Main_window(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.init_main_window()

    def init_main_window(self):

        frame_title = ttk.Frame(borderwidth=5, relief=tk.SOLID, height=50)
        frame_tools = ttk.Frame(borderwidth=5, relief=tk.SOLID, width=150)
        frame_order = ttk.Frame(borderwidth=5, relief=tk.SOLID)
        

        button_profile = ttk.Button(frame_title, text="Профиль")
        button_profile.pack(side = tk.RIGHT)
       
        name_label = ttk.Label(frame_title, text="TASK MANAGER", font =  36, padding=[15,0])
        name_label.pack(anchor = tk.N)

        button_add_order = ttk.Button(frame_tools, text = "Добавить", command=self.open_window)
        button_add_order.pack(anchor = tk.N)
 

        frame_tools.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        frame_title.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        frame_title.pack_propagate(False)
        frame_tools.pack_propagate(False)
        frame_order.pack(anchor=tk.SW, fill=tk.BOTH, expand=tk.TRUE, padx=5, pady=5)


    def open_window(self):
        self.window_add = Window_add()

class Window_add(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.main_window = app
        self.list_frame_product = []
        self.current_step: int
        
        self.init_window_add()



    def init_window_add(self):
        self.geometry("1000x650+258+100")
        self.resizable(False,False)
        self.overrideredirect(True)


        self.panel_add()

        self.add_area_order()
        self.add_area_product()
        self.add_area_step()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=610)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=10)
        self.columnconfigure(4, weight=1)


        self.bind("<Configure>", self.resize)
        self.minsize(self.winfo_width(), self.winfo_height())

    def resize(self, event):
        region = self.canvas_product.bbox(tk.ALL)
        self.canvas_product.configure(scrollregion=region)

        region_step = self.canvas_step.bbox(tk.ALL)
        self.canvas_step.configure(scrollregion=region_step)



    def panel_add(self):

        self.frame_order_panel = ttk.Frame(self, borderwidth=5, relief=tk.GROOVE, width=300, height=40)
        self.frame_product_panel = ttk.Frame(self, borderwidth=5, relief=tk.GROOVE, width=400, height=40)
        self.frame_step_panel = ttk.Frame(self, borderwidth=5, relief=tk.GROOVE, width=400, height=40)

        self.frame_order_panel.grid(row=0, column=0, sticky="ew")
        self.frame_product_panel.grid(row=0, column=1, columnspan=2, sticky="ew")
        self.frame_step_panel.grid(row=0, column=3, sticky="ew")

        button_add_order = ttk.Button( self.frame_order_panel, text="Добавить заказ",
                             command=self.add_new_order)
        button_add_order.pack(side=tk.RIGHT)

        label_title_order = ttk.Label(self.frame_order_panel, text="ЗАКАЗ")
        label_title_order.pack(anchor=tk.CENTER, pady=5)

        button_add_product = ttk.Button(self.frame_product_panel, text="Добавить продукт", command=self.add_product_field)
        button_add_product.pack(side=tk.RIGHT)

        label_title_product = ttk.Label(self.frame_product_panel, text="ПРОДУКТЫ")
        label_title_product.pack(side=tk.RIGHT, pady=5, padx=50)

        button_add_step = ttk.Button(self.frame_step_panel, text="Добавить шаг", command=self.add_step_field)
        button_add_step.pack(side=tk.RIGHT)

        label_title_step = ttk.Label(self.frame_step_panel, text="ШАГИ")
        label_title_step.pack(anchor=tk.CENTER, pady=5)



    def add_area_order(self):
        self.frame_order = ttk.Frame(self, borderwidth=5, relief=tk.GROOVE, width=300, height=600)

        self.add_order_field()
        self.frame_order.grid(row=1, column=0)
        
        


    def add_area_product(self):
        self.number_product = 1

        scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas_product = tk.Canvas(self, yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.canvas_product.yview)

        self.frame_product = tk.Frame(self.canvas_product)

        self.canvas_product.create_window((0, 0), window=self.frame_product,
                                  anchor=tk.N)

        self.canvas_product.grid(row=1, column=1, sticky="nsw")
        scroll_y.grid(row=1, column=2, sticky="ns")



    def add_area_step(self):
        self.number_step = 1

        scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas_step = tk.Canvas(self, yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.canvas_step.yview)

        self.frame_step = tk.Frame(self.canvas_step)

        self.canvas_step.create_window((0, 0), window=self.frame_step,
                                  anchor=tk.N)

        self.canvas_step.grid(row=1, column=3, sticky="nsw")
        scroll_y.grid(row=1, column=4, sticky="ns")



    def add_order_field(self):
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

        button_close = ttk.Button(frame_order_field, text="Закрыть", command=self.close_window)
        button_close.pack(side=tk.BOTTOM, anchor=tk.E)

    



    def add_step_field(self):
        step = Step_field()
        
        self.list_frame_product[self.current_step].append(step)

    def add_product_field(self):
        self.product = Product_field(self.number_product)
        self.number_product+=1
        list_step: Step_field = []
        self.list_frame_product.append(list_step)
        self.product.reload(tk.Event)

        


    def close_window(self):
        self.destroy()

    def add_new_order(self):
        pass



class Product_field():
    def __init__(self, count: int) -> None:
        self.main_window = app
        self.window_add = self.main_window.window_add

        self.count = count

        self.label_count: ttk.Label
        self.frame_product_field: ttk.Frame
        self.label_name: ttk.Label
        self.entry_name: ttk.Entry
        self.label_selling_cost: ttk.Label
        self.entry_selling_cost: ttk.Entry
        self.label_production_cost: ttk.Label
        self.entry_production_cost: ttk.Entry
        self.label_commentariy: ttk.Label
        self.entry_commentariy: ttk.Entry
        self.label_quantity: ttk.Label
        self.entry_quantity: ttk.Entry

        self.add_product()


    def add_product(self):
        self.label_count = ttk.Label(self.window_add.frame_product, text="Продукт № " + str(self.count))
        self.label_count.pack(anchor=tk.CENTER, pady=5)

        self.frame_product_field = ttk.Frame(self.window_add.frame_product, borderwidth=5, relief=tk.SOLID, width=350, height=320)
        self.frame_product_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_product_field.pack_propagate(False)
        self.frame_product_field.bind('<Button-1>', self.reload)

        self.label_name = ttk.Label(self.frame_product_field, text="Введите название продукта")
        self.label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name = ttk.Entry(self.frame_product_field)
        self.entry_name.pack(fill=tk.X, pady=5)

        self.label_selling_cost = ttk.Label(self.frame_product_field, text="Введите стоимость продажи")
        self.label_selling_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_selling_cost = ttk.Entry(self.frame_product_field)
        self.entry_selling_cost.pack(fill=tk.X, pady=5)

        self.label_production_cost = ttk.Label(self.frame_product_field, text="Введите себестоимость товара")
        self.label_production_cost .pack(anchor=tk.CENTER, pady=5)

        self.entry_production_cost = ttk.Entry(self.frame_product_field)
        self.entry_production_cost.pack(fill=tk.X, pady=5)

        self.label_commentariy = ttk.Label(self.frame_product_field, text="Введите описание заказа")
        self.label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy = ttk.Entry(self.frame_product_field)
        self.entry_commentariy.pack(fill=tk.X, pady=5)

        self.label_quantity = ttk.Label(self.frame_product_field, text="Введите количество товаров")
        self.label_quantity.pack(anchor=tk.CENTER, pady=5)

        self.entry_quantity = ttk.Entry(self.frame_product_field)
        self.entry_quantity.pack(fill=tk.X, pady=5)



    def reload(self, event):
        self.window_add.canvas_step.delete(tk.ALL)
        self.window_add.add_area_step()
        self.window_add.current_step = self.count-1
        for element in self.window_add.list_frame_product[self.count-1]:
            element.add_step()
        

    



class Step_field():
    def __init__(self) -> None:

        self.main_window = app
        self.window_add = self.main_window.window_add

        self.label_count: ttk.Label
        self.frame_step_field: ttk.Frame
        self.label_name: ttk.Label
        self.entry_name: ttk.Entry
        self.label_complexity_cost: ttk.Label
        self.entry_complexity_cost: ttk.Entry
        self.add_step()


    def add_step(self):

        self.label_count = ttk.Label(self.window_add.frame_step, text="Шаг № " + str(self.window_add.number_step))
        self.label_count.pack(anchor=tk.CENTER, pady=5)
        self.window_add.number_step+=1

        self.frame_step_field = ttk.Frame(self.window_add.frame_step, borderwidth=5, relief=tk.SOLID, width=350, height=150)
        self.frame_step_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_step_field.pack_propagate(False)

        self.label_name = ttk.Label(self.frame_step_field, text="Введите название шага")
        self.label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name= ttk.Entry(self.frame_step_field)
        self.entry_name.pack(fill=tk.X, pady=5)

        self.label_complexity_cost = ttk.Label(self.frame_step_field, text="Введите сложность шага")
        self.label_complexity_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_complexity_cost = ttk.Entry(self.frame_step_field)
        self.entry_complexity_cost.pack(fill=tk.X, pady=5)        




if __name__ == "__main__":
    root = tk.Tk()
    app = Main_window(root)
    app.pack()
    root.title("Task manager")
    root.geometry("1000x600+250+100")
    root.resizable(False, False)
    root.mainloop()
