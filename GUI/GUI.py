import tkinter as tk
import customtkinter as ctk



class Main_window(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.init_main_window()

    def init_main_window(self):
        frame_title = ctk.CTkFrame(master=root, height=50, border_width=3, fg_color="#FFFFFF")
        frame_tools = ctk.CTkFrame(master=root, width=150, border_width=3)
        frame_order = ctk.CTkFrame(master=root, border_width=3)
        

        button_profile = ctk.CTkButton(frame_title, text="Профиль")
        button_profile.pack(side = tk.RIGHT, padx=10)
       
        name_label = ctk.CTkLabel(frame_title, text="TASK MANAGER", fg_color="transparent", font=ctk.CTkFont(family="Arial", size=24))
        name_label.place(relx=0.37,rely=0.2)

        button_add_order = ctk.CTkButton(frame_tools, text = "Добавить", command=self.open_window)
        button_add_order.pack(anchor = tk.N, pady=6)
 

        frame_tools.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        frame_title.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        frame_title.pack_propagate(False)
        frame_tools.pack_propagate(False)
        frame_order.pack(anchor=tk.SW, fill=tk.BOTH, expand=tk.TRUE, padx=5, pady=5)


    def open_window(self):
        self.window_add = Window_add()

class Window_add(ctk.CTkToplevel):
    def __init__(self):
        super().__init__(root)        
        self.main_window = app
        self.list_frame_product = []
        self.current_step: int
        
        self.init_window_add()



    def init_window_add(self):
        self.geometry("810x510+250+100")
        self.resizable(False,False)
        self.overrideredirect(True)


        self.panel_add()

        self.add_area_order()
        self.add_area_product()
        self.add_area_step()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        #надо разобраться с колоннами (разметкой)
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
         
        self.frame_order_panel = ctk.CTkFrame(self, border_width=1, width=300, corner_radius=0)
        self.frame_product_panel = ctk.CTkFrame(self, border_width=1, width=400, corner_radius=0)
        self.frame_step_panel = ctk.CTkFrame(self, border_width=1, width=400, corner_radius=0)

        self.frame_order_panel.grid(row=0, column=0, sticky="ensw")
        self.frame_product_panel.grid(row=0, column=1, columnspan=2, sticky="ensw")
        self.frame_step_panel.grid(row=0, column=3, columnspan=2, sticky="ensw")

        button_add_order = ctk.CTkButton( self.frame_order_panel, text="Добавить заказ",
                             command=self.add_new_order, width=40, height=10)
        button_add_order.pack(side=tk.TOP, pady=7)

        button_add_product = ctk.CTkButton(self.frame_product_panel, text="Добавить товар", command=self.add_product_field, width=40, height=10)
        button_add_product.pack(side=tk.TOP, pady=7)

        button_add_step = ctk.CTkButton(self.frame_step_panel, text="Добавить шаг", command=self.add_step_field, width=40, height=10)
        button_add_step.pack(side=tk.TOP, pady=7)
        



    def add_area_order(self):
        self.frame_order = ctk.CTkFrame(self, border_width=1, width=300, height=650, corner_radius=0)

        self.add_order_field()
        self.frame_order.grid(row=1, column=0, sticky="ensw")
        
        


    def add_area_product(self):
        self.number_product = 1

        scroll_y = ctk.CTkScrollbar(self)
        self.canvas_product = tk.Canvas(self, yscrollcommand=scroll_y.set) #избавиться от Canvas если это возможно
        scroll_y.configure(command=self.canvas_product.yview)

        self.frame_product = tk.Frame(self.canvas_product)

        self.canvas_product.create_window((0, 0), window=self.frame_product,
                                  anchor=tk.N)

        self.canvas_product.grid(row=1, column=1, sticky="ensw")
        scroll_y.grid(row=1, column=2, sticky="ns")



    def add_area_step(self):
        self.number_step = 1

        scroll_y = ctk.CTkScrollbar(self)
        self.canvas_step = tk.Canvas(self, yscrollcommand=scroll_y.set)
        scroll_y.configure(command=self.canvas_step.yview)

        self.frame_step = tk.Frame(self.canvas_step)

        self.canvas_step.create_window((0, 0), window=self.frame_step,
                                  anchor=tk.N)

        self.canvas_step.grid(row=1, column=3, sticky="ensw")
        scroll_y.grid(row=1, column=4, sticky="ns")



    def add_order_field(self):
        frame_order_field = ctk.CTkFrame(self.frame_order, width=250, height=700, corner_radius=0)
        frame_order_field.pack(side=tk.TOP, padx=1, pady=1)
        frame_order_field.pack_propagate(False)

        label_name = ctk.CTkLabel(frame_order_field, text="Введите имя заказа", font = font_)
        label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name_order = ctk.CTkEntry(frame_order_field)
        self.entry_name_order.pack(fill=tk.X, pady=5)

        label_commentariy = ctk.CTkLabel(frame_order_field, text="Введите описание заказа", font=font_)
        label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy_order = ctk.CTkEntry(frame_order_field)
        self.entry_commentariy_order.pack(fill=tk.X, pady=5)

        button_close = ctk.CTkButton(frame_order_field, text="Закрыть", command=self.close_window, width=40, height=10)
        button_close.pack(side=tk.BOTTOM, anchor=tk.E)

    



    def add_step_field(self):
        step = Step_field()
        
        self.list_frame_product[self.current_step].append(step) #разобраться с исключением

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

        self.add_product()


    def add_product(self):
        self.label_count = ctk.CTkLabel(self.window_add.frame_product, text="Товар № " + str(self.count), font = font_)
        self.label_count.pack(anchor=tk.CENTER, pady=5)

        self.frame_product_field = ctk.CTkFrame(self.window_add.frame_product, border_width=2, width=350, height=385)
        self.frame_product_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_product_field.pack_propagate(False)
        self.frame_product_field.bind('<Button-1>', self.reload)

        self.label_name = ctk.CTkLabel(self.frame_product_field, text="Введите название товара", font = fontmini)
        self.label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name = ctk.CTkEntry(self.frame_product_field)
        self.entry_name.pack(fill=tk.X, pady=5, padx=5)

        self.label_selling_cost = ctk.CTkLabel(self.frame_product_field, text="Введите стоимость продажи", font = fontmini)
        self.label_selling_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_selling_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_selling_cost.pack(fill=tk.X, pady=5, padx=5)

        self.label_production_cost = ctk.CTkLabel(self.frame_product_field, text="Введите себестоимость товара", font = fontmini)
        self.label_production_cost .pack(anchor=tk.CENTER, pady=5)

        self.entry_production_cost = ctk.CTkEntry(self.frame_product_field)
        self.entry_production_cost.pack(fill=tk.X, pady=5, padx=5)

        self.label_commentariy = ctk.CTkLabel(self.frame_product_field, text="Введите описание заказа", font = fontmini)
        self.label_commentariy.pack(anchor=tk.CENTER, pady=5)

        self.entry_commentariy = ctk.CTkEntry(self.frame_product_field)
        self.entry_commentariy.pack(fill=tk.X, pady=5, padx=5)

        self.label_quantity = ctk.CTkLabel(self.frame_product_field, text="Введите количество товаров", font = fontmini)
        self.label_quantity.pack(anchor=tk.CENTER, pady=5)

        self.entry_quantity = ctk.CTkEntry(self.frame_product_field)
        self.entry_quantity.pack(fill=tk.X, pady=5, padx=5)



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

        self.label_count: ctk.CTkLabel
        self.frame_step_field: ctk.CTkFrame
        self.label_name: ctk.CTkLabel
        self.entry_name: ctk.CTkEntry
        self.label_complexity_cost: ctk.CTkLabel
        self.entry_complexity_cost: ctk.CTkEntry
        self.add_step()


    def add_step(self):

        self.label_count = ctk.CTkLabel(self.window_add.frame_step, text="Шаг № " + str(self.window_add.number_step), font=font_)
        self.label_count.pack(anchor=tk.CENTER, pady=5)
        self.window_add.number_step+=1

        self.frame_step_field = ctk.CTkFrame(self.window_add.frame_step, border_width=2, width=350, height=175)
        self.frame_step_field.pack(side=tk.TOP, padx=1, pady=1)
        self.frame_step_field.pack_propagate(False)

        self.label_name = ctk.CTkLabel(self.frame_step_field, text="Введите название шага", font=fontmini)
        self.label_name.pack(anchor=tk.CENTER, pady=5)

        self.entry_name= ctk.CTkEntry(self.frame_step_field)
        self.entry_name.pack(fill=tk.X, pady=5, padx = 5)

        self.label_complexity_cost = ctk.CTkLabel(self.frame_step_field, text="Введите сложность шага", font=fontmini)
        self.label_complexity_cost.pack(anchor=tk.CENTER, pady=5)

        self.entry_complexity_cost = ctk.CTkEntry(self.frame_step_field)
        self.entry_complexity_cost.pack(fill=tk.X, pady=5, padx = 5)        

if __name__ == "__main__":
    root = ctk.CTk()
    font_ = ctk.CTkFont(family="Arial", size=16)
    fontmini = ctk.CTkFont(family="Arial", size=12)
    app = Main_window(root)
    app.pack()
    root.title("Task manager")
    root.geometry("1000x600+250+100")
    root.resizable(False, False)
    root.mainloop()
